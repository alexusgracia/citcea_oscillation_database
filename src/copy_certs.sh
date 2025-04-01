#!/bin/bash

# Rutas de origen de los certificados
FULLCHAIN_SRC="/etc/letsencrypt/live/citcea.oscillations.upc.edu/fullchain.pem"
PRIVKEY_SRC="/etc/letsencrypt/live/citcea.oscillations.upc.edu/privkey.pem"

# Carpeta destino (local)
DEST_DIR="./certs"

# Crear el directorio destino si no existe
if [ ! -d "$DEST_DIR" ]; then
    echo "Creando el directorio $DEST_DIR..."
    mkdir -p "$DEST_DIR"
fi

# Copiar los archivos (se necesita sudo para leer los archivos originales)
echo "Copiando $FULLCHAIN_SRC a $DEST_DIR..."
sudo cp "$FULLCHAIN_SRC" "$DEST_DIR/"
echo "Copiando $PRIVKEY_SRC a $DEST_DIR..."
sudo cp "$PRIVKEY_SRC" "$DEST_DIR/"

# Cambiar la propiedad a tu usuario (usa $USER para el usuario actual)
echo "Cambiando propietario de los certificados a $USER..."
sudo chown "$USER:$USER" "$DEST_DIR/fullchain.pem" "$DEST_DIR/privkey.pem"

# Ajustar permisos:
# fullchain.pem: lectura para todos (644)
# privkey.pem: lectura solo para el propietario (600)
echo "Ajustando permisos de los certificados..."
chmod 644 "$DEST_DIR/fullchain.pem"
chmod 600 "$DEST_DIR/privkey.pem"

echo "Certificados copiados y configurados correctamente en $DEST_DIR."
