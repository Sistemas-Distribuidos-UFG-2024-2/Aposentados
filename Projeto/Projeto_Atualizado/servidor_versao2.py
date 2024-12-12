import asyncio
import json

def verificar_aposentadoria(idade, tempo_servico, cpf):
    if idade >= 65 and tempo_servico >= 30:
        print(f"Funcionário {cpf}: Pode se aposentar.")
        return 'APOSENTADO !!'
    elif idade >= 60 and tempo_servico >= 25:
        print(f"Funcionário {cpf}: Pode se aposentar.")
        return 'APOSENTADO !!'
    else:
        print(f"Funcionário {cpf}: Ainda não pode se aposentar.")
        return 'Não Aposentado'
    
def calcular_valor_aposentadoria(media_salarial, tempo_contribuicao):
    # Fórmula: 
    # 1. O valor base é 60% da média salarial.
    # 2. Cada ano além de 20 anos de contribuição aumenta 2% no valor.
    # 3. O valor máximo é 100% da média salarial.
    base = 0.6 * media_salarial
    adicional = max(0, tempo_contribuicao - 20) * 0.02 * media_salarial
    valor_final = min(base + adicional, media_salarial)
    return valor_final

MIDDLEWARE_IP = "localhost"
MIDDLEWARE_REGISTRATION_PORT = 8081

async def register_with_middleware(service_name, server_ip, server_port):
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

    except Exception as e:
        print(f"Erro ao registrar no middleware: {e}")

async def checagem_usuario(funcionario):
    reader, writer = await asyncio.open_connection('127.0.0.1', 5005)  # Conectando ao servidor registrador

    # Enviando dados do funcionário para o servidor de validação
    request = {
        "operation": "CADASTRAR_FUNCIONARIO",  # OPERAÇÃO QUE O SERVIDOR REGISTRADOR VAI REALIZAR
        "funcionario": funcionario
    }
    
    request = json.dumps(request)
    writer.write(request.encode())
    await writer.drain()

    # Recebendo a resposta do servidor de validação
    resposta = await reader.read(1024)
    resposta_decodificada = resposta.decode()
    
    # Fechando a conexão com o servidor de validação
    writer.close()
    await writer.wait_closed()

    # Retorna True se o servidor de validação indicar que o usuário é válido
    return resposta_decodificada == "Valido" # Isso deve ser diferente, considerando que o servidor irá enviar multiplas respostas.

        
async def handle_connection(reader, writer):
    print("Servidor conectado, aguardando dados do middleware...")

    while True:
        # Lendo os dados do middleware
        data = await reader.read(1024)
        if not data:
            break  # Encerra o loop se não houver mais dados (middleware fechou a conexão)

        # Decodificando os dados do funcionário
        request_json = data.decode()
        request = json.loads(request_json)
        operation = request.get("operation")
        funcionario = request.get("funcionario")
        
        print(f"Operação recebida: {operation}")
        print(f"Dados do funcionário: {funcionario}")

        if operation == "SIMULAR_APOSENTADORIA":
            # Extrair dados necessários
            media_salarial = funcionario.get("media_salarial")
            tempo_contribuicao = funcionario.get("tempo_de_contribuicao")

            if media_salarial is None or tempo_contribuicao is None:
                resposta = json.dumps({"success": False, "error": "Dados insuficientes para simular aposentadoria"})
            else:
                # Calcular valor da aposentadoria
                valor = calcular_valor_aposentadoria(media_salarial, tempo_contribuicao)
                resposta = json.dumps({"success": True, "valor_aposentadoria": valor})
        
        elif operation == "VERIFICAR_APOSENTADORIA":
            # Verificar se o funcionário pode se aposentar
            usuario_valido = await checagem_usuario(funcionario)
            if usuario_valido:
                print("USUÁRIO VALIDO !!!")
                situacao = verificar_aposentadoria(int(funcionario['idade']), int(funcionario['tempoDeTrabalho']), funcionario['cpf'])
                resposta = f"Funcionário: {funcionario['nome']}, Situação: {situacao}"
            else:
                resposta = "Funcionário inválido"

        else:
            resposta = json.dumps({"success": False, "error": "Operação desconhecida"})
        
        # Enviar a resposta para o middleware
        writer.write(resposta.encode())
        await writer.drain()

    print("Fechando a conexão com o middleware...")
    writer.close()
    await writer.wait_closed()

async def main():
    server_ip = '127.0.0.1'
    server_port = 9001  # Porta do servidor
    service_name = "servidor_principal"

    # Registra o servidor no middleware
    await register_with_middleware(service_name, server_ip, server_port)

    # Inicia o servidor principal
    server = await asyncio.start_server(handle_connection, server_ip, server_port)
    addr = server.sockets[0].getsockname()
    print(f'Servidor rodando em {addr}')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
