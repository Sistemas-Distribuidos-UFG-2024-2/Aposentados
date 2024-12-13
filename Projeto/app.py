# app.py
from flask import Flask, render_template, request, redirect, url_for
import asyncio
import json
from client import empacotar_funcionario

app = Flask(__name__)

# Função de comunicação TCP
async def tcp_client(request_data, service_name, retries=3):
    for attempt in range(retries):
        try:
            reader, writer = await asyncio.open_connection('127.0.0.1', 8080)

            # Enviar o nome do serviço
            writer.write(service_name.encode() + b'\n')  # Service name isolado
            await writer.drain()

            # Serializar e enviar os dados em formato JSON
            funcionario_json = json.dumps(request_data)
            print(f'Enviando: {funcionario_json}')
            writer.write(funcionario_json.encode())
            await writer.drain()

            # Receber resposta do servidor
            response = await reader.read(1024)
            writer.close()
            await writer.wait_closed()

            print(f"Resposta recebida: {response.decode()}")
            return response.decode()

        except Exception as e:
            print(f"Erro na tentativa {attempt + 1}: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(3)
            else:
                return "Falha na conexão com o servidor após várias tentativas."


# Rota principal do menu inicial
@app.route('/')
def home():
    return render_template('interface.html')


# Menu do Usuário
@app.route('/menu_usuario', methods=['GET', 'POST'])
def menu_usuario():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        funcionario = empacotar_funcionario(cpf=cpf)

        request_data = {
            "operation": "PESQUISAR_FUNCIONARIO",
            "funcionario": funcionario
        }
        service_name = "servidor"

        # Comunicação TCP
        response = asyncio.run(tcp_client(request_data, service_name))

        # Tratamento da resposta (JSON ou texto simples)
        if response.strip().startswith(("{", "[")):  # Verifica se é JSON
            try:
                response_dict = json.loads(response)
            except json.JSONDecodeError:
                response_dict = {"Erro": "Resposta inválida do servidor"}
        else:
            # Caso seja uma resposta simples, encapsula em um dicionário
            response_dict = {"Resultado": response.strip()}

        return render_template('resultado.html', response=response_dict)

    return render_template('menu_usuario.html')


# Menu do Administrador
@app.route('/menu_adm', methods=['GET', 'POST'])
def menu_adm():
    if request.method == 'POST':
        operation = request.form.get('operation')
        service_name = "servidor"

        if operation == "pesquisar":
            cpf = request.form.get('cpf')
            funcionario = empacotar_funcionario(cpf=cpf)
            request_data = {
                "operation": "PESQUISAR_FUNCIONARIO",
                "funcionario": funcionario
            }
        elif operation == "cadastrar":
            nome = request.form.get('nome')
            idade = request.form.get('idade')
            tempoDeTrabalho = request.form.get('tempoDeTrabalho')
            cargo = request.form.get('cargo')
            cpf = request.form.get('cpf')
            salario = request.form.get('salario')
            funcionario = empacotar_funcionario(nome, idade, tempoDeTrabalho, cargo, cpf, salario)
            request_data = {
                "operation": "CADASTRAR_FUNCIONARIO",
                "funcionario": funcionario
            }
        else:
            return redirect(url_for('menu_adm'))

        # Comunicação TCP
        response = asyncio.run(tcp_client(request_data, service_name))

        # Tratamento da resposta (JSON ou texto simples)
        if response.strip().startswith(("{", "[")):  # Verifica se é JSON
            try:
                response_dict = json.loads(response)
            except json.JSONDecodeError:
                response_dict = {"Erro": "Resposta inválida do servidor"}
        else:
            # Caso seja uma resposta simples, encapsula em um dicionário
            response_dict = {"Resultado": response.strip()}

        return render_template('resultado.html', response=response_dict)

    return render_template('menu_adm.html')


# Rota para sair
@app.route('/sair')
def sair():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8081)
