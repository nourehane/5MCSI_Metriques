from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm2

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("forms.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def colonnes():
    return render_template("colonnes.html")


# début du test pour l'exercice 6
GITHUB_API_URL = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

@app.route('/')
def home():
    return "<h1>Bienvenue ! Visitez <a href='/commits'>/commits</a> pour voir les graphiques des commits.</h1>"

@app.route('/commits')
def commits():
    try:
        # Récupérer les commits depuis l'API GitHub
        response = requests.get(GITHUB_API_URL)
        commits_data = response.json()

        # Extraire les minutes des commits
        commit_minutes = []
        for commit in commits_data:
            commit_date = commit["commit"]["author"]["date"]
            date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
            commit_minutes.append(date_object.minute)

        # Compter les occurrences de chaque minute
        minute_counts = Counter(commit_minutes)

        # Transformer les données pour le graphique
        labels = sorted(minute_counts.keys())
        values = [minute_counts[minute] for minute in labels]

        return render_template('commits.html', labels=labels, values=values)

    except Exception as e:
        return jsonify({"error": str(e)})
# fin du test pour l'exercice 6
  
if __name__ == "__main__":
  app.run(debug=True)
