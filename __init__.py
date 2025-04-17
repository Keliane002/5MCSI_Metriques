from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
from flask import Flask, jsonify
from urllib.request import urlopen
import requests
from collections import Counter
from datetime import datetime
                                                                                                                                     
app = Flask(__name__)  

@app.route('/contact/')
def contact():
    return render_template("contact.html")

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

@app.route('/rapport/')
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

@app.route('/histogramme/')
def histogramme():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt_txt', '')[:16]  # Affiche la date+heure
        temp_kelvin = list_element.get('main', {}).get('temp')
        if temp_kelvin is not None:
            temp_celsius = temp_kelvin - 273.15
            results.append({'Jour': dt_value, 'temp': round(temp_celsius, 2)})
    return render_template("histogramme.html", meteo=results)
                                                                                                                                      
@app.route('/')
def hello_world():
    return render_template('hello.html') #(COMMENTAIRE)

@app.route('/commits/')
def commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Erreur lors de l'appel à l'API GitHub"

    data = response.json()
    minutes_list = []

    for commit in data:
        date_str = commit['commit']['author']['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        minutes_list.append(date_obj.minute)

    # Compter le nombre de commits par minute
    count = Counter(minutes_list)
    minutes = list(count.keys())
    commit_counts = list(count.values())

    return render_template('commits.html', minutes=minutes, commit_counts=commit_counts)
  
if __name__ == "__main__":
  app.run(debug=True)
