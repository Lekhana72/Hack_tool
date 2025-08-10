from flask import Flask, render_template, request, jsonify
import socket

app = Flask(__name__)

def scan_ports(target, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            s.close()
        except Exception:
            pass
    return open_ports

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    target = data.get("target")
    start_port = int(data.get("startPort"))
    end_port = int(data.get("endPort"))

    open_ports = scan_ports(target, start_port, end_port)
    return jsonify({"open_ports": open_ports})

if __name__ == "__main__":
    app.run(debug=True)
