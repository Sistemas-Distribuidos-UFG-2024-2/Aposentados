import asyncio

service_names = {
    "servidor_principal": [("127.0.0.1", 9001), ("127.0.0.1", 9002)],
    "servidor_backup": [("127.0.0.1", 9003)]
}

connects = {}

async def check_service_exists(service_name):
    # Verifica se o servico existe na listagem de serviços
    if service_name not in service_names:
        print(f"Serviço '{service_name}' não encontrado.")
        return None, None

    servers = service_names[service_name]
    servers_checked = 0

    while servers_checked < len(servers):
        server_ip, server_port = servers[connects[service_name]]
        connects[service_name] = (connects[service_name] + 1) % len(servers)
        servers_checked += 1

        if await check_server_health(server_ip, server_port):
            return server_ip, server_port

    return None, None

async def handle_connection(reader, writer):
    # data = await reader.read(1024)
    # service_name = data.decode().strip()

async def main():
    server = await asyncio.start_server(handle_connection, '127.0.0.1', 9010)  # Rodando em 9010
    addr = server.sockets[0].getsockname()
    print(f'Serviço de Health Check rodando em {addr}')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
