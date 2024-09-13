import socket

# Configurações do cliente
HOST = '127.0.0.1'  # Colocar IP do servidor  *****127.0.0.1 aponta para a própria máquina
PORT = 5000              # Porta da comunicação

# Criando o socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor
print("Tentando se conectar ao servidor...")
client_socket.connect((HOST, PORT))    #Essa porta é != da porta declarada em PORT.
                                       # A Porta declarada em PORT apenas escuta a conexão enquanto essa realiza a conexão.
# Envia a string para o servidor
message = "Olá"
client_socket.send(message.encode())

# Recebe a resposta do servidor
response = client_socket.recv(1024).decode()
print(f"Resposta do servidor: {response}")

# Fechando a conexão
client_socket.close()