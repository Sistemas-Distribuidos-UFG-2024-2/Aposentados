from xmlrpc.server import SimpleXMLRPCServer

# Função para calcular o reajuste de salário
def calcula_reajuste(nome, cargo, salario):
    if cargo.lower() == "operador":
        salario_reajustado = salario * 1.20  # 20% de reajuste
    elif cargo.lower() == "programador":
        salario_reajustado = salario * 1.18  # 18% de reajuste
    else:
        salario_reajustado = salario  # Sem reajuste para outros cargos

    return f"Nome: {nome}, Salário Reajustado: {salario_reajustado:.2f}"

# Configurando o servidor XML-RPC
def servidor():
    server = SimpleXMLRPCServer(('localhost', 8000))
    print("Servidor RPC rodando na porta 8000...")
    server.register_function(calcula_reajuste, 'calcula_reajuste')  # Registrando a função

    server.serve_forever()  # Mantendo o servidor ativo

if __name__ == "__main__":
    servidor()
