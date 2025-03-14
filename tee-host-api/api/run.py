import argparse
import socket
import uvicorn


def main():
    port: int = 5000
    print(f"Starting Uvicorn on {port} ...")
    uvicorn.run("app:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
