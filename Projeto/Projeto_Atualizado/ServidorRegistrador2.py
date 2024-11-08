import socket
import threading
import json
import os
import time
from datetime import datetime


# Arquivo de registros
REGISTRY_FILE = "registrosServidor2.json"

LISTA_SERVIDORES_REGISTRADORES = [
    ("localhost", 5005)  # Lista de outros servidores registradores que possuem um arquivo de registro.
]

# Carrega os registros existentes, se houver
def load_registry():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    return {}

# Salva os registros no arquivo
def save_registry():
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registro, f, indent=4)

# Função que executa a verificação de registros a cada 60 segundos
def checagem_temporaria(interval=60):
    while True:
        for ip, port in LISTA_SERVIDORES_REGISTRADORES:
            checagem_de_registro(ip, port)
        time.sleep(interval)


def merge_registros(registro1, registro2):
    # Converte registros em listas de funcionários com identificadores
    funcionarios = []
    
    # Adiciona funcionários do primeiro registro (registro1)
    for id, dados in registro1.items():
        dados["id"] = id
        dados["data_hora_cadastro"] = datetime.strptime(dados["data_hora_cadastro"], "%Y-%m-%d %H:%M:%S")
        funcionarios.append(dados)
    
    # Adiciona funcionários do segundo registro (registro2)
    for id, dados in registro2.items():
        dados["id"] = id
        dados["data_hora_cadastro"] = datetime.strptime(dados["data_hora_cadastro"], "%Y-%m-%d %H:%M:%S")
        
        # Verifica se o funcionário já existe em registro1
        existente = next((func for func in funcionarios if func["id"] == id), None)
        
        if existente:
            # Se existe, mantém o registro com a data mais antiga
            if dados["data_hora_cadastro"] < existente["data_hora_cadastro"]:
                funcionarios.remove(existente)
                funcionarios.append(dados)
        else:
            # Caso contrário, adiciona como um novo funcionário
            funcionarios.append(dados)
    
    # Ordena a lista de funcionários pela data e hora de cadastro
    funcionarios.sort(key=lambda x: x["data_hora_cadastro"])
    
    # Converte novamente a data e hora para string e cria o novo registro
    novo_registro = {funcionario.pop("id"): {**funcionario, "data_hora_cadastro": funcionario["data_hora_cadastro"].strftime("%Y-%m-%d %H:%M:%S")} for funcionario in funcionarios}
    
    return novo_registro



# Inicializa a tabela de clientes com os registros salvos
registro = load_registry()

def handle_client(conn, addr):
    global registro
    while True:
        try:
            # Recebe a mensagem do cliente
            message = conn.recv(4096).decode()
            if not message:
                break
            
            try:
                # Tenta carregar a mensagem como JSON
                request = json.loads(message)
                operation = request.get("operation")  # Operação desejada
                funcionario = request.get("funcionario")  # Dados do funcionário

                # Verifica qual operação foi solicitada
                if operation == "CADASTRAR_FUNCIONARIO":

                    if funcionario:
                        # Verifica se o CPF do funcionário já existe
                        cpf_existente = any(func["cpf"] == funcionario["cpf"] for func in registro.values())
                        
                        if cpf_existente:
                            conn.send("Valido".encode())
                        else:
                            # Define o identificador do funcionário automaticamente
                            identifier = f"Aposentado{len(registro) + 1}"
                            
                            # Adiciona a data e hora do cadastro
                            funcionario["data_hora_cadastro"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            # Armazena o funcionário no dicionário registro com o identificador automático
                            registro[identifier] = funcionario
                            save_registry()
                            
                            conn.send(f"{identifier}_CADASTRADO".encode())
                    else:
                        conn.send("DADOS_FUNCIONARIO_INVALIDOS".encode())
                
                elif operation == "PESQUISAR_FUNCIONARIO":

                    if funcionario:
                        # Verifica se o CPF do funcionário já existe
                        cpf_existente = any(func["cpf"] == funcionario["cpf"] for func in registro.values())
                        
                        if cpf_existente:
                            conn.send("Valido".encode())
                        else:
                            conn.send("NÃO_ENCONTRADO".encode())
                    else:
                        conn.send("DADOS_FUNCIONARIO_INVALIDOS".encode())

                elif operation == "ENVIAR_REGISTRO":

                    # Envia o conteúdo do arquivo de registros como JSON
                    conn.send(json.dumps(registro).encode())
                
                elif operation == "REGISTROS_IGUAIS":
                    print(f"Registros Iguais entre esse servidor e o {addr}")

                elif operation == "ORDEM_DE_ATUALIZACAO":
                    
                    # Substitui o registro atual pelo novo registro recebido somente se forem diferentes

                    novo_registro = request.get("registro")
                    if novo_registro:

                        # Verifica se os registros são diferentes antes de atualizar
                        if novo_registro != registro:
                            registro = novo_registro
                            save_registry()
                            print(f"Registro atualizado com sucesso a partir da ordem de atualização do servidor {addr}")
                        else:
                            print(f"Registro não atualizado, pois já está sincronizado com o servidor {addr}")

                    else:
                        conn.send("DADOS_REGISTRO_INVALIDOS".encode())
                
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
    server.bind(("localhost", 5006))
    server.listen()
    print("Servidor iniciado em localhost:5006")

    while True:
        conn, addr = server.accept()
        print(f"Conexão de {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


# Função para verificar registros entre servidores
def checagem_de_registro(IP, Porta):
    global registro
    try:
        # Conecta ao outro servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((IP, Porta))
            
            # Solicita o conteúdo do registro
            request = {"operation": "ENVIAR_REGISTRO"}
            sock.send(json.dumps(request).encode())

            # Recebe a resposta
            response = sock.recv(4096).decode()
            OUTRO_registro = json.loads(response)

            # Verifica se os registros são iguais
            if registro == OUTRO_registro:

                mensagem = {"operation": "REGISTROS_IGUAIS"}
                sock.send(json.dumps(mensagem).encode())
                print(f"Registros são iguais com o servidor {IP}:{Porta}. Confirmado.")

            else:
                print("Os arquivos de registro são diferentes.")
                registro = merge_registros(registro, OUTRO_registro)
                save_registry()

                mensagem = {
                    "operation": "ORDEM_DE_ATUALIZACAO",
                    "registro": registro
                }

                sock.send(json.dumps(mensagem).encode())
                print(f"Registro atualizado enviado ao servidor {IP}:{Porta}.")

    except Exception as e:
        print(f"Erro ao conectar ao servidor {IP}:{Porta} - {e}")



# Inicia o servidor e a verificação 
if __name__ == "__main__":
    # Inicia o servidor em uma thread separada
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    
    # Inicia a verificação  com todos os servidores
    check_thread = threading.Thread(target=checagem_temporaria)
    check_thread.daemon = True  # Torna a thread um daemon, ou seja, termina quando o processo principal encerrar
    check_thread.start()