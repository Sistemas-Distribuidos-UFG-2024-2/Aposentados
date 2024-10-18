import socket

def classificar_idade(idade):
    """ Essa função classifica a idade conforme o valor recebido"""

    if 5 <= idade <= 7:
        return "infantil A"
    elif 8 <= idade <= 10:
        return "infantil B"
    elif 11 <= idade <= 13:
        return "juvenil A"
    elif 14 <= idade <= 17:
        return "juvenil B"
    elif idade >= 18:
        return "adulto"
    else:
        return "Idade não se enquadra nas Categorias."


if __name__ == '__main__':

    host, port = 'localhost', 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Servidor aguardando conexão....")
    while True:
        conn, addr = server_socket.accept()

        print(f"Servidor conectado com: {addr}")

        idade_data = conn.recv(1024).decode()
        idade = int(idade_data)

        print(f"Servidor classificando a idade: {idade}.....")

        classificar = classificar_idade(idade)

        conn.send(classificar.encode())
        print(f"Classificação finalizada, enviando ao cliente....")

        conn.close()