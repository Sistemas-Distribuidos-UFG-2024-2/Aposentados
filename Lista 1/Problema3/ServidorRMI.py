from flask import Flask, request, jsonify

app = Flask(__name__)

def calcular_resultado(N1, N2, N3=None):
    media = (N1 + N2) / 2
    if media >= 7.0:
        return {"resultado": "Aprovado", "media": media}
    elif 3.0 < media < 7.0:
        if N3 is None:
            return {"resultado": "fazer N3"}
        else:
            mediafinal = (media + N3) / 2
            if mediafinal >= 5.0:
                return {"resultado": "Aprovado com N3", "mediafinal": mediafinal}
            else:
                return {"resultado": "Reprovado", "mediafinal": mediafinal}
    else:
        return {"resultado": "Reprovado", "media": media}

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json
    N1 = float(data['N1'])
    N2 = float(data['N2'])
    N3 = float(data['N3']) if 'N3' in data else None
    
    resultado = calcular_resultado(N1, N2, N3)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
