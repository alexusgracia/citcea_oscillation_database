#!/bin/bash

# Definir variables
VENV_PATH="./venv"  # Ruta del entorno virtual
APP_SCRIPT="app.py"  # Nombre del script de la aplicación
LOG_FILE="flask.log"  # Archivo de log

# Buscar el proceso que ejecuta app.py (solo el primer PID)
PID=$(pgrep -f "$APP_SCRIPT" | head -n 1)

# Si hay un proceso en ejecución, matarlo
if [[ -n "$PID" && "$PID" =~ ^[0-9]+$ ]]; then
    echo "Deteniendo el proceso $PID..."
    kill "$PID"
    sleep 3  # Esperar que el proceso termine
    if ps -p "$PID" > /dev/null; then
        echo "Proceso no terminó, forzando con kill -9"
        kill -9 "$PID"
    fi
else
    echo "No se encontró ningún proceso ejecutando $APP_SCRIPT."
fi

# Verificar que el entorno virtual existe
if [ ! -d "$VENV_PATH" ]; then
    echo "El entorno virtual no existe en $VENV_PATH"
fi

# Activar el entorno virtual
source "$VENV_PATH/bin/activate"

# Iniciar la aplicación en segundo plano con nohup y redirigir la salida
echo "Running app..."
nohup bash -c "source $VENV_PATH/bin/activate && python3 $APP_SCRIPT" > "$LOG_FILE" 2>&1 &

# Capturar el PID del nuevo proceso
NEW_PID=$!
echo "Nueva instancia en ejecución con PID: $NEW_PID"

# Salir del entorno virtual
deactivate

echo "Proceso finalizado. Ver logs en $LOG_FILE."

#sleep 1
#cat "$LOG_FILE"


