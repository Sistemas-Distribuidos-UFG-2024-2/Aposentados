import socket
import threading
import json
import os

# Arquivo de registros
REGISTRY_FILE = "registros.json"

# Carrega os registros existentes, se houver
def load_registry():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    return {}

# Salva os registros no arquivo
def save_registry():
    with open(REGISTRY_FILE, "w") as f:
        json.dump(clients, f)

# Inicializa a tabela de clientes com os registros salvos
clients = load_registry()

def handle_client(conn, addr):
    while True:
        try:
            # Recebe a mensagem do cliente
            message = conn.recv(1024).decode()
            if not message:
                break
            
            action, data = message.split("|", 1)
            
            if action == "REGISTER":
                # Extrai o identificador, IP e porta do cliente
                identifier, client_ip, client_port = data.split(",")
                clients[identifier] = (client_ip, int(client_port))
                save_registry()  # Salva no arquivo
                conn.send("REGISTERED".encode())
            
            elif action == "LOOKUP":
                # Busca o identificador do cliente requisitado
                target_id = data
                if target_id in clients:
                    target_info = f"{clients[target_id][0]},{clients[target_id][1]}"
                    conn.send(target_info.encode())
                else:
                    conn.send("NOT_FOUND".encode())
        
        except Exception as e:
            print(f"Erro: {e}")
            break

    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5000))
    server.listen()
    print("Servidor TCP iniciado em localhost:5000")

    while True:
        conn, addr = server.accept()
        print(f"Conexão de {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start_server()
