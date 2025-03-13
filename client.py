from flask import Flask, render_template, jsonify
import socket
import json

app = Flask(__name__)
SERVERS = ["10.0.1.2", "10.0.2.2", "10.0.3.2"]  # Example server IPs
PORT = 5000
thresholds = {"cpu": 80, "memory": 80, "disk": 80}


def fetch_data(server_ip):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, PORT))
        client_socket.sendall(b"get_metrics")
        data = client_socket.recv(4096).decode('utf-8')
        client_socket.close()
        return json.loads(data)
    except:
        return None


@app.route("/metrics")
def get_metrics():
    all_metrics = {}
    for server in SERVERS:
        metrics = fetch_data(server)
        if metrics:
            all_metrics[server] = metrics
    return jsonify(all_metrics)


@app.route("/thresholds/<metric>/<int:value>", methods=['POST'])
def set_threshold(metric, value):
    if metric in thresholds:
        thresholds[metric] = value
    return jsonify({"message": "Threshold updated", "thresholds": thresholds})


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True, host='10.0.4.2', port=8000)
