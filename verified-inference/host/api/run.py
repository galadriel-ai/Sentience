import argparse
import socket
import uvicorn


def main():
    port: int = 5000
    print(f"Starting Uvicorn on localhost:{port} ...")
    uvicorn.run("app:app", host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
