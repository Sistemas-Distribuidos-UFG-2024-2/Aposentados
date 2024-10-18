import socket

def start_server(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((address, port))
    sock.listen(5)
    print(f"Servidor rodando em {address}:{port}")

    while True:
        client_socket, client_address = sock.accept()
        print(f"Conexão estabelecida com {client_address}")
        
        request = client_socket.recv(1024)
        print(f"Requisição recebida: {request.decode('utf-8')}")
        
        # Resposta simples
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from the server!"
        client_socket.sendall(response.encode('utf-8'))
        
        client_socket.close()

if __name__ == "__main__":
    start_server('0.0.0.0', 8080)
