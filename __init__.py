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

@app.route('/commits/')
def commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    data = json.loads(response.read().decode("utf-8"))

    minutes_list = []
    for commit in data:
        date_str = commit.get("commit", {}).get("author", {}).get("date")
        if date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes_list.append(date_obj.strftime('%H:%M'))

    minute_counts = Counter(minutes_list)
    sorted_items = sorted(minute_counts.items(), key=lambda x: datetime.strptime(x[0], "%H:%M"))
    return render_template("commits.html", meteo=[{"Jour": m, "temp": c} for m, c in sorted_items])

if __name__ == "__main__":
    app.run(debug=True)
