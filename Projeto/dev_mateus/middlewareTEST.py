import asyncio

async def request_healthy_servers(service_name):
    # Configurações do serviço de descoberta
    discovery_ip = '127.0.0.1'
    discovery_port = 9010

    reader, writer = await asyncio.open_connection(discovery_ip, discovery_port)

    # Envia o nome do serviço para o serviço de descoberta
    writer.write(service_name.encode())
    await writer.drain()

    # Recebe a resposta do serviço de descoberta
    data = await reader.read(1024)
    healthy_servers = data.decode()

    print(f'Servidores saudáveis para o serviço "{service_name}": {healthy_servers}')

    # Fecha a conexão
    writer.close()
    await writer.wait_closed()

async def main():
    service_name = "servidor_principal"  # Nome do serviço que queremos consultar
    await request_healthy_servers(service_name)

if __name__ == '__main__':
    asyncio.run(main())
