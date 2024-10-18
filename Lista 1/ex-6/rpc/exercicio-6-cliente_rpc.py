import xmlrpc.client

def cliente_rpc():
    # Conecta ao servidor RPC
    server = xmlrpc.client.ServerProxy("http://127.0.0.1:65432/")

    nome = input("Digite o nome do funcionário: ")
    nivel = input("Digite o nível do funcionário (A, B, C, D): ").upper()
    salario_bruto = float(input("Digite o salário bruto do funcionário: "))
    dependentes = int(input("Digite o número de dependentes: "))

    # Faz a chamada remota para calcular o salário líquido
    resultado = server.calcular_salario_liquido(nome, nivel, salario_bruto, dependentes)
    print(f"Resposta do servidor: {resultado}")

if __name__ == "__main__":
    cliente_rpc()
