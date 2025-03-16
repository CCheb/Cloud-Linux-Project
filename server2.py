import os
import json
import psutil
import time
from flask import Flask, jsonify

PIPE_PATH = "/tmp/server2_pipe"  # Pipe for metrics
LOG_PATH = "/tmp/server2_log.json"  # Log for historical data

app = Flask(__name__)

# Ensure the pipe exists
if not os.path.exists(PIPE_PATH):
    os.mkfifo(PIPE_PATH)

def get_metrics():
    """Fetch system metrics."""
    metrics = {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "network_sent": psutil.net_io_counters().bytes_sent,
        "network_recv": psutil.net_io_counters().bytes_recv,
        "timestamp": time.time()
    }
    return metrics

def write_to_pipe():
    """Continuously write system metrics to a named pipe and log the data."""
    while True:
        metrics = get_metrics()
        with open(LOG_PATH, 'a') as log_file:
            log_file.write(json.dumps(metrics) + "\n")

        try:
            with open(PIPE_PATH, 'w') as pipe:
                pipe.write(json.dumps(metrics) + "\n")
        except BrokenPipeError:
            pass  # No reader, but keep running

        time.sleep(2)  # Update every 2 seconds

@app.route("/metrics")
def serve_metrics():
    """Read latest metrics from pipe and serve them over HTTP."""
    try:
        with open(PIPE_PATH, 'r') as pipe:
            return jsonify(json.loads(pipe.readline().strip()))
    except:
        return jsonify({"error": "Unable to read from pipe"}), 500

@app.route("/historical-metrics")
def serve_historical_metrics():
    """Read historical data from log file."""
    try:
        with open(LOG_PATH, 'r') as log_file:
            logs = [json.loads(line.strip()) for line in log_file.readlines()]
        return jsonify(logs)
    except:
        return jsonify({"error": "Unable to read log file"}), 500

if __name__ == "__main__":
    import threading
    threading.Thread(target=write_to_pipe, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)  # Runs HTTP server restricting access to client only
