from xmlrpc.server import SimpleXMLRPCServer

class CartaBaralho:
    VALORES = {
        1: "Ás", 2: "Dois", 3: "Três", 4: "Quatro", 5: "Cinco", 6: "Seis",
        7: "Sete", 8: "Oito", 9: "Nove", 10: "Dez", 11: "Valete", 12: "Dama", 13: "Rei"
    }
    
    NAIPES = {
        1: "Ouros", 2: "Paus", 3: "Copas", 4: "Espadas"
    }

    @staticmethod
    def nome_carta(valor, naipe):
        if 1 <= valor <= 13 and 1 <= naipe <= 4:
            return f"{CartaBaralho.VALORES[valor]} de {CartaBaralho.NAIPES[naipe]}"
        return "Carta inválida"


# Iniciando o servidor XML-RPC
def iniciar_servidor():
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Servidor RPC rodando na porta 8000...")
    
    # Registrando a função nome_carta do objeto CartaBaralho
    server.register_function(CartaBaralho.nome_carta, "nome_carta")
    
    server.serve_forever()

if __name__ == "__main__":
    iniciar_servidor()
