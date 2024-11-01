import asyncio
import json

async def handle_connection(reader, writer):
    while True:
        data = await reader.read(1024)

        if not data:
            break



async def main():
    middleware = await asyncio.start_server(handle_connection, '127.0.0.1', 9010)  # Rodando em 9010
    addr = middleware.sockets[0].getsockname()
    print(f'Middleware rodando em {addr}')

    async with middleware:
        await middleware.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())