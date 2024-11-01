import asyncio
import json

# Dados do funcionário que serão enviados
funcionario = {
    "nome": "Joao Silva",
    "idade": "77",
    "tempoDeTrabalho": "60",
    "cargo": "Desenvolvedor",
    "cpf": "123.132.132-77",
    "salario": 5000
}

# Nome do serviço que o cliente quer acessar
service_name = "servidor_principal"  # Nome do serviço a ser passado ao middleware

async def tcp_client(funcionario, service_name, retries=3):
    for attempt in range(retries): # Tentativa de se conectar ao servidor
        try:
            reader, writer = await asyncio.open_connection('127.0.0.1', 8080)  # Conectar ao middleware

            # Enviando o nome do serviço ao middleware
            writer.write(service_name.encode() + b'\n')
            await writer.drain()

            # Serializando os dados do funcionário em JSON
            funcionario_json = json.dumps(funcionario)
            print(f'Enviando: {funcionario_json}')
            
            # Enviando os dados para o middleware
            writer.write(funcionario_json.encode())
            await writer.drain()

            # Recebendo a resposta do middleware (ou servidor final)
            data = await reader.read(1024)

            if data:  # Recebeu a resposta do middleware
                print(f'Resposta recebida: {data.decode()}')
                print('Fechando a conexão...')
                writer.close()
                await writer.wait_closed()
                break

        except Exception as e:
            print(e)
            if attempt < retries - 1:
                await asyncio.sleep(10)  # Espera antes de tentar novamente
            else:
                print(f"Falha ao conectar após {retries} tentativas.")

if __name__ == '__main__':
    asyncio.run(tcp_client(funcionario, service_name))
