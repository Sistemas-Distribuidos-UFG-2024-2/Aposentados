import xmlrpc.client

def cliente():
    # Conectar ao servidor RPC
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
    
    # Exemplo: enviar valor 1 (Ás) e naipe 1 (Ouros)
    resposta = proxy.nome_carta(1, 1)
    print("Nome da carta:", resposta)

if __name__ == "__main__":
    cliente()
