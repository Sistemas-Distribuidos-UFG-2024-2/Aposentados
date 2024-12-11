# server_health_server.py

import asyncio
import json

server_failures = {}
MAX_FAILURES = 3
COOL_DOWN = 60  # Segundos para cooldown

async def checar_saude_servidor(server_ip, server_port):
    server = (server_ip, server_port)
    if server_failures.get(server, 0) >= MAX_FAILURES:
        print(f"Servidor {server_ip}:{server_port} em cooldown.")
        await asyncio.sleep(COOL_DOWN)
        server_failures[server] = 0

    try:
        reader, writer = await asyncio.open_connection(server_ip, server_port)
        writer.close()
        await writer.wait_closed()
        server_failures[server] = 0
        return {"status": "ok"}
    except Exception as e:
        print(f"Servidor {server_ip}:{server_port} indisponível - {e}")
        server_failures[server] = server_failures.get(server, 0) + 1
        return {"status": "unavailable", "error": str(e)}

async def handle_client(reader, writer):
    try:
        data = await reader.read(1024)
        request = json.loads(data.decode())

        server_ip = request.get("server_ip")
        server_port = request.get("server_port")
        if not server_ip or not server_port:
            response = {"error": "Parâmetros inválidos"}
        else:
            response = await checar_saude_servidor(server_ip, server_port)

        writer.write(json.dumps(response).encode())
        await writer.drain()
    except Exception as e:
        writer.write(json.dumps({"error": str(e)}).encode())
        await writer.drain()
    finally:
        writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 9090)
    print("Servidor de saúde rodando em 0.0.0.0:9090")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
