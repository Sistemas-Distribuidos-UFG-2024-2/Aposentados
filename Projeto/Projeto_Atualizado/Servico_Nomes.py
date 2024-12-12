# Servico_Nomes.py
import asyncio
import json

# Dicionário para armazenar os endereços dos serviços registrados
service_registry = {}

async def register_service(reader, writer):
    global service_registry
    try:
        # Recebe dados de registro
        data = await reader.read(1024)
        request = json.loads(data.decode())

        service_name = request.get("service_name")
        server_ip = request.get("server_ip")
        server_port = request.get("server_port")

        if not service_name or not server_ip or not server_port:
            writer.write("Dados de registro inválidos.\n".encode())
            await writer.drain()
            return

        # Adiciona ou atualiza o registro do serviço
        if service_name not in service_registry:
            service_registry[service_name] = []

        if (server_ip, server_port) not in service_registry[service_name]:
            service_registry[service_name].append((server_ip, server_port))
            print(f"Registrado: {service_name} -> {server_ip}:{server_port}")
            writer.write("Registro no Serviço de Nomes bem sucedido.\n".encode())
        else:
            writer.write("Servidor já registrado.\n".encode())

        await writer.drain()
    except Exception as e:
        print(f"Erro no registro: {e}")
        writer.write("Erro ao registrar serviço.\n".encode())
    finally:
        writer.close()

async def get_service(reader, writer):
    try:
        # Recebe o nome do serviço solicitado
        data = await reader.read(1024)
        request = json.loads(data.decode())
        service_name = request.get("service_name")

        if not service_name or service_name not in service_registry:
            writer.write(json.dumps({"error": "Serviço não encontrado"}).encode())
            await writer.drain()
            return

        # Retorna a lista de servidores do serviço solicitado
        writer.write(json.dumps({"servers": service_registry[service_name]}).encode())
        await writer.drain()
    except Exception as e:
        print(f"Erro ao consultar serviço: {e}")
        writer.write("Erro ao processar consulta.\n".encode())
    finally:
        writer.close()

async def main():
    # Porta de registro e consulta
    registration_server = await asyncio.start_server(register_service, '0.0.0.0', 9000)
    query_server = await asyncio.start_server(get_service, '0.0.0.0', 9001)

    print("Serviço de Nomes rodando nas portas 9000 (registro) e 9001 (consulta)")
    async with registration_server, query_server:
        await asyncio.gather(registration_server.serve_forever(), query_server.serve_forever())

if __name__ == '__main__':
    asyncio.run(main())
