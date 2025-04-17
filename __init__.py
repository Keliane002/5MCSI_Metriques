from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
from flask import Flask, jsonify
from urllib.request import urlopen
                                                                                                                                     
app = Flask(__name__)  

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_kelvin = list_element.get('main', {}).get('temp')
        if temp_kelvin is not None:
            temp_celsius = temp_kelvin - 273.15
            results.append({'Jour': dt_value, 'temp': round(temp_celsius, 2)})
    return jsonify(results=results)

@app.route('/tawarano_html/')
def mongraphique():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_kelvin = list_element.get('main', {}).get('temp')
        if temp_kelvin is not None:
            temp_celsius = temp_kelvin - 273.15
            results.append({'Jour': dt_value, 'temp': round(temp_celsius, 2)})
    return render_template("graphique.html", meteo=results)
                                                                                                                                      
@app.route('/')
def hello_world():
    return render_template('hello.html') #(COMMENTAIRE)
  
if __name__ == "__main__":
  app.run(debug=True)
