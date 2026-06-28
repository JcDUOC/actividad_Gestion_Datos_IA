import logging_utils.logging_utils as lgu
import pandas as pd
import json

logger = lgu.configurar_logger("transformacion")


def obtener_archivo_json(ruta : str):
    with open(ruta, "r", encoding = "utf-8") as f:
        json_ = json.load(f)

    return json_




def obtener_rango_peso_por_fila(columna_peso : str, fila : pd.Series, rangos_peso_especie_raza):
    

    raza = fila["raza"].lower()

    especie = fila["especie"].lower()

    peso = fila[columna_peso]

    for k, v in rangos_peso_especie_raza[especie][raza].items():
        if(v[0] is None):
            if v[1] >= peso:
                return k
        elif((v[1] is None)):
            if(v[0] <= peso):
                return k
        else:
            if(v[0] <= peso <= v[1]):
                return k
            



def crear_columna_rango_peso_por_especie_raza(df : pd.DataFrame, columna_peso : str) -> pd.DataFrame:
    rangos_peso_especie_raza=obtener_archivo_json("pipeline_limpieza_transformacion/rangos_peso_por_especie_raza.json")
    nueva_columna = "rango_peso"
    rangos_peso = []
    indexes = []

    for i, f in df.iterrows():
       rango_peso = obtener_rango_peso_por_fila(columna_peso, f, rangos_peso_especie_raza)
       indexes.append(i)
       rangos_peso.append(rango_peso)


    columna_rango_peso = pd.Series(data = rangos_peso, index=indexes, name=nueva_columna)

    df[nueva_columna] = columna_rango_peso

    return df


