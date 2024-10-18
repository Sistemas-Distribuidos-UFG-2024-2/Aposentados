import socket

def verificar_maioridade(nome, sexo, idade):
    sexo = sexo.lower()  # Tornar o sexo insensível a maiúsculas/minúsculas
    if sexo == 'masculino' and idade >= 18:
        return f"{nome} já atingiu a maioridade."
    elif sexo == 'feminino' and idade >= 21:
        return f"{nome} já atingiu a maioridade."
    else:
        return f"{nome} ainda não atingiu a maioridade."

def servidor():
    host = 'localhost'  # Endereço do servidor
    port = 5000         # Porta do servidor
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, port))
    servidor_socket.listen(1)
    print(f"Servidor rodando na porta {port}...")

    while True:
        conexao, endereco = servidor_socket.accept()
        print(f"Conexão estabelecida com {endereco}")

        # Receber os dados do cliente
        dados = conexao.recv(1024).decode()
        if not dados:
            break

        # Separar os dados recebidos
        nome, sexo, idade = dados.split(',')
        idade = int(idade)  # Converter a idade para inteiro

        # Verificar se atingiu a maioridade
        resultado = verificar_maioridade(nome, sexo, idade)

        # Enviar a resposta de volta para o cliente
        conexao.send(resultado.encode())

        # Fechar a conexão
        conexao.close()

if __name__ == "__main__":
    servidor()
