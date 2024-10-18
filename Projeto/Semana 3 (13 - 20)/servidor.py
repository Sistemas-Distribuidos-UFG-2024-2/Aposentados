import asyncio
import json

async def handle_connection(reader, writer):
    print("Servidor conectado, aguardando dados do middleware...")

    # Lendo os dados do middleware
    data = await reader.read(1024)
    if data:
        # Decodificando os dados do funcionário
        funcionario_json = data.decode()
        funcionario = json.loads(funcionario_json)
        print(f"Dados do funcionário recebidos: {funcionario}")

        # Processar os dados do funcionário (por exemplo, calcular bônus)
        bonus = funcionario['salario'] * 0.1
        resposta = f"Funcionário: {funcionario['nome']}, Bônus calculado: {bonus}"

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
