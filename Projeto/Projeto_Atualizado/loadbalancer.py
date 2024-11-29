# testar_conexao.py

import asyncio
import json

service_names = {
    "servidor_principal": [("127.0.0.1", 9001), ("127.0.0.1", 9002)],
    "servidor_backup": [("127.0.0.1", 9003)],
    "servidor_registrador": [("127.0.0.1", 5005), ("127.0.0.1", 5006)]
}

current_server_index = {service: 0 for service in service_names}

async def testar_conexao(server_ip, server_port):
    try:
        reader, writer = await asyncio.open_connection(server_ip, server_port)
        writer.close()
        await writer.wait_closed()
        return True
    except Exception:
        return False

async def obter_outro_server(service_name):
    if service_name not in service_names:
        return {"error": f"Serviço '{service_name}' não encontrado."}

    servers = service_names[service_name]
    servers_checked = 0

    while servers_checked < len(servers):
        server_ip, server_port = servers[current_server_index[service_name]]
        current_server_index[service_name] = (current_server_index[service_name] + 1) % len(servers)
        servers_checked += 1

        if await testar_conexao(server_ip, server_port):
            return {"server_ip": server_ip, "server_port": server_port}

    return {"error": "Nenhum servidor disponível."}

async def handle_client(reader, writer):
    try:
        data = await reader.read(1024)
        request = json.loads(data.decode())

        service_name = request.get("service_name")
        if not service_name:
            response = {"error": "Parâmetro 'service_name' ausente."}
        else:
            response = await obter_outro_server(service_name)

        writer.write(json.dumps(response).encode())
        await writer.drain()
    except Exception as e:
        writer.write(json.dumps({"error": str(e)}).encode())
        await writer.drain()
    finally:
        writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 9091)  # Porta 9091
    print("Servidor de seleção rodando em 0.0.0.0:9091")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())

