import socket


if __name__ == '__main__':
    host, port = 'localhost', 8080

    idade = print(f"Para finalizar o programa digite 'q'!")

    while True:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, port))

        print("----- Insira as informações do usuário ----")
        idade = input("Idade: ")

        if idade == 'q':
            break

        tempo_servico = input("Tempo de serviço: ")

        if tempo_servico == 'q':
            break

        dados = f"{idade},{tempo_servico}"

        cliente_socket.send(dados.encode())

        classificacao = cliente_socket.recv(1024).decode()

        print("\n ------- Resposta recebida pelo cliente: ---------")
        print(f"Dados enviados: {dados}")
        print(f"Resposta: {classificacao}\n")

