from flask import Flask, render_template, request, jsonify
import redis

# Configuración de Redis
r = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

# Implementar un algoritmo de recomendación mejorado
def recommend_products(input_text):
    if not input_text:
        return []

    recommendations = []
    input_tokens = input_text.lower().split()
    for key in r.keys():
        title = r.get(key).decode('utf-8')
        title_tokens = title.lower().split()
        if any(token in title_tokens for token in input_tokens):
            recommendations.append(title)
    return recommendations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.form
    input_text = data.get('user_input')
    
    if not input_text:
        return render_template('result.html', results=["No se proporcionó entrada."])
    
    recommendations = recommend_products(input_text)
    return render_template('result.html', results=recommendations)

# Ruta para recibir solicitudes JSON
@app.route('/api/recommend', methods=['POST'])
def api_recommendations():
    data = request.get_json()
    input_text = data.get('input_text')
    
    if not input_text:
        return jsonify([])

    recommendations = recommend_products(input_text)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
