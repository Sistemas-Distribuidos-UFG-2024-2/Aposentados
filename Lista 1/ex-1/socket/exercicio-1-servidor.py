import socket

def calcula_reajuste(cargo, salario):
    # Aplicando a regra de reajuste
    if cargo.lower() == 'operador':
        reajuste = salario * 0.20
    elif cargo.lower() == 'programador':
        reajuste = salario * 0.18
    else:
        reajuste = 0  # Sem reajuste para outros cargos
    return salario + reajuste

def servidor():
    # Criando o socket do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Endereço e porta
    server_socket.listen(5)
    print("Servidor aguardando conexões...")

    while True:
        # Aceitando a conexão do cliente
        conn, addr = server_socket.accept()
        print(f"Conectado a {addr}")

        # Recebendo dados do cliente
        dados = conn.recv(1024).decode()
        nome, cargo, salario = dados.split(',')
        salario = float(salario)

        # Calculando o reajuste
        salario_reajustado = calcula_reajuste(cargo, salario)

        # Enviando o resultado para o cliente
        resposta = f"Nome: {nome}, Salário Reajustado: {salario_reajustado:.2f}"
        conn.send(resposta.encode())

        # Fechando a conexão
        conn.close()

if __name__ == "__main__":
    servidor()
