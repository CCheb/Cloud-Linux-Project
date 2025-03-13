import socket
import threading
import psutil
import json

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_metrics(self):
        metrics = {
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "network_sent": psutil.net_io_counters().bytes_sent,
            "network_recv": psutil.net_io_counters().bytes_recv,
        }
        return json.dumps(metrics)

    def handle_client(self, conn):
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                response = self.get_metrics()
                conn.sendall(response.encode('utf-8'))
            except:
                break
        conn.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn,))
            thread.start()

if __name__ == "__main__":
    server = Server("10.0.3.2", 5000)
    server.start()
