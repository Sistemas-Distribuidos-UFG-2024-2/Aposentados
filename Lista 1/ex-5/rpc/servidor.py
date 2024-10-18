from xmlrpc.server import SimpleXMLRPCServer

def classificar_idade(idade):
    """ Essa função classifica a idade conforme o valor recebido"""

    if 5 <= idade <= 7:
        return "infantil A"
    elif 8 <= idade <= 10:
        return "infantil B"
    elif 11 <= idade <= 13:
        return "juvenil A"
    elif 14 <= idade <= 17:
        return "juvenil B"
    elif idade >= 18:
        return "adulto"
    else:
        return "Idade não se enquadra nas Categorias."


if __name__ == '__main__':
    host, port = 'localhost', 8080

    servidor = SimpleXMLRPCServer((host,port))

    print("Servidor conectado em http://localhost:8080")

    servidor.register_function(classificar_idade, "classificar_idade")

    servidor.serve_forever()