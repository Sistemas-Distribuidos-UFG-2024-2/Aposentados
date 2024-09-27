import asyncio
import socket
import time

# Lista de servidores para verificar
servers = [("127.0.0.1", 9001), ("127.0.0.1", 9002)]  # Servidores do sistema distribuído


async def check_server_health(server_ip, server_port):
    """Função para verificar se o servidor está ativo e disponível."""
    try:
        # Tentar abrir uma conexão com o servidor
        reader, writer = await asyncio.open_connection(server_ip, server_port)

        # Enviar uma pequena mensagem para verificar a resposta do servidor
        writer.write(b"STATUS_CHECK")
        await writer.drain()

        # Ler a resposta
        response = await reader.read(100)
        if response:
            print(f"Servidor {server_ip}:{server_port} está online.")
        else:
            print(f"Servidor {server_ip}:{server_port} não respondeu corretamente.")

        # Fechar a conexão
        writer.close()
        await writer.wait_closed()
        return True
    except Exception as e:
        print(f"Falha ao conectar com o servidor {server_ip}:{server_port}: {e}")
        return False


async def verify_servers():
    """Função principal que verifica todos os servidores periodicamente."""
    while True:
        print("\n=== Iniciando verificação de servidores ===")
        for server_ip, server_port in servers:
            # Verificar a disponibilidade de cada servidor na lista
            result = await check_server_health(server_ip, server_port)
            if result:
                print(f"Servidor {server_ip}:{server_port} está ativo.")
            else:
                print(f"Servidor {server_ip}:{server_port} está offline ou inacessível.")

        print("=== Verificação completa. Próxima verificação em 10 segundos ===\n")
        # Esperar 10 segundos antes de verificar novamente
        await asyncio.sleep(10)


async def handle_client(reader, writer):
    """Lidar com solicitações de verificação de outros componentes."""
    data = await reader.read(100)
    message = data.decode().strip()
    addr = writer.get_extra_info('peername')

    print(f"Recebida solicitação de {addr}: {message}")

    if message == "VERIFY":
        # Fazer a verificação de todos os servidores e retornar o status
        response = ""
        for server_ip, server_port in servers:
            status = await check_server_health(server_ip, server_port)
            if status:
                response += f"Servidor {server_ip}:{server_port} está ativo.\n"
            else:
                response += f"Servidor {server_ip}:{server_port} está offline.\n"

        # Enviar a resposta ao cliente solicitante
        writer.write(response.encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main():
    """Função principal que roda o serviço de verificação."""
    # Iniciar o verificador de servidores como uma tarefa contínua
    asyncio.create_task(verify_servers())

    # Iniciar o servidor de verificação para atender a requisições externas
    server = await asyncio.start_server(handle_client, '0.0.0.0', 5002)  # Porta 5002 para verificação externa
    addr = server.sockets[0].getsockname()
    print(f"Serviço de Verificação rodando em {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())