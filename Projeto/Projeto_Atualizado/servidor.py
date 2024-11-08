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
        funcionario_json = data.decode()
        funcionario = json.loads(funcionario_json)
        print(f"Dados do funcionário recebidos: {funcionario}")

        # Verificando se o funcionário é válido com o ServidorRegistrador
        usuario_valido = await checagem_usuario(funcionario)

        if usuario_valido:
            print("USUÁRIO VALIDO !!!")
            situacao = verificar_aposentadoria(int(funcionario['idade']), int(funcionario['tempoDeTrabalho']), funcionario['cpf'])
            resposta = f"Funcionário: {funcionario['nome']}, Situação: {situacao}"
        else:
            resposta = "Funcionário inválido"

        # Enviando a resposta de volta ao middleware
        writer.write(resposta.encode())
        await writer.drain()

    print("Fechando a conexão com o middleware...")
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_connection, '127.0.0.1', 9001)  # Rodando em 9001
    addr = server.sockets[0].getsockname()
    print(f'Servidor rodando em {addr}')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
