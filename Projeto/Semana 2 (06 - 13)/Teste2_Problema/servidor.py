import socket

# Configurações do servidor
HOST = '0.0.0.0'  # Deixar em 0.0.0.0 qualquer 1 pode se conectar
PORT = 5000       # Porta que o servidor vai escutar

# Criando o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  #Esperando alguma conexão chegar da porta 5000

print(f"Servidor escutando na porta {PORT}...")

# Aceita a conexão do cliente
conexao, addr = server_socket.accept()
print(f"Conexão estabelecida com {addr}")

# Recebe a string do cliente
data = conexao.recv(1024).decode()  # Recebe até 1024 bytes
print(f"Mensagem recebida do cliente: {data}")

# Envia uma resposta de volta
resposta = "Mundo"
conexao.send(resposta.encode())

# Fechando a conexão
conexao.close()
server_socket.close()