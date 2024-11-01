import asyncio
from os import write

# Lista de servidores para cada serviço
service_names = {
    "servidor_principal": [("127.0.0.1", 9001), ("127.0.0.1", 9002)],
    "servidor_backup": [("127.0.0.1", 9003)]
}

HEARTBEAT_INTERVAL = 3
MAX_FAILURES = 3

server_status = {}

status_lock = asyncio.Lock()

async def check_server_health():
    while True:
        async with status_lock:
            for service, servers in service_names.items():
                for ip, port in servers:
                    server_failures = 0

                    while server_failures < MAX_FAILURES:
                        try:
                            reader, writer = await asyncio.open_connection(ip, port)

                            server_status[(ip, port)] = True
                            writer.close()
                            await writer.wait_closed()

                            break
                        except:
                            if server_failures >= 2:
                                server_status[(ip,port)] = False
                            server_failures+=1
        await asyncio.sleep(HEARTBEAT_INTERVAL)

async def handle_connection(reader, writer):
    data = await reader.read(1024)
    service_name = data.decode().strip()

    async with status_lock:
        if service_name in service_names:
            healthy_servers = [
                addr for addr in service_names[service_name] if server_status.get(addr)
            ]
            response = str(healthy_servers).encode()
        else:
            response = b"[]"

    writer.write(response)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    asyncio.create_task(check_server_health())

    server_descoberta = await asyncio.start_server(handle_connection, '127.0.0.1', 9010)  # Rodando em 9010
    addr = server_descoberta.sockets[0].getsockname()
    print(f'Serviço de DESCOBERTA rodando em {addr}')

    async with server_descoberta:
        await server_descoberta.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
