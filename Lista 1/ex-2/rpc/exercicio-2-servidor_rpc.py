from xmlrpc.server import SimpleXMLRPCServer

def verificar_maioridade(nome, sexo, idade):
    sexo = sexo.lower()  # Tornar o sexo insensível a maiúsculas/minúsculas
    idade = int(idade)   # Certificar que a idade seja um número inteiro
    if sexo == 'masculino' and idade >= 18:
        return f"{nome} já atingiu a maioridade."
    elif sexo == 'feminino' and idade >= 21:
        return f"{nome} já atingiu a maioridade."
    else:
        return f"{nome} ainda não atingiu a maioridade."

def iniciar_servidor():
    servidor = SimpleXMLRPCServer(("localhost", 8000))
    print("Servidor RPC rodando na porta 8000...")
    servidor.register_function(verificar_maioridade, "verificar_maioridade")
    servidor.serve_forever()

if __name__ == "__main__":
    iniciar_servidor()
