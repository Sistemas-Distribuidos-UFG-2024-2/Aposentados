import asyncio
import socket
import random

# Lista de servidores disponíveis
servers = [("127.0.0.1", 9001), ("127.0.0.1", 9002)]  # Endereços dos servidores


async def check_server_health(server_ip, server_port):
    """Verifica se o servidor está disponível."""
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(server_ip, server_port), timeout=5)
        writer.close()
        await writer.wait_closed()
        return True
    except Exception as e:
        print(f"Servidor {server_ip}:{server_port} indisponível - {e}")
        return False


async def get_next_server():
    """Seleciona o próximo servidor disponível."""
    random.shuffle(servers)  # Distribui a carga aleatoriamente
    for server_ip, server_port in servers:
        if await check_server_health(server_ip, server_port):
            return server_ip, server_port
    return None, None


async def handle_client(reader, writer):
    """Manipula a conexão do cliente."""
    print("Conexão recebida")

    server_ip, server_port = await get_next_server()

    if server_ip is None:
        print("Nenhum servidor disponível.")
        writer.write(b"Nenhum servidor disponivel.\n")
        await writer.drain()
        writer.close()
        return

    try:
        server_reader, server_writer = await asyncio.wait_for(asyncio.open_connection(server_ip, server_port),
                                                              timeout=5)
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
        writer.write(b"Erro ao se comunicar com o servidor.\n")
        await writer.drain()
    finally:
        writer.close()
        if 'server_writer' in locals():
            server_writer.close()


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8080)  # VIP será em 0.0.0.0
    addr = server.sockets[0].getsockname()
    print(f'Middleware rodando em {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())