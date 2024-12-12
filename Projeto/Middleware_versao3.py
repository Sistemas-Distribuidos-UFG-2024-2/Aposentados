# middleware.py

import asyncio
import json

NOME_SERVICE_IP = "127.0.0.1"
NOME_SERVICE_PORT_REGISTER = 9000 
NOME_SERVICE_PORT_QUERY = 9001  

async def register_with_name_service(service_name, server_ip, server_port):
    try:
        reader, writer = await asyncio.open_connection(NOME_SERVICE_IP, NOME_SERVICE_PORT_REGISTER)
        request = {"service_name": service_name, "server_ip": server_ip, "server_port": server_port}
        writer.write(json.dumps(request).encode())
        await writer.drain()

        response = await reader.read(1024)
        print(f"Resposta do Serviço de Nomes: {response.decode()}")

        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"Erro ao registrar no Serviço de Nomes: {e}")

async def query_name_service(service_name):
    try:
        reader, writer = await asyncio.open_connection(NOME_SERVICE_IP, NOME_SERVICE_PORT_QUERY)
        request = {"service_name": service_name}
        writer.write(json.dumps(request).encode())
        await writer.drain()

        response_data = await reader.read(1024)
        response = json.loads(response_data.decode())

        writer.close()
        await writer.wait_closed()

        if "servers" in response:
            return response["servers"]
        else:
            print(f"Erro ao consultar Serviço de Nomes: {response.get('error')}")
            return []
    except Exception as e:
        print(f"Erro ao conectar ao Serviço de Nomes: {e}")
        return []

#current_server_index = {}

#for service, servers in service_names.items():
#    current_server_index[service] = 0

async def check_server_health_remote(server_ip, server_port):
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 9090)  # IP e porta do servidor de saúde

        request = {"server_ip": server_ip, "server_port": server_port}
        writer.write(json.dumps(request).encode())
        await writer.drain()

        response_data = await reader.read(1024)
        response = json.loads(response_data.decode())

        writer.close()
        await writer.wait_closed()

        if response.get("status") == "ok":
            return True
        else:
            print(f"Falha ao verificar saúde do servidor: {response.get('error')}")
            return False
    except Exception as e:
        print(f"Erro ao conectar ao servidor de saúde: {e}")
        return False

async def get_next_server_remote(service_name):
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 9091)  # IP e porta do servidor de seleção

        request = {"service_name": service_name}
        writer.write(json.dumps(request).encode())
        await writer.drain()

        response_data = await reader.read(1024)
        response = json.loads(response_data.decode())

        writer.close()
        await writer.wait_closed()

        if "server_ip" in response and "server_port" in response:
            return response["server_ip"], response["server_port"]
        else:
            print(f"Erro ao obter próximo servidor: {response.get('error')}")
            return None, None
    except Exception as e:
        print(f"Erro ao conectar ao servidor de seleção: {e}")
        return None, None

# Outras partes do middleware permanecem iguais...
async def handle_client(reader, writer):
    print("Conexão recebida")

    # Recebendo o nome do serviço solicitado
    data = await reader.read(1024)
    service_name = data.decode().strip()

    server_ip, server_port = await get_next_server_remote(service_name)

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
    print(f'Middleware rodando em 0.0.0.0:8080')

    async with server:
        await server.serve_forever()
        
if __name__ == '__main__':
    asyncio.run(main())
