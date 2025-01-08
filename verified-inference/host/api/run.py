import argparse
import socket
import uvicorn


def main(debug: bool):
    if debug:
        port: int = 5001
        # Bind to localhost:port
        print(f"Starting Uvicorn on localhost:{port} (debug mode)...")
        uvicorn.run("app:app", host="127.0.0.1", port=port)
    else:
        print("Starting Uvicorn on VSOCK...")
        try:
            client_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
            cid = socket.VMADDR_CID_ANY
            client_port = 5000
            client_socket.bind((cid, client_port))
            client_socket.listen()

            # Get the file descriptor of the socket
            fd = client_socket.fileno()

            # Run Uvicorn using the file descriptor
            uvicorn.run("app:app", fd=fd)
        except Exception as e:
            print(f"Failed to start Uvicorn with VSOCK: {e}")
        finally:
            client_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Uvicorn with VSOCK or localhost.")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run the server in debug mode (bind to localhost:5000 instead of VSOCK).",
    )
    args = parser.parse_args()
    main(args.debug)
