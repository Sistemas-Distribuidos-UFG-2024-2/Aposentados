import asyncio
import json

# Lista de servidores para cada serviço
service_names = {
    "servidor_principal": [("127.0.0.1", 9001), ("127.0.0.1", 9002)],
    "servidor_backup": [("127.0.0.1", 9003)]
}

server_failures = {}
MAX_FAILURES = 3
COOL_DOWN = 60  # Segundos para cooldown
current_server_index = {}

for service, servers in service_names.items():
    current_server_index[service] = 0
    for server in servers:
        server_failures[server] = 0

async def check_server_health(server_ip, server_port):
    server = (server_ip, server_port)
    if server_failures[server] >= MAX_FAILURES:
        print(f"Servidor {server_ip}:{server_port} em cooldown.")
        await asyncio.sleep(COOL_DOWN)
        server_failures[server] = 0

    try:
        reader, writer = await asyncio.open_connection(server_ip, server_port)
        writer.close()
        await writer.wait_closed()
        server_failures[server] = 0
        return True
    except Exception as e:
        print(f"Servidor {server_ip}:{server_port} indisponível - {e}")
        server_failures[server] += 1
        return False

async def get_next_server(service_name):
    if service_name not in service_names:
        print(f"Serviço '{service_name}' não encontrado.")
        return None, None

    servers = service_names[service_name]
    servers_checked = 0

    while servers_checked < len(servers):
        server_ip, server_port = servers[current_server_index[service_name]]
        current_server_index[service_name] = (current_server_index[service_name] + 1) % len(servers)
        servers_checked += 1

        if await check_server_health(server_ip, server_port):
            return server_ip, server_port

    return None, None

async def handle_client(reader, writer):
    print("Conexão recebida")

    # Recebendo o nome do serviço solicitado
    data = await reader.read(1024)
    service_name = data.decode().strip()

    server_ip, server_port = await get_next_server(service_name)

    if server_ip is None:
        writer.write("Nenhum servidor disponível para o serviço solicitado.\n".encode())
        await writer.drain()
        writer.close()
        return

    try:
        server_reader, server_writer = await asyncio.open_connection(server_ip, server_port)
        print(f"Conectado ao servidor {server_ip}:{server_port}")

        while True:
            data = await reader.read(1024)
            if not data:
                break
            server_writer.write(data)
            await server_writer.drain()

            response = await server_reader.read(1024)
            if response:
                writer.write(response)
                await writer.drain()
    except Exception as e:
        print(f"Erro ao conectar ao servidor {server_ip}:{server_port} - {e}")
        writer.write("Erro ao se comunicar com o servidor.\n".encode())
        await writer.drain()
    finally:
        writer.close()
        if 'server_writer' in locals():
            server_writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8080)
    addr = server.sockets[0].getsockname()
    print(f'Middleware rodando em {addr}')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
