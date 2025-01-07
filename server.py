import socket

Host = "127.0.0.1"
PORT = 4444

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((Host, PORT))
    s.listen()
    conn, addr = s.accept()
    print(f'printed connection : {conn}')
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)