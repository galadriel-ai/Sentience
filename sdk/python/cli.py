import os
import shutil
from io import BytesIO
from zipfile import ZipFile
import click
import requests
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from typing import Tuple

@click.group()
def main():
    """Sentience CLI"""
    pass

@main.group()
def agent():
    """Agent-related commands."""
    pass

@agent.command()
def init() -> None:
    """Create a new Agent folder template in the current directory."""
    agent_name = click.prompt("Enter agent name", type=str)
    docker_username = click.prompt("Enter Docker username", type=str)
    docker_password = click.prompt("Enter Docker password", hide_input=True, type=str)
    galadriel_api_key = click.prompt("Enter Galadriel API key", hide_input=True, type=str)

    click.echo(f"Creating a new agent template in {os.getcwd()}...")
    try:
        _create_agent_template(agent_name, docker_username, docker_password, galadriel_api_key)
        click.echo("Successfully created agent template!")
    except Exception as e:
        click.echo(f"Error creating agent template: {str(e)}", err=True)

@agent.command()
@click.option('--image-name', default='agent', help='Name of the Docker image')
def build(image_name: str) -> None:
    """Build the agent Docker image."""
    try:
        docker_username, _ = _assert_config_files(image_name=image_name)
        _build_image(docker_username=docker_username)
    except subprocess.CalledProcessError as e:
        raise click.ClickException(f"Docker command failed: {str(e)}")
    except Exception as e:
        raise click.ClickException(str(e))

@agent.command()
@click.option('--image-name', default='agent', help='Name of the Docker image')
def publish(image_name: str) -> None:
    """Publish the agent Docker image to the Docker Hub."""
    try:
        docker_username, docker_password = _assert_config_files(image_name=image_name)
        _publish_image(image_name=image_name, docker_username=docker_username, docker_password=docker_password)
    except subprocess.CalledProcessError as e:
        raise click.ClickException(f"Docker command failed: {str(e)}")
    except Exception as e:
        raise click.ClickException(str(e))

@agent.command()
@click.option('--image-name', default='agent', help='Name of the Docker image')
def deploy(image_name: str) -> None:
    """Build, publish and deploy the agent."""
    try:
        docker_username, docker_password = _assert_config_files(image_name=image_name)

        click.echo("Building agent...")
        _build_image(docker_username=docker_username)

        click.echo("Publishing agent...")
        _publish_image(image_name=image_name, docker_username=docker_username, docker_password=docker_password)

        click.echo("Deploying agent...")
        agent_id = _galadriel_deploy(image_name)
        if not agent_id:
            raise click.ClickException("Failed to deploy agent")
        click.echo(f"Successfully deployed agent! Agent ID: {agent_id}")
    except Exception as e:
        raise click.ClickException(str(e))

@click.command()
def get_agent_state(agent_id: str):
    """Get information about a deployed agent from Galadriel platform."""
    try:
        response = requests.get(
            f"https://api.galadriel.com/agent/{agent_id}",
            headers={"Content-Type": "application/json"}
        )

        if not response.status_code == 200:
            click.echo(f"Failed to get agent state with status {response.status_code}: {response.text}")
        click.echo(json.dumps(response.json(), indent=2))
    except Exception as e:
        click.echo(f"Failed to get agent state: {str(e)}")

@click.command()
def get_agent_ids():
    """Get list of agent IDs for the current Galadriel user."""
    try:
        galadriel_key = os.getenv('GALADRIEL_API_KEY')
        if not galadriel_key:
            raise click.ClickException("GALADRIEL_KEY environment variable not set")

        response = requests.get(
            f"https://api.galadriel.com/agent/{galadriel_key}",
            headers={"Content-Type": "application/json"}
        )
        if not response.status_code == 200:
            click.echo(f"Failed to get agent IDs with status {response.status_code}: {response.text}")
        
        click.echo(json.dumps(response.json(), indent=2))
    except Exception as e:
        click.echo(f"Failed to get agent IDs: {str(e)}")


def _assert_config_files(image_name: str) -> Tuple[str, str]:
    if not os.path.exists('docker-compose.yml'):
            raise click.ClickException("No docker-compose.yml found in current directory")
    if not os.path.exists('.env'):
        raise click.ClickException("No .env file found in current directory")
    
    load_dotenv(dotenv_path=Path(".") / ".env")
    docker_username = os.getenv('DOCKER_USERNAME')
    docker_password = os.getenv('DOCKER_PASSWORD')
    os.environ['IMAGE_NAME'] = image_name # required for docker-compose.yml
    if not docker_username or not docker_password:
        raise click.ClickException("DOCKER_USERNAME or DOCKER_PASSWORD not found in .env file")
    return docker_username, docker_password

def _create_agent_template(agent_name: str, docker_username: str, docker_password: str, galadriel_api_key: str) -> None:
    """Download and extract the template repository files in the current directory."""
    # TODO: maybe fork the repo instead of downloading the zip file so the user can source control their changes (?)
    zip_url = "https://github.com/galadriel-ai/galadriel-agent/archive/refs/heads/main.zip"
    
    # Download the zip file
    response = requests.get(zip_url, timeout=30)
    response.raise_for_status()
    
    # Extract contents to current directory
    with ZipFile(BytesIO(response.content)) as zip_file:
        root_dir = zip_file.namelist()[0]        
        for file in zip_file.namelist()[1:]:
            relative_path = file[len(root_dir):]
            if relative_path:
                if relative_path == 'agents/agent.json' and agent_name:
                    # Update the agent json file name and "name" field within the file
                    with zip_file.open(file) as source:
                        agent_json = json.load(source)
                        agent_json["name"] = agent_name
                        relative_path = f'agents/{agent_name}.json'
                        os.makedirs(os.path.dirname(relative_path), exist_ok=True)
                        with open(relative_path, 'w') as f:
                            json.dump(agent_json, f, indent=2)
                    continue
                
                if file.endswith('/'):
                    os.makedirs(relative_path.rstrip('/'), exist_ok=True)
                else:
                    with zip_file.open(file) as source:
                        with open(relative_path, 'wb') as target:
                            shutil.copyfileobj(source, target)
    
    # Create .env file in the agent directory
    env_content = f"""DOCKER_USERNAME={docker_username}
DOCKER_PASSWORD={docker_password}
GALADRIEL_API_KEY={galadriel_api_key}"""
    with open('.env', 'w') as f:
        f.write(env_content)


def _build_image(docker_username: str) -> None:
    """Core logic to build the Docker image."""
    click.echo(f"Building Docker image with tag {docker_username}/{os.environ['IMAGE_NAME']}...")
    subprocess.run(['docker-compose', 'build'], check=True)
    click.echo("Successfully built Docker image!")

def _publish_image(image_name: str, docker_username: str, docker_password: str) -> None:
    """Core logic to publish the Docker image to the Docker Hub."""

    # Login to Docker Hub
    click.echo("Logging into Docker Hub...")
    login_process = subprocess.run(
        ['docker', 'login', '-u', docker_username, '--password-stdin'],
        input=docker_password.encode(),
        capture_output=True
    )
    if login_process.returncode != 0:
        raise click.ClickException(f"Docker login failed: {login_process.stderr.decode()}")
    
    # Create repository if it doesn't exist
    click.echo(f"Creating repository {docker_username}/{image_name} if it doesn't exist...")
    create_repo_url = f"https://hub.docker.com/v2/repositories/{docker_username}/{image_name}"
    token_response = requests.post(
        'https://hub.docker.com/v2/users/login/',
        json={'username': docker_username, 'password': docker_password}
    )
    if token_response.status_code == 200:
        token = token_response.json()['token']
        requests.post(create_repo_url, headers={'Content-Type': 'application/json', 'Authorization': f'JWT {token}'},
                        json={'name': image_name, 'is_private': False})
    # Push image to Docker Hub
    click.echo(f"Pushing Docker image {docker_username}/{image_name}:latest ...")
    subprocess.run(['docker', 'push', f'{docker_username}/{image_name}:latest'], check=True)
    
    click.echo("Successfully pushed Docker image!")

def _galadriel_deploy(image_name: str, docker_username: str) -> str:
    """Deploy agent to Galadriel platform."""

    if not os.path.exists('.agents.env'):
        raise click.ClickException("No .agents.env file found in current directory. Please create one.")
    
    with open('.agents.env', 'r') as f:
        env_vars = f.read()

    payload = {
        "name": image_name,
        "docker_image": f"{docker_username}/{image_name}:latest",
        "env_vars": env_vars
    }

    response = requests.post(
        "https://api.galadriel.com/agent",
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        agent_id = response.json()["agent_id"]
        return agent_id
    else:
        return None
