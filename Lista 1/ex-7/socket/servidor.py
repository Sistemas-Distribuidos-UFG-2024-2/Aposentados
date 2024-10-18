import socket

def classificar(idade, tempo_servico):
    """ Essa função classifica se o colaborador está propício à aposentadoria"""

    if idade >= 65 and tempo_servico >= 30:
        return "Pode se aposentar!"
    elif idade >= 60 and tempo_servico >= 25:
        return "Pode se aposentar!"
    else:
        return "Não pode se aposentar!"


if __name__ == '__main__':

    host, port = 'localhost', 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Servidor aguardando conexão....")
    while True:
        conn, addr = server_socket.accept()

        print(f"\nServidor conectado com: {addr}")

        dados = conn.recv(1024).decode()

        print(f"Servidor classificando os dados: {dados}.....")

        idade, tempo_servico = map(int,dados.split(","))

        classificacao = classificar(idade, tempo_servico)

        conn.send(classificacao.encode())
        print(f"Classificação finalizada, enviando ao cliente....")

        conn.close()