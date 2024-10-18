import socket

def cliente():
    host = '127.0.0.1'
    port = 65432

    saldo_medio = float(input("Digite o saldo médio do cliente: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(str(saldo_medio).encode('utf-8'))

        data = s.recv(1024).decode('utf-8')
        print(f"Resposta do servidor: {data}")

if __name__ == "__main__":
    cliente()
