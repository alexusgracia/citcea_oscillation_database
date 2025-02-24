from flask import Flask, render_template, jsonify
import json

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

if __name__ == "__main__":
    app.run(debug=True)
