import socket

# Define the server's IP address and port
server_ip = '127.0.0.1'
server_port = 8080

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the address and port
server_socket.bind((server_ip, server_port))

print(f"UDP server up and listening on {server_ip}:{server_port}")

# Loop to keep the server running
try:
    while True:
        # Receive message from client
        message, client_address = server_socket.recvfrom(1024)  # 1024 is the buffer size
        print(f"Message from {client_address}: {message.decode()}")

        # Optionally, send a response back to the client
        response = "Message received"
        server_socket.sendto(response.encode(), client_address)
        
except KeyboardInterrupt:
    print("Server is shutting down.")

# Close the socket
server_socket.close()
