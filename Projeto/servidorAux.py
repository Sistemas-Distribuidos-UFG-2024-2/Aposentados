import socket
import threading
import json
import os
import time
import asyncio
from datetime import datetime

MIDDLEWARE_IP = "127.0.0.1"
MIDDLEWARE_REGISTRATION_PORT = 9000 # Porta do Serviço de Nomes

# Arquivo de registros
REGISTRY_FILE = "registrosServidorAUX.json"

LISTA_SERVIDORES_REGISTRADORES = [
    ("localhost", 5005),
    ("localhost", 5006),  # Lista de outros servidores registradores que possuem um arquivo de registro.
    ("localhost", 5011)
]

# Critérios de aposentadoria
IDADE_MINIMA = 60  # Idade mínima para aposentadoria
TEMPO_CONTRIBUICAO_MINIMO = 35  # Tempo mínimo de contribuição em anos

# Registro no middleware
async def register_with_middleware(service_name, server_ip, server_port, retry_interval=5, max_retries=None):
    """
    Registra o servidor no middleware com retentativas automáticas.

    Args:
        service_name (str): Nome do serviço a ser registrado.
        server_ip (str): IP do servidor.
        server_port (int): Porta do servidor.
        retry_interval (int): Intervalo em segundos entre as tentativas. Padrão é 5 segundos.
        max_retries (int, optional): Número máximo de tentativas. None para tentativas infinitas.
    """
    retries = 0

    while max_retries is None or retries < max_retries:
        try:
            reader, writer = await asyncio.open_connection(MIDDLEWARE_IP, MIDDLEWARE_REGISTRATION_PORT)

            # Dados do servidor a serem registrados
            request = {
                "service_name": service_name,
                "server_ip": server_ip,
                "server_port": server_port
            }

            # Envia os dados de registro
            writer.write(json.dumps(request).encode())
            await writer.drain()

            # Lê a resposta do middleware
            response = await reader.read(1024)
            print(f"Resposta do middleware: {response.decode()}")

            writer.close()
            await writer.wait_closed()

            print("Registro no middleware concluído com sucesso.")
            return  # Sai da função após o sucesso

        except Exception as e:
            retries += 1
            print(f"Erro ao registrar no middleware: {e}. Tentativa {retries}. Retentando em {retry_interval} segundos...")
            await asyncio.sleep(retry_interval)

    print("Número máximo de tentativas atingido. Falha ao registrar no middleware.")

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

def verificar_aposentadoria(funcionario):
    idade = int(funcionario.get("idade", 0))
    tempo_trabalhado = int(funcionario.get("tempoDeTrabalho"))

    if idade >= IDADE_MINIMA and tempo_trabalhado >= TEMPO_CONTRIBUICAO_MINIMO:
        return "O usuario pode se aposentar."
    elif idade < IDADE_MINIMA:
        return f"O usuario nao atingiu a idade minima de {IDADE_MINIMA} anos."
    else:
        return f"O usuario nao possui o tempo de contribuicao minimo de {TEMPO_CONTRIBUICAO_MINIMO} anos."

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

                if operation == "PESQUISAR_FUNCIONARIO":
                    cpf_solicitado = funcionario.get("cpf")
                    funcionario_encontrado = next(
                        (func for func in registro.values() if func["cpf"] == cpf_solicitado), 
                        None
                    )

                    if funcionario_encontrado:
                        mensagem = verificar_aposentadoria(funcionario_encontrado)
                        resposta = {
                            "Nome": funcionario_encontrado.get("nome"),
                            "CPF": cpf_solicitado,
                            "Mensagem": mensagem
                        }
                        conn.send(json.dumps(resposta).encode())
                    else:
                        conn.send("Nenhum funcionario encontrado para este CPF".encode())

                elif operation == "CADASTRAR_FUNCIONARIO":

                    conn.send("SERVIDOR AUXILIAR, NÃO POSSUI AUTORIDADE PARA ESCRITA.")
                    print("SERVIDOR AUXILIAR, NÃO POSSUI AUTORIDADE PARA ESCRITA.")

                elif operation == "ENVIAR_REGISTRO":
                    conn.send(json.dumps(registro).encode())

                elif operation == "ORDEM_DE_ATUALIZACAO":
                    novo_registro = request.get("registro")
                    if novo_registro and novo_registro != registro:
                        registro = merge_registros(registro, novo_registro)
                        save_registry()
                        print(f"Registro atualizado do servidor {addr}")
                    conn.send("REGISTRO_ATUALIZADO".encode())

                else:
                    conn.send("OPERACAO_DESCONHECIDA".encode())

            except json.JSONDecodeError:
                conn.send("FORMATO_INVALIDO".encode())

        except Exception as e:
            print(f"Erro: {e}")
            break

    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5010))
    server.listen()
    print("Servidor iniciado em localhost:5010")

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

def Propagar():
    """
    Envia o registro atual para todos os servidores na LISTA_SERVIDORES_REGISTRADORES.
    """
    global registro

    for ip, port in LISTA_SERVIDORES_REGISTRADORES:
        try:
            # Conecta ao outro servidor
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))

                # Prepara a mensagem para enviar o registro
                mensagem = {
                    "operation": "ORDEM_DE_ATUALIZACAO",
                    "registro": registro
                }

                # Envia a mensagem
                sock.send(json.dumps(mensagem).encode())
                print(f"Registro enviado para o servidor {ip}:{port}")

                # Recebe a resposta
                resposta = sock.recv(4096).decode()
                if resposta == "REGISTRO_ATUALIZADO":
                    print(f"Servidor {ip}:{port} confirmou a PROPAGACAO do registro.")
                else:
                    print(f"Resposta inesperada do servidor {ip}:{port}: {resposta}")

        except Exception as e:
            print(f"Erro ao conectar ou enviar registro para o servidor {ip}:{port} - {e}")


# Inicia o servidor e a verificação 
if __name__ == "__main__":
    service_name = "servidorAux"
    server_ip = "127.0.0.1"
    server_port = 5010
    
    asyncio.run(register_with_middleware(service_name, server_ip, server_port))
    
    # Inicia o servidor em uma thread separada
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    
    # Inicia a verificação  com todos os servidores
    check_thread = threading.Thread(target=checagem_temporaria)
    check_thread.daemon = True  # Torna a thread um daemon, ou seja, termina quando o processo principal encerrar
    check_thread.start()
