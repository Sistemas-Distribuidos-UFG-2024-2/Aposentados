from xmlrpc.server import SimpleXMLRPCServer

def calcular_credito(saldo_medio):
    if saldo_medio >= 0 and saldo_medio <= 200:
        credito = 0
    elif saldo_medio >= 201 and saldo_medio <= 400:
        credito = saldo_medio * 0.20
    elif saldo_medio >= 401 and saldo_medio <= 600:
        credito = saldo_medio * 0.30
    else:
        credito = saldo_medio * 0.40

    return f"Saldo Médio: R$ {saldo_medio:.2f}, Crédito Especial: R$ {credito:.2f}"

def servidor_rpc():
    server = SimpleXMLRPCServer(("127.0.0.1", 65432))
    print("Servidor RPC ouvindo em 127.0.0.1:65432")

    # Registra a função para ser acessível remotamente
    server.register_function(calcular_credito, "calcular_credito")
    
    # Mantém o servidor em execução
    server.serve_forever()

if __name__ == "__main__":
    servidor_rpc()
