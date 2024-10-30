import socket
import threading

# Função para registrar o cliente no servidor
def register_on_server(server_ip, server_port, identifier, udp_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    client.send(f"REGISTER|{identifier},{socket.gethostbyname(socket.gethostname())},{udp_port}".encode())
    response = client.recv(1024).decode()
    client.close()
    return response

# Função para consultar informações de outro cliente no servidor
def lookup_client(server_ip, server_port, target_id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    client.send(f"LOOKUP|{target_id}".encode())
    response = client.recv(1024).decode()
    client.close()
    return response

# Função para enviar mensagem UDP
def send_udp_message(ip, port, message):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(message.encode(), (ip, port))

# Função para iniciar o ouvinte UDP em uma thread separada
def start_udp_listener(udp_port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("localhost", udp_port))
    print(f"Escutando mensagens UDP na porta {udp_port}...")

    while True:
        message, addr = udp_socket.recvfrom(1024)
        print(f"Mensagem recebida de {addr}: {message.decode()}")

# Função principal para a interface interativa do cliente
def client_interface(server_ip, server_port, identifier, udp_port):
    # Registra o cliente no servidor
    response = register_on_server(server_ip, server_port, identifier, udp_port)
    if response == "REGISTERED":
        print("Registrado com sucesso no servidor.")
    else:
        print("Falha ao registrar no servidor.")
        return
    
    # Menu de operações do cliente
    while True:
        print("\nEscolha uma opção:")
        print("1. Consultar outro cliente")
        print("2. Enviar mensagem para outro cliente (UDP)")
        print("3. Sair")

        option = input("Opção: ")

        if option == "1":
            target_id = input("Digite o identificador do cliente que deseja consultar: ")
            response = lookup_client(server_ip, server_port, target_id)
            if response == "NOT_FOUND":
                print("Cliente não encontrado.")
            else:
                ip, port = response.split(",")
                print(f"Cliente encontrado: IP={ip}, Porta={port}")

        elif option == "2":
            ip = input("Digite o IP do cliente: ")
            port = int(input("Digite a porta UDP do cliente: "))
            message = input("Digite a mensagem a ser enviada: ")
            send_udp_message(ip, port, message)
            print("Mensagem enviada.")

        elif option == "3":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

# Executa a interface do cliente com entrada de dados manual
if __name__ == "__main__":
    # Dados do servidor e do cliente
    server_ip = input("Digite o IP do servidor (localhost para local): ") or "localhost"
    server_port = int(input("Digite a porta do servidor (5000 por padrão): ") or 5000)
    identifier = input("Digite seu identificador (ex.: cliente@email.com): ")
    udp_port = int(input("Digite sua porta UDP para receber mensagens: "))
    
    # Inicia o ouvinte UDP em uma thread separada
    threading.Thread(target=start_udp_listener, args=(udp_port,), daemon=True).start()
    
    # Inicia o menu de interface do cliente
    client_interface(server_ip, server_port, identifier, udp_port)
