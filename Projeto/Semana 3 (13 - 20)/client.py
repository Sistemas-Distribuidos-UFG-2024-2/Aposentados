import asyncio
import json

# Dados do funcionário que serão enviados
funcionario = {
    "nome": "Joao Silva",
    "cargo": "Desenvolvedor",
    "salario": 5000
}

async def tcp_client(funcionario):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8080)  # Conectar ao middleware

    # Serializando os dados do funcionário em JSON
    funcionario_json = json.dumps(funcionario)
    print(f'Enviando: {funcionario_json}')
    
    # Enviando os dados para o middleware
    writer.write(funcionario_json.encode())
    await writer.drain()

    # Recebendo a resposta do middleware (ou servidor final)
    data = await reader.read(1024)
    print(f'Resposta recebida: {data.decode()}')

    print('Fechando a conexão...')
    writer.close()
    await writer.wait_closed()

if __name__ == '__main__':
    asyncio.run(tcp_client(funcionario))
