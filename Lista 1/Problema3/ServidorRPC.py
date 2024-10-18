from xmlrpc.server import SimpleXMLRPCServer

def calcular_resultado(N1, N2, N3=None):
    media = (N1 + N2) / 2
    if media >= 7.0:
        return "Aprovado com {:.2f}".format(media)
    elif 3.0 < media < 7.0:
        if N3 is None:
            return "fazer N3"
        else:
            mediafinal = (media + N3) / 2
            if mediafinal >= 5.0:
                return "Aprovado com {:.2f}".format(mediafinal)
            else:
                return "Reprovado com {:.2f}".format(mediafinal)
    else:
        return "Reprovado com {:.2f}".format(media)

# Inicializa o servidor XML-RPC
def main():
    server = SimpleXMLRPCServer(("127.0.0.1", 5000))
    print("Servidor XML-RPC ouvindo na porta 5000...")
    
    server.register_function(calcular_resultado, "calcular_resultado")
    
    server.serve_forever()

if __name__ == "__main__":
    main()
