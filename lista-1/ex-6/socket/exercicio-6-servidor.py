import socket

def calcular_salario_liquido(nome, nivel, salario_bruto, dependentes):
    if nivel == "A":
        desconto = 0.03 if dependentes == 0 else 0.08
    elif nivel == "B":
        desconto = 0.05 if dependentes == 0 else 0.10
    elif nivel == "C":
        desconto = 0.08 if dependentes == 0 else 0.15
    elif nivel == "D":
        desconto = 0.10 if dependentes == 0 else 0.17
    else:
        return "Nível inválido"

    salario_liquido = salario_bruto * (1 - desconto)
    return f"Nome: {nome}, Nível: {nivel}, Salário Líquido: R$ {salario_liquido:.2f}"

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
                nome, nivel, salario_bruto, dependentes = data.split(',')
                salario_bruto = float(salario_bruto)
                dependentes = int(dependentes)

                resultado = calcular_salario_liquido(nome, nivel, salario_bruto, dependentes)
                conn.sendall(resultado.encode('utf-8'))
                print("Resultado enviado ao cliente")

if __name__ == "__main__":
    servidor()
