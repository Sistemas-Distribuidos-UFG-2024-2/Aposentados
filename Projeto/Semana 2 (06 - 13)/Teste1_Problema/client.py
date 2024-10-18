import socket

def send_request_to_load_balancer(load_balancer_address, load_balancer_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((load_balancer_address, load_balancer_port))

        # Envia uma requisição simples ao balanceador
        request = "GET / HTTP/1.1\r\nHost: cliente\r\n\r\n"
        sock.sendall(request.encode('utf-8'))

        # Recebe a resposta
        response = sock.recv(1024)
        print(f"Resposta do servidor: {response.decode('utf-8')}")
        
        sock.close()
    except socket.error as e:
        print(f"Erro ao se conectar ao balanceador: {e}")

if __name__ == "__main__":
    send_request_to_load_balancer('127.0.0.1', 8080)  # Endereço e porta do balanceador de carga
