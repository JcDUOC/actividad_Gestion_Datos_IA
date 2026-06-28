import sys
import os 

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.resolve()))

os.chdir(str(Path(__file__).parent.parent.resolve()))


import pipeline_ingesta.ingesta as inge
import pipeline_limpieza_transformacion.limpieza as limp






ruta_ingesta_recien, hoja_ingesta_excel = "data/raw/mascotas.csv", None

ruta_limpieza = limp.script_limpieza(ruta_ingesta_recien, None)

