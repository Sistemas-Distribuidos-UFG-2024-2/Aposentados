import threading

# Função que verifica a aposentadoria
def verificar_aposentadoria(idade, tempo_servico, funcionario_id):
    if idade >= 65 and tempo_servico >= 30:
        print(f"Funcionário {funcionario_id}: Pode se aposentar.")
    elif idade >= 60 and tempo_servico >= 25:
        print(f"Funcionário {funcionario_id}: Pode se aposentar.")
    else:
        print(f"Funcionário {funcionario_id}: Ainda não pode se aposentar.")

# Função que simula a entrada de dados para múltiplos funcionários
def processar_funcionarios(dados_funcionarios):
    threads = []
    
    for funcionario_id, (idade, tempo_servico) in enumerate(dados_funcionarios, start=1):
        # Criação de uma thread para cada funcionário
        t = threading.Thread(target=verificar_aposentadoria, args=(idade, tempo_servico, funcionario_id))
        threads.append(t)
        t.start()

    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()

# Lista de funcionários com idade e tempo de serviço
dados_funcionarios = [
    (66, 31),   # Funcionário 1
    (60, 25),   # Funcionário 2
    (55, 20),   # Funcionário 3
    (70, 35),   # Funcionário 4
    (61, 24)    # Funcionário 5
]

# Processar todos os funcionários
processar_funcionarios(dados_funcionarios)
