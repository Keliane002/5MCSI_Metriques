from flask import Flask, render_template, jsonify
import json
from datetime import datetime
from urllib.request import Request, urlopen
from collections import Counter

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("hello.html")

@app.route('/contact/')
def contact():
    return render_template("contact.html")

@app.route('/histogramme/')
def histogramme():
    url = 'https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    data = json.loads(response.read().decode('utf-8'))

    results = []
    for item in data.get('list', []):
        dt = item.get('dt_txt', '')[:16]
        temp_kelvin = item.get('main', {}).get('temp')
        if temp_kelvin:
            temp_celsius = temp_kelvin - 273.15
            results.append({'Jour': dt, 'temp': round(temp_celsius, 2)})
    return render_template("histogramme.html", meteo=results)

@app.route('/rapport/')
def rapport():
    url = 'https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    data = json.loads(response.read().decode('utf-8'))

    results = []
    for item in data.get('list', []):
        dt = item.get('dt')
        temp_kelvin = item.get('main', {}).get('temp')
        if temp_kelvin:
            temp_celsius = temp_kelvin - 273.15
            results.append({'Jour': dt, 'temp': round(temp_celsius, 2)})
    return render_template("graphique.html", meteo=results)

if __name__ == "__main__":
    app.run(debug=True)
