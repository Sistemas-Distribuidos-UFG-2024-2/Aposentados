from flask import Flask, request, jsonify

app = Flask(__name__)

def calcular_Peso(sexo, altura):
    if sexo == 'M':
        ideal= (72.7 * altura) - 58
        return "Peso ideal Masculino com {:.2f}".format(ideal)
    elif sexo == 'F':
        ideal= (62.1 * altura) - 44.7
        return "Peso ideal Feminino com {:.2f}".format(ideal)
    return "Erro"

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json
    sexo = data['sexo']
    altura = float(data['altura'])
    
    resultado = calcular_Peso(sexo, altura)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
