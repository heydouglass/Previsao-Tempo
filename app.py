import requests
import json
from decouple import config
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_KEY = "572976fc428065b9885807e4b718c994"

with open('static/cities.json', 'r', encoding='utf-8') as json_file:
    city_data = json.load(json_file)

cities = [city["name"] for city in city_data]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete():
    search_term = request.args.get('term')
    matched_cities = [
        city for city in cities if search_term.lower() in city.lower()]
    return jsonify(matched_cities)


@app.route('/processar_dados', methods=['POST'])
def processar_dados():
    cidade = request.form.get('cidade')
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br"

    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()
    descricao = requisicao_dic['weather'][0]['description']
    temperatura = requisicao_dic['main']['temp'] - 273.15
    umidade = requisicao_dic['main']['humidity']

    temperatura_int = int(temperatura)
    return render_template('index.html', descricao=descricao, temperatura_int=temperatura_int, umidade=umidade, cidade=cidade)


if __name__ == '__main__':
    app.run(debug=True)
