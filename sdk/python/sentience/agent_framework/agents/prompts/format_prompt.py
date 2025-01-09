from typing import Dict


def execute(prompt_template: str, prompt_state: Dict) -> str:
    prompt = prompt_template
    for k, v in prompt_state.items():
        prompt = prompt.replace("{{" + k + "}}", str(v))
    return prompt
