import socket
import threading
import time
import os

# Dicionário que armazena os domínios e seus respectivos IPs
domain_ip_mapping = {
    "exemplo.com": "93.184.216.34",
    "google.com": "142.250.190.46",
    "qualquercoisa.com": "98.137.11.163"
}

def handle_request(data):
    domain = data.decode('utf-8').strip()
    if domain in domain_ip_mapping:
        return f"IP for {domain}: {domain_ip_mapping[domain]}"
    else:
        return f"Domain {domain} not found"

def run_server():
    server_address = ('localhost', 5003)  # Endereço e porta do servidor 5003 o cliente vai conectar
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(1)
    
    print(f"Servidor alocado em {server_address}")

    while True:
        print("\nAguardando Conexão...")
        connection, client_address = sock.accept()
        try:
            print(f"Connected to {client_address}")

            while True:
                data = connection.recv(1024) #tamanho da msg
                if not data:
                    break
                print(f"Domínio a ser pesquisado: {data.decode('utf-8')}")
                
                response = handle_request(data)
                connection.sendall(response.encode('utf-8'))
        
        finally:
            connection.close()

def checagem_de_saude_servidor(host, porta):

    """
    print(f"Checando Status do Servidor {host}")
    response = os.system(f"ping -c 1 {host}")
    if response == 0:
        print(f"{host} is up!")
    else:
        print(f"{host} is down!")



    """
    try:
        mensagem = "Checagem_Saude"
        # Criando um objeto socket
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Conectando ao host e porta especificados
        cliente_socket.connect((host, porta))
        
        # Enviando a mensagem (convertida para bytes)
        cliente_socket.sendall(mensagem.encode('utf-8'))
        
        # Recebendo a resposta (opcional)
        resposta = cliente_socket.recv(1024).decode('utf-8')
        print(f"Resposta do servidor: {resposta}\nO Servidor está Online")
        
        # Fechando a conexão
        cliente_socket.close()

        return True
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

        return False
    

def ServicoDeDescoberta():
    IP = 'localhost' #IP = "255.255.255.255" EnderecoDeBroadCast
    Porta = 5001
    mensagem = "DESCOBERTA"

    try:
        # Criando um objeto socket
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Conectando ao host e porta especificados
        cliente_socket.connect((IP, Porta))
        
        # Enviando a mensagem (convertida para bytes)
        cliente_socket.sendall(mensagem.encode('utf-8'))
        
        # Recebendo a resposta (opcional)
        resposta = cliente_socket.recv(1024).decode('utf-8')
        print(f"Resposta do servidor: {resposta}\nO Servidor está Online")
        
        # Fechando a conexão
        cliente_socket.close()

        if ':' in resposta:
            novo_dominio, novo_ip = resposta.split(':')
            novo_dominio = novo_dominio.strip()  # Removendo possíveis espaços
            novo_ip = novo_ip.strip()  # Removendo possíveis espaços
            
            # Adicionando o novo domínio
            if novo_dominio not in domain_ip_mapping:
                domain_ip_mapping[novo_dominio] = novo_ip
                print(f"Novo domínio adicionado: {novo_dominio} -> {novo_ip}")
            else:
                print(f"O domínio {novo_dominio} já existe no mapeamento.")
        else:
            print("A resposta do servidor está em um formato inesperado.")

    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    
    
if __name__ == "__main__":
    #run_server()
    #checagem_de_saude_servidor('localhost', 5000)
    ServicoDeDescoberta()

    print(domain_ip_mapping)