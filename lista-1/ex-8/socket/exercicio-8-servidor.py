import socket

def calcular_credito(saldo_medio):
    if saldo_medio >= 0 and saldo_medio <= 200:
        credito = 0
    elif saldo_medio >= 201 and saldo_medio <= 400:
        credito = saldo_medio * 0.20
    elif saldo_medio >= 401 and saldo_medio <= 600:
        credito = saldo_medio * 0.30
    else:
        credito = saldo_medio * 0.40

    return f"Saldo Médio: R$ {saldo_medio:.2f}, Crédito Especial: R$ {credito:.2f}"

def servidor():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor ouvindo em {host}:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")

            data = conn.recv(1024).decode('utf-8')
            if data:
                saldo_medio = float(data)
                resultado = calcular_credito(saldo_medio)
                conn.sendall(resultado.encode('utf-8'))
                print("Resultado enviado ao cliente")

if __name__ == "__main__":
    servidor()
