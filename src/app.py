import os
from flask import Flask, render_template, jsonify, send_from_directory, request, redirect, url_for, send_file
from dotenv import load_dotenv
import json
import pandas as pd
from io import BytesIO
from datetime import datetime

# Cargar las variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Archivo JSON donde se almacenarán los datos
data_file = "oscillation_data.json"

# Cargar los datos del archivo JSON si existe, si no, crear una lista vacía
if os.path.exists(data_file):
    with open(data_file, "r") as f:
        data = json.load(f)
else:
    data = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    return jsonify(data)

@app.route('/images/<path:filename>')
def static_files(filename):
    return send_from_directory('images', filename)

@app.route("/submit_new_point", methods=["GET", "POST"])
def submit_new_point():
    if request.method == "POST":
        # Obtener los datos del formulario
        new_point = {
            "id": request.form.get("id"),
            "country": request.form.get("country"),
            "Region_state": request.form.get("Region_state"),
            "europe": request.form.get("europe") == "on",
            "repetitive": request.form.get("repetitive") == "on",
            "last_observation": request.form.get("last_observation"),
            "trigger": request.form.get("trigger"),
            "duration": request.form.get("duration"),
            "frequency": request.form.get("frequency"),
            "involved_devices": request.form.get("involved_devices"),
            "propagation": request.form.get("propagation"),
            "distance": request.form.get("distance"),
            "radius": request.form.get("radius"),
            "outages": request.form.get("outages"),
            "identification": request.form.get("identification"),
            "method": request.form.get("method"),
            "purported": request.form.get("purported"),
            "mitigation_measures": request.form.get("mitigation_measures"),
            "images": request.form.getlist("images"),
            "links": request.form.getlist("links"),
            "coordinates": request.form.get("coordinates"),
            "first_observation": request.form.get("first_observation"),
            "grid": request.form.get("grid"),
            "points": json.loads(request.form.get("points", "[]")),
            "connections": json.loads(request.form.get("connections", "[]"))
        }

        # Convertir valores numéricos
        try:
            new_point["id"] = int(new_point["id"])
            new_point["frequency"] = float(new_point["frequency"])
            new_point["distance"] = float(new_point["distance"])
            new_point["radius"] = float(new_point["radius"])
        except ValueError:
            return "Error: Algunos valores deben ser numéricos.", 400

        # Agregar el nuevo punto a la lista de datos
        data.append(new_point)

        # Guardar en el archivo JSON
        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)

        return redirect(url_for("index"))

    return render_template("form.html")

# Nueva ruta para descargar el contenido en formato Excel
@app.route("/download_excel")
def download_excel():


    # Convertir los datos a un DataFrame (asegúrate de que 'data' sea una lista de diccionarios)
    df = pd.DataFrame(data)
    output = BytesIO()

    # Escribir el DataFrame a un archivo Excel en memoria
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Oscillations')
    output.seek(0)

    # Obtener fecha y hora actuales y formatearlas
    now = datetime.now().strftime("%Y%m%d")
    filename = f"oscillations_{now}.xlsx"
    # Enviar el archivo Excel como descarga
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
if __name__ == "__main__":
    port_flask = int(os.getenv("FLASK_RUN_PORT", 8080))  # Toma el puerto del .env o usa 8080 por defecto
    host_flask = os.getenv("FLASK_RUN_HOST", "0.0.0.0")  # Toma el host del .env o usa 0.0.0.0 por defecto
    app.run(debug=True, host=host_flask, port=port_flask)