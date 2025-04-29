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
visits_file = "visits.json"
if os.path.exists(visits_file):
    with open(visits_file, "r") as f:
        visits_data = json.load(f)
        
# Cargar los datos del archivo JSON si existe, si no, crear una lista vacía
if os.path.exists(data_file):
    with open(data_file, "r") as f:
        data = json.load(f)
else:
    data = []

@app.route("/")
def index():
    visits_data["count"] += 1
    with open(visits_file, "w") as f:
        json.dump(visits_data, f, indent=4)
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
        with open(data_file, "w") as file:
            json.dump(data, file, indent=4)

        return redirect(url_for("index"))

    return render_template("form.html")

# Nueva ruta para descargar el contenido en formato Excel
@app.route("/download_excel")
def download_excel():


    # Convertir los datos a un DataFrame
    df = pd.DataFrame(data)
    output = BytesIO()

    columns = [
        'country', 'Region_state', 'last_observation', 'europe', 'repetitive',
        'trigger', 'duration', 'frequency', 'involved_devices', 'propagation',
        'distance', 'radius', 'outages', 'identification', 'method', 'purported',
        'mitigation_measures','possible_mechanism','first_observation', 'grid', 'id' 
    ]
    excluded = [
        'coordinates', 'images', 'links',  'points', 'connections'
    ]
    df = df[columns]


    # Escribir el DataFrame a un archivo Excel en memoria
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Oscillations')

        # Obtener la hoja de trabajo (worksheet)
        workbook = writer.book
        worksheet = writer.sheets['Oscillations']

        # Crear formato con color de fondo PANTONE 3005
        header_format = workbook.add_format({
            'bold': True,               # Negrita
            'font_color': 'white',       # Texto blanco
            'bg_color': '#0077C8',       # Azul PANTONE 3005
            'align': 'center',           # Centrado horizontal
            'valign': 'vcenter',         # Centrado vertical
            'border': 1                  # Borde delgado
        })

        # Aplicar el formato a la primera fila (encabezados)
        for i, col in enumerate(df.columns):
            content_max_length = df[col].astype(str).apply(len).max() + 1  # Longitud máxima del contenido + margen
            title_length = len(col) + 6  # Longitud del título + margen adicional si es más largo
            optimal_width = max(content_max_length, title_length)  # Elegir el más largo entre contenido y título
            worksheet.set_column(i, i, optimal_width)
            worksheet.write(0, i, col.capitalize(), header_format)  # Aplicar formato al titulo y primera letra en mayúscula


        # Ajustar la altura de la primera fila para que el filtro no tape el texto
        worksheet.set_row(0, 20)  # Ajusta la altura de la primera fila

        # Aplicar filtro a la primera fila (desde A1 hasta la última columna con datos)
        worksheet.autofilter(0, 0, 0, len(columns) - 1)

        # Bloquear la primera fila y las 3 primeras columnas
        worksheet.freeze_panes(1, 3)

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
    # Usar rutas absolutas a los certificados
    ssl_context = (
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'certs/fullchain.pem')),
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'certs/privkey.pem'))
    )

    app.run(debug=True, host=host_flask, port=port_flask, ssl_context=ssl_context)