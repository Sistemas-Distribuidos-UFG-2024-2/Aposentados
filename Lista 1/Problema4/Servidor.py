import socket
import string

def calcular_Peso(sexo, altura):
    if sexo == 'M':
        ideal= (72.7 * altura) - 58
        return "Peso ideal Masculino com {:.2f}".format(ideal)
    elif sexo == 'F':
        ideal= (62.1 * altura) - 44.7
        return "Peso ideal Feminino com {:.2f}".format(ideal)
    return "Erro"

HOST = '127.0.0.1'  
PORT = 5000        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor ouvindo na porta {PORT}...")

    conn, addr = s.accept()
    with conn:
        print('Conectado por', addr)
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            dados = data.split(';')
            sexo = dados[0]
            altura = float(dados[1])

            resultado = calcular_Peso(sexo, altura)
            print(f"Resultado: {resultado}")
            conn.sendall((resultado+'\n').encode())

