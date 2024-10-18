import socket
from carta_baralho import CartaBaralho  # Importando a classe definida acima

def servidor():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind(('localhost', 12345))
    servidor_socket.listen(5)
    print("Servidor aguardando conexões...")

    while True:
        conn, addr = servidor_socket.accept()
        print(f"Conectado por {addr}")
        
        dados = conn.recv(1024).decode()  # Recebendo os dados do cliente
        if not dados:
            break
        
        valor, naipe = map(int, dados.split(','))  # Separando o valor e o naipe enviados
        carta = CartaBaralho(valor, naipe)
        nome_carta = carta.nome_carta()
        
        conn.send(nome_carta.encode())  # Enviando o nome da carta de volta para o cliente
        conn.close()

if __name__ == "__main__":
    servidor()
