import socket
import struct
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()


class HostProxy:
    BUFFER_SIZE = 1024
    CID = 3  # The CID of the enclave
    PORT = 8001  # The port where this proxy listens for traffic from the enclave

    def forward(self, source, destination):
        """Forward data between two sockets."""
        try:
            while True:
                data = source.recv(self.BUFFER_SIZE)
                if not data:
                    break
                destination.sendall(data)
        except Exception as exc:
            logger.error(f"Exception in forward: {exc}")
        finally:
            source.close()
            destination.close()

    def handle_vsock_connection(self, vsock_client):
        """
        Handles a new connection from the enclave over vsock,
        extracts the original destination, and forwards traffic.
        """
        try:
            # Read first 6 bytes which contain the prepended IP and port
            header = vsock_client.recv(6)
            if len(header) < 6:
                logger.error("Error: Incomplete header received")
                vsock_client.close()
                return

            # Extract original IP and port
            original_ip_bin, original_port_bin = header[:4], header[4:6]
            original_ip = socket.inet_ntoa(
                original_ip_bin
            )  # Convert binary IP to string
            original_port = struct.unpack("!H", original_port_bin)[
                0
            ]  # Convert binary port to integer

            logger.info(f"Forwarding traffic to {original_ip}:{original_port}")

            # Connect to the real destination
            destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            destination_socket.connect((original_ip, original_port))

            # Start forwarding traffic in both directions
            outgoing_thread = threading.Thread(
                target=self.forward, args=(vsock_client, destination_socket)
            )
            incoming_thread = threading.Thread(
                target=self.forward, args=(destination_socket, vsock_client)
            )

            outgoing_thread.start()
            incoming_thread.start()
        except Exception as exc:
            logger.error(f"Error handling vsock connection: {exc}")
            vsock_client.close()

    def start(self):
        """Starts the host-side proxy listening on vsock."""
        try:
            vsock_server = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
            vsock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            vsock_server.bind((self.CID, self.PORT))
            vsock_server.listen(10)

            logger.info(
                f"Host proxy listening on vsock {self.vsock_cid}:{self.vsock_port}"
            )

            while True:
                client_socket, _ = vsock_server.accept()
                threading.Thread(
                    target=self.handle_vsock_connection, args=(client_socket,)
                ).start()
        except Exception as exc:
            logger.error(f"HostProxy exception: {exc}")


if __name__ == "__main__":
    proxy = HostProxy()
    proxy.start()
