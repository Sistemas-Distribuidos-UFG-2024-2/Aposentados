import socket

def cliente():
    host = '127.0.0.1'
    port = 65432

    nome = input("Digite o nome do funcionário: ")
    nivel = input("Digite o nível do funcionário (A, B, C, D): ").upper()
    salario_bruto = float(input("Digite o salário bruto do funcionário: "))
    dependentes = int(input("Digite o número de dependentes: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        mensagem = f"{nome},{nivel},{salario_bruto},{dependentes}"
        s.sendall(mensagem.encode('utf-8'))

        data = s.recv(1024).decode('utf-8')
        print(f"Resposta do servidor: {data}")

if __name__ == "__main__":
    cliente()
