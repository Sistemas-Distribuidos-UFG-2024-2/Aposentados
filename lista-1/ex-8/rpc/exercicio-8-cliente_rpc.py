import xmlrpc.client

def cliente_rpc():
    # Conecta ao servidor RPC
    server = xmlrpc.client.ServerProxy("http://127.0.0.1:65432/")

    saldo_medio = float(input("Digite o saldo médio do cliente: "))

    # Faz a chamada remota para calcular o crédito especial
    resultado = server.calcular_credito(saldo_medio)
    print(f"Resposta do servidor: {resultado}")

if __name__ == "__main__":
    cliente_rpc()
