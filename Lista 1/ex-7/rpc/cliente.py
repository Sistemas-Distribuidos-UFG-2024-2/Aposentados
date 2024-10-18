import xmlrpc.client

if __name__ == '__main__':
    cliente = xmlrpc.client.ServerProxy("http://localhost:8080")

    print(f"Para finalizar o programa digite 'q'!")

    while True:
        print("----- Insira as informações do usuário ----")
        idade = input("Idade: ")

        if idade == 'q':
            break

        tempo_servico = input("Tempo de serviço: ")

        if tempo_servico == 'q':
            break

        idade = int(idade)
        tempo_servico = int(tempo_servico)

        classificacao = cliente.classificar(idade, tempo_servico)

        print("\n ------- Resposta recebida pelo cliente: ---------")
        print(f"Resposta: {classificacao}\n")