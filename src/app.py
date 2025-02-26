import os
from flask import Flask, render_template, jsonify, send_from_directory
from dotenv import load_dotenv
import json

# Cargar las variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Cargar los datos del archivo JSON
with open("oscillation_data.json", "r") as f:
    data = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    return jsonify(data)

@app.route('/images/<path:filename>')
def static_files(filename):
    return send_from_directory('images', filename)

if __name__ == "__main__":
    port_flask = int(os.getenv("FLASK_RUN_PORT", 8080))	# Toma el puerto del .env o usa 8080 por defecto
    host_flask=os.getenv("FLASK_RUN_HOST", "0.0.0.0")	# Toma el host del .env o usa 0.0.0.0 por defecto
    app.run(debug=True, host=host_flask, port=port_flask)
