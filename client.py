import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)
SERVERS = ["http://10.0.1.2:5000", "http://10.0.2.2:5000", "http://10.0.3.2:5000"]

#get data from all servers
def fetch_data(endpoint):
    """Fetch data from all servers."""
    results = {}
    for server in SERVERS:
        try:
            response = requests.get(f"{server}/{endpoint}")
            if response.status_code == 200:
                results[server] = response.json()
        except:
            results[server] = None
    return results

#get metric data
@app.route("/metrics")
def get_metrics():
    return jsonify(fetch_data("metrics"))

#get historical data
@app.route("/historical-metrics")
def get_historical_metrics():
    return jsonify(fetch_data("historical-metrics"))

#send to dashboard
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8000)
