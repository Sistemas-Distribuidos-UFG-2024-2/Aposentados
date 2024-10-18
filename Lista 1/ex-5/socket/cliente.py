import socket

if __name__ == '__main__':
    host, port = 'localhost', 8080

    print(f"Para finalizar o programa digite 'q'!")

    while True:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, port))

        idade = input("Insira a idade do nadador: ")


        if idade == 'q':
            break

        cliente_socket.send(idade.encode())

        classificacao = cliente_socket.recv(1024).decode()

        print(f"A idade: {idade}, enquadra na categoria: {classificacao}")