# loadbalancer.py

import asyncio
import json

# Mantém o índice atual para Round Robin
current_server_index = {}

async def handle_client(reader, writer):
    try:
        data = await reader.read(1024)
        request = json.loads(data.decode())

        action = request.get("action")
        service_name = request.get("service_name")
        healthy_servers = request.get("healthy_servers")

        if action == "get_next_server" and service_name and healthy_servers is not None:
            response = await get_next_server(service_name, healthy_servers)
        else:
            response = {"error": "Dados inválidos ou ação desconhecida."}

        writer.write(json.dumps(response).encode())
        await writer.drain()
    except Exception as e:
        writer.write(json.dumps({"error": str(e)}).encode())
        await writer.drain()
    finally:
        writer.close()

async def get_next_server(service_name, healthy_servers):
    if not healthy_servers:
        return {"error": "Nenhum servidor saudável disponível."}

    # Inicializa o índice de Round Robin para o serviço, se necessário
    if service_name not in current_server_index:
        current_server_index[service_name] = 0

    # Ajusta o índice se a lista de servidores mudou
    if current_server_index[service_name] >= len(healthy_servers):
        current_server_index[service_name] = 0

    # Aplica o Round Robin para escolher o servidor
    server_ip, server_port = healthy_servers[current_server_index[service_name]]
    current_server_index[service_name] = (current_server_index[service_name] + 1) % len(healthy_servers)

    return {"server_ip": server_ip, "server_port": server_port}

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 9091)  # Porta 9091
    print("Load Balancer rodando em 0.0.0.0:9091")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
