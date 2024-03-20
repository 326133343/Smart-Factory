import socket
import threading

class TCPServer:
    def __init__(self, ip, port, data_processor):
        self.ip = ip
        self.port = port
        self.server_socket = None
        self.data_processor = data_processor

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(3)
        print(f"Server listening on {self.ip}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

    def handle_client(self, client_socket, address):
        print(f"Connection from {address} has been established.")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            self.data_processor.process_and_store_data(data.decode('utf-8'))

        client_socket.close()
        print(f"Connection from {address} closed.")
