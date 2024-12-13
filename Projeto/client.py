import asyncio
import json

# Dados do funcionário que serão enviados
funcionario = {
    "nome": "Joao Silva",
    "idade": "77",
    "tempoDeTrabalho": "60",
    "cargo": "Desenvolvedor",
    "cpf": "123.132.132-77",
    "salario": 5000
}

# Nome do serviço que o cliente quer acessar
service_name = "servidor_principal"  # Nome do serviço a ser passado ao middleware

async def tcp_client(funcionario, service_name, retries=3):
    for attempt in range(retries): # Tentativa de se conectar ao servidor
        try:
            reader, writer = await asyncio.open_connection('127.0.0.1', 8080)  # Conectar ao middleware

            # Enviando o nome do serviço ao middleware
            writer.write(service_name.encode() + b'\n')
            await writer.drain()

            # Serializando os dados do funcionário em JSON
            funcionario_json = json.dumps(funcionario)
            print(f'Enviando: {funcionario_json}')
            
            # Enviando os dados para o middleware
            writer.write(funcionario_json.encode())
            await writer.drain()

            # Recebendo a resposta do middleware (ou servidor final)
            data = await reader.read(1024)

            if data:  # Recebeu a resposta do middleware
                print(f'Resposta recebida: {data.decode()}')
                print('Fechando a conexão...')
                writer.close()
                await writer.wait_closed()
                break

        except Exception as e:
            print(e)
            if attempt < retries - 1:
                await asyncio.sleep(10)  # Espera antes de tentar novamente
            else:
                print(f"Falha ao conectar após {retries} tentativas.")

def empacotar_funcionario(nome=None, idade=None, tempoDeTrabalho=None, cargo=None, cpf=None, salario=None):
    funcionario = {
        "nome": nome,
        "idade": idade,
        "tempoDeTrabalho": tempoDeTrabalho,
        "cargo": cargo,
        "cpf": cpf,
        "salario": salario
    }
    return funcionario


def iniciar_menu():
    while True:
        print("\n--- MENU ---")
        print("1. Entrar como Usuário")
        print("2. Entrar como Administrador")
        print("3. Sair")

        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            menu_usuario()
        elif escolha == '2':
            menu_adm()
        elif escolha == '3':
            print("\nEncerrando programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

def menu_usuario():
    while True:
        print("\n--- MENU DO USUÁRIO ---")
        print("1. Pesquisar um Funcionário")
        print("2. Voltar ao Menu Principal")

        escolha = input("\nEscolha uma opção: ")

        if escolha == '1': #A diferença dessa para o do administrador é que essa não retorna todos os dados do funcionario

            CPF= input(f"Digite o CPF de um Funcionário para Pesquisa. (formato: 123.132.132-77)\n")
            funcionario= empacotar_funcionario(cpf= CPF)
            request = {
                "operation": "PESQUISAR_FUNCIONARIO",  # OPERAÇÃO QUE O SERVIDOR REGISTRADOR VAI REALIZAR
                "funcionario": funcionario
            }
            service_name = "servidorAux"

            asyncio.run(tcp_client(request, service_name))

        elif escolha == '2':
            break
        else:
            print("Opção inválida! Tente novamente.")

def menu_adm():
    while True:
        print("\n--- MENU DO ADMINISTRADOR ---")
        print("1. Pesquisar um Funcionário")
        print("2. Registrar um Funcionário")
        print("3. Teste de Cadastro")
        print("4. Teste de Pesquisa")
        print("5. Sair")

        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':

            CPF= input(f"Digite o CPF de um Funcionário para Pesquisa. (formato: 123.132.132-77)\n")
            funcionario= empacotar_funcionario(cpf= CPF)
            request = {
                "operation": "GET_FUNCIONARIO",  # OPERAÇÃO QUE O SERVIDOR REGISTRADOR VAI REALIZAR
                "funcionario": funcionario
            }
            service_name = "servidor_registrador"

            asyncio.run(tcp_client(request, service_name))

        elif escolha == '2':
            
            nome= input(f"Digite o nome de um Funcionário para Cadastro.\n")
            idade= input(f"Digite a idade de um Funcionário para Cadastro.\n")
            tempoDeTrabalho= input(f"Digite o Tempo de Trabalho de um Funcionário para Cadastro.\n")
            cargo= input(f"Digite o cargo de um Funcionário para Cadastro.\n")
            CPF= input(f"Digite o CPF de um Funcionário para Cadastro. (formato: 123.132.132-77)\n")
            salario= input(f"Digite o salario de um Funcionário para Cadastro. \n")

            funcionario= empacotar_funcionario(nome, idade, tempoDeTrabalho, cargo, CPF, salario)
            request = {
                "operation": "CADASTRAR_FUNCIONARIO",  # OPERAÇÃO QUE O SERVIDOR REGISTRADOR VAI REALIZAR
                "funcionario": funcionario
            }
            service_name = "servidor_registrador"

            asyncio.run(tcp_client(request, service_name))

        elif escolha == '3':

            funcionario = {
                            "nome": "Joao Silva",
                            "idade": "77",
                            "tempoDeTrabalho": "60",
                            "cargo": "Desenvolvedor",
                            "cpf": "123.132.132-77",
                            "salario": 5000
                        }
            
            request = {
                "operation": "CADASTRAR_FUNCIONARIO",  # OPERAÇÃO QUE O SERVIDOR REGISTRADOR VAI REALIZAR
                "funcionario": funcionario
            }
            service_name = "servidor_registrador"

            asyncio.run(tcp_client(request, service_name))
        
        elif escolha == '4':

            CPF= "123.132.132-77"
            funcionario= empacotar_funcionario(cpf= CPF)
            request = {
                "operation": "GET_FUNCIONARIO",  # OPERAÇÃO QUE O SERVIDOR REGISTRADOR VAI REALIZAR
                "funcionario": funcionario
            }
            service_name = "servidor_registrador"

            asyncio.run(tcp_client(request, service_name))

        elif escolha == '5':
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == '__main__':
    iniciar_menu()
