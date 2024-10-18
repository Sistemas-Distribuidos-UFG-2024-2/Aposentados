from xmlrpc.server import SimpleXMLRPCServer

def classificar(idade, tempo_servico):
    """ Essa função classifica se o colaborador está propício à aposentadoria"""

    if idade >= 65 and tempo_servico >= 30:
        return "Pode se aposentar!"
    elif idade >= 60 and tempo_servico >= 25:
        return "Pode se aposentar!"
    else:
        return "Não pode se aposentar!"


if __name__ == '__main__':
    host, port = 'localhost', 8080

    servidor = SimpleXMLRPCServer((host, port))

    print("Servidor conectado em http://localhost:8080")

    servidor.register_function(classificar, "classificar")

    servidor.serve_forever()