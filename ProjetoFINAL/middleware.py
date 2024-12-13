# middleware.py
import asyncio
import json

NOME_SERVICE_IP = "127.0.0.1"
NOME_SERVICE_PORT_REGISTER = 9000 
NOME_SERVICE_PORT_QUERY = 9001
SAUDE_SERVICE_PORT = 9090
LOAD_BALANCER_PORT = 9091

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

# Função para obter servidores saudáveis a partir do serviço de saúde
async def update_healthy_servers():
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', SAUDE_SERVICE_PORT)
        writer.write(b"health_check")
        await writer.drain()

        response_data = await reader.read(1024)
        response = json.loads(response_data.decode())
        writer.close()
        await writer.wait_closed()

        if "servers" in response:
            return response["servers"]  # Retorna a lista de servidores saudáveis
        else:
            print("Erro: resposta inesperada do serviço de saúde")
            return []
    except Exception as e:
        print(f"Erro ao conectar ao serviço de saúde: {e}")
        return []

# Função para consultar o load balancer e obter o próximo servidor
async def get_next_server_from_loadbalancer(service_name, healthy_servers):
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', LOAD_BALANCER_PORT)
        request = {
            "action": "get_next_server",
            "service_name": service_name,
            "healthy_servers": healthy_servers
        }
        writer.write(json.dumps(request).encode())
        await writer.drain()

        response_data = await reader.read(1024)
        response = json.loads(response_data.decode())

        writer.close()
        await writer.wait_closed()

        if "server_ip" in response and "server_port" in response:
            return response["server_ip"], response["server_port"]
        else:
            print(f"Erro ao obter próximo servidor do load balancer: {response.get('error')}")
            return None, None
    except Exception as e:
        print(f"Erro ao conectar ao load balancer: {e}")
        return None, None

async def handle_client(reader, writer):
    print("Conexão recebida")

    try:
        # Recebe o nome do serviço solicitado
        data = await reader.read(1024)
        service_name = data.decode().strip()

        # Obtém a lista de servidores saudáveis
        healthy_servers = await update_healthy_servers()

        if not healthy_servers:
            writer.write("Nenhum servidor saudável disponível para o serviço solicitado.\n".encode())
            await writer.drain()
            writer.close()
            return

        # Consulta o load balancer para o próximo servidor
        server_ip, server_port = await get_next_server_from_loadbalancer(service_name, healthy_servers)

        if server_ip is None:
            writer.write("Erro ao obter servidor do load balancer.\n".encode())
            await writer.drain()
            writer.close()
            return

        # Conecta ao servidor selecionado
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
        print(f"Erro: {e}")
        writer.write(f"Erro no middleware: {str(e)}\n".encode())
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
