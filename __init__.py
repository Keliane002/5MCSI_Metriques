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
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

    try:
        response = urlopen(url)
        data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        return f"Erreur lors de l'appel à l'API GitHub : {e}"

    minutes_list = []

    for commit in data:
        try:
            date_str = commit.get("commit", {}).get("author", {}).get("date")
            if date_str:
                date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                minute = date_obj.strftime("%H:%M")
                minutes_list.append(minute)
        except Exception as e:
            print(f"Erreur dans le parsing : {e}")

    if not minutes_list:
        return "Aucun commit trouvé."

    counts = Counter(minutes_list)
    sorted_counts = sorted(counts.items(), key=lambda x: datetime.strptime(x[0], "%H:%M"))
    minutes = [item[0] for item in sorted_counts]
    values = [item[1] for item in sorted_counts]

    return render_template("commits.html", minutes=minutes, counts=values)
  
if __name__ == "__main__":
  app.run(debug=True)
