import socket
import time

# Lista de servidores (endereços IP e portas)
servers = [
    ('0.0.0.0', 8080),  # s1
]

###
#('192.168.1.102', 8080),  # s2
#    ('192.168.1.103', 8080)   # s3
### 

# Função para checar se o servidor está ativo
def check_server(address, port):
    try:
        # Tenta conectar ao servidor
        sock = socket.create_connection((address, port), timeout=2)
        sock.close()
        return True
    except socket.error:
        return False

# Função para balancear requisições entre os servidores
def send_request(data):
    for server in servers:
        address, port = server
        if check_server(address, port):
            try:
                # Cria uma conexão com o servidor ativo
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((address, port))
                print(f"Enviando dados para o servidor {address}:{port}")
                
                # Envia dados
                sock.sendall(data.encode('utf-8'))
                
                # Recebe a resposta do servidor
                response = sock.recv(1024)
                print(f"Resposta do servidor {address}:{port}: {response.decode('utf-8')}")
                
                sock.close()
                return response.decode('utf-8')
            except socket.error as e:
                print(f"Erro ao se conectar com o servidor {address}:{port}: {e}")
        else:
            print(f"Servidor {address}:{port} está offline.")
    
    print("Nenhum servidor está disponível.")
    return None

# Teste de envio de requisição
if __name__ == "__main__":
    while True:
        # Simulando envio de uma requisição
        data = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        response = send_request(data)
        if response:
            print("Requisição processada com sucesso.")
        else:
            print("Falha ao processar a requisição.")

        # Pausa de 5 segundos antes de enviar a próxima requisição
        time.sleep(5)
