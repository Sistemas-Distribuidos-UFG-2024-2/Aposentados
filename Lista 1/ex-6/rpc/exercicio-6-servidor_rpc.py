from xmlrpc.server import SimpleXMLRPCServer

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

def servidor_rpc():
    server = SimpleXMLRPCServer(("127.0.0.1", 65432))
    print("Servidor RPC ouvindo em 127.0.0.1:65432")

    # Registra a função para ser acessível remotamente
    server.register_function(calcular_salario_liquido, "calcular_salario_liquido")
    
    # Mantém o servidor em execução
    server.serve_forever()

if __name__ == "__main__":
    servidor_rpc()