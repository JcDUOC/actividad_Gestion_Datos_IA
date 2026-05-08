import shutil
import os
import logging
from datetime import datetime
# -- 1. Configurar logging ----------------------------------------
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
level=logging.INFO,
format="%(asctime)s - %(levelname)s - %(message)s",
handlers=[
logging.FileHandler("logs/ingesta.log"), # guarda en archivo
logging.StreamHandler() # muestra en consola
]
)
# -- 2. Funcion de ingesta ----------------------------------------
def ingestar(origen: str, destino_carpeta: str) -> None:
    """Copia un archivo desde origen hacia destino_carpeta."""
    os.makedirs(destino_carpeta, exist_ok=True)
    nombre = os.path.basename(origen)
    destino = os.path.join(destino_carpeta, nombre)
    logging.info(f"Iniciando ingesta: {origen}")
    try:
        shutil.copy(origen, destino)
        logging.info(f"[OK] Archivo copiado a: {destino}")
    except FileNotFoundError:
        logging.error(f"[ERROR] No se encontro el archivo: {origen}")
        raise
# -- 3. Ejecutar --------------------------------------------------
if __name__ == "__main__":
    ingestar("datos_prueba.csv", "data/raw")
    logging.info("Ingesta completada.")