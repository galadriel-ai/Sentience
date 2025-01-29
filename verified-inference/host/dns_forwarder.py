import socket

VSOCK_PORT = 5053


def get_system_dns():
    """Retrieve the first nameserver from /etc/resolv.conf."""
    try:
        with open("/etc/resolv.conf", "r") as f:
            for line in f:
                if line.startswith("nameserver"):
                    return line.split()[1], 53  # Extract the IP and set port 53
    except Exception as e:
        print(f"Failed to get system DNS: {e}")

    return "8.8.8.8", 53  # Fallback to Google DNS if none found


def forward_dns_to_public(dns_request, dns_ip, dns_port):
    """Forward the DNS request to a public DNS resolver."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dns_sock:
        dns_sock.sendto(
            dns_request, (dns_ip, dns_port)
        )  # Send request to the DNS resolver
        response, _ = dns_sock.recvfrom(512)  # Receive response from the DNS resolver
        return response


def vsock_dns_proxy():
    """Listen on a vsock port and forward DNS requests to a public DNS server."""
    server_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    server_socket.bind((socket.VMADDR_CID_ANY, VSOCK_PORT))
    server_socket.listen(5)
    print(f"Listening for DNS requests on vsock port {VSOCK_PORT}...")
    dns_ip, dns_port = get_system_dns()
    print(f"Using DNS server {dns_ip}:{dns_port}")

    while True:
        client_socket, _ = server_socket.accept()
        print("Received DNS request from enclave.")

        try:
            # Receive the DNS request
            dns_request = client_socket.recv(512)
            dns_response = forward_dns_to_public(dns_request, dns_ip, dns_port)

            # Send response back to enclave
            client_socket.sendall(dns_response)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()


if __name__ == "__main__":
    vsock_dns_proxy()
