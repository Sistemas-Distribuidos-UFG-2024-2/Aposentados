class CartaBaralho:
    VALORES = {
        1: "Ás", 2: "Dois", 3: "Três", 4: "Quatro", 5: "Cinco", 6: "Seis",
        7: "Sete", 8: "Oito", 9: "Nove", 10: "Dez", 11: "Valete", 12: "Dama", 13: "Rei"
    }
    
    NAIPES = {
        1: "Ouros", 2: "Paus", 3: "Copas", 4: "Espadas"
    }

    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    def nome_carta(self):
        return f"{CartaBaralho.VALORES[self.valor]} de {CartaBaralho.NAIPES[self.naipe]}"

# Exemplo de instanciamento
carta1 = CartaBaralho(1, 1)
print(carta1.nome_carta())  # Saída: Ás de Ouros
