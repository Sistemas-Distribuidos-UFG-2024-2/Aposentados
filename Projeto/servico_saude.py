# servico_saude.py
import asyncio
import json

SERVERS = [("127.0.0.1", 5005), ("127.0.0.1", 5006)]  # Lista inicial de servidores

async def check_server_health(server_ip, server_port):
    # Simulação de checagem de saúde (implementação real pode variar)
    try:
        reader, writer = await asyncio.open_connection(server_ip, server_port)
        writer.close()
        await writer.wait_closed()
        return True
    except Exception:
        return False

async def get_healthy_servers():
    healthy_servers = []
    for ip, port in SERVERS:
        is_healthy = await check_server_health(ip, port)
        if is_healthy:
            healthy_servers.append((ip, port))
    return healthy_servers

async def handle_health_check_request(reader, writer):
    healthy_servers = await get_healthy_servers()
    response = json.dumps({"servers": healthy_servers})
    writer.write(response.encode())
    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(handle_health_check_request, '0.0.0.0', 9090)
    print("Serviço de Saúde rodando em 0.0.0.0:9090")
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
