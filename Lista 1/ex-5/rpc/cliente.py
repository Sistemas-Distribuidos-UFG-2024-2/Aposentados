import xmlrpc.client

if __name__ == '__main__':
    host, port = 'localhost', 8080

    print(f"Para finalizar o programa digite 'q'!")

    while True:
        cliente = xmlrpc.client.ServerProxy('http://localhost:8080')

        idade = input("Insira a idade do nadador: ")

        if idade == 'q':
            break

        classificacao = cliente.classificar_idade(int(idade))

        print(f"A idade: {idade}, enquadra na categoria: {classificacao}")