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
        json.dump(clients, f, indent=4)

# Inicializa a tabela de clientes com os registros salvos
clients = load_registry()

def handle_client(conn, addr):
    while True:
        try:
            # Recebe a mensagem do cliente
            message = conn.recv(1024).decode()
            if not message:
                break
            
            try:
                # Tenta carregar a mensagem como JSON
                request = json.loads(message)
                operation = request.get("operation")  # Operação desejada
                funcionario = request.get("funcionario")  # Dados do funcionário

                # Verifica qual operação foi solicitada
                if operation == "REGISTER":
                    identifier = request.get("identifier")
                    client_ip = request.get("ip")
                    client_port = request.get("port")
                    
                    # Registro do cliente
                    clients[identifier] = {"ip": client_ip, "port": int(client_port)}
                    save_registry()
                    conn.send("REGISTERED".encode())

                elif operation == "LOOKUP":
                    # Pesquisa o cliente pelo identificador
                    target_id = request.get("identifier")
                    if target_id in clients:
                        target_info = f"{clients[target_id]['ip']},{clients[target_id]['port']}"
                        conn.send(target_info.encode())
                    else:
                        conn.send("NOT_FOUND".encode())

                elif operation == "CADASTRAR_FUNCIONARIO":
                    if funcionario:
                        # Verifica se o CPF do funcionário já existe
                        cpf_existente = any(func["cpf"] == funcionario["cpf"] for func in clients.values())
                        
                        if cpf_existente:
                            conn.send("APOSENTADO_JA_CADASTRADO".encode())
                        else:
                            # Define o identificador do funcionário automaticamente
                            identifier = f"Aposentado{len(clients) + 1}"
                            
                            # Armazena o funcionário no dicionário clients com o identificador automático
                            clients[identifier] = funcionario
                            save_registry()
                            
                            conn.send(f"{identifier}_CADASTRADO".encode())
                    else:
                        conn.send("DADOS_FUNCIONARIO_INVALIDOS".encode())
                
                elif operation == "PESQUISAR_FUNCIONARIO":
                    if funcionario:
                        # Verifica se o CPF do funcionário já existe
                        cpf_existente = any(func["cpf"] == funcionario["cpf"] for func in clients.values())
                        
                        if cpf_existente:
                            conn.send("Valido".encode())
                        else:
                            conn.send("NÃO_ENCONTRADO".encode())
                    else:
                        conn.send("DADOS_FUNCIONARIO_INVALIDOS".encode())
                
                else:
                    # Operação desconhecida
                    conn.send("OPERACAO_DESCONHECIDA".encode())

            except json.JSONDecodeError:
                # Mensagem não estava em formato JSON
                conn.send("FORMATO_INVALIDO".encode())

        except Exception as e:
            print(f"Erro: {e}")
            break

    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5005))
    server.listen()
    print("Servidor iniciado em localhost:5005")

    while True:
        conn, addr = server.accept()
        print(f"Conexão de {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start_server()
