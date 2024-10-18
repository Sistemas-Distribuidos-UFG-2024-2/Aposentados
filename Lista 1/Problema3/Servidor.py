import socket

def calcular_resultado(N1, N2, N3= None):
    media= (N1+N2) /2
    if media>=7.0:
        return "Aprovado com {:.2f}".format(media)
    elif media>3.0 and media<7.0:
        if N3 is None:
            return "fazer N3"
        else:
            mediafinal= (media+N3)/2
            if mediafinal >= 5.0:
                return "Aprovado com {:.2f}".format(mediafinal)
            else:
                return "Reprovado com {:.2f}".format(mediafinal)
    else:
        return "Reprovado com {:.2f}".format(media)

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

            notas = data.split(';')
            n1 = float(notas[0])
            n2 = float(notas[1])
            n3 = float(notas[2]) if len(notas) > 2 else None

            resultado = calcular_resultado(n1, n2, n3)
            print(f"Resultado: {resultado}")
            conn.sendall((resultado+'\n').encode())

