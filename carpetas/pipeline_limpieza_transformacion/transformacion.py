import logging_utils.logging_utils as lgu
import pandas as pd
import json
import pipeline_ingesta.ingesta as inge
import numpy as np
from pathlib import Path

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


def parsear_a_date_time(df : pd.DataFrame, columna : str):

    df[columna] = pd.to_datetime(df[columna], errors="coerce", yearfirst=True, format="ISO8601")

    return df


def nueva_columna_mes_annio(df : pd.DataFrame, columna_fecha_hora : str):

    df["consulta_mes_año"] = df["fecha_consulta"].dt.strftime("%m/%Y")

    return df




def obtener_annos_duenno_cliente(df : pd.DataFrame, columna_duenno, duenno, columna_fecha_consulta, fecha_consulta):

    fechas_consulta = df[(df[columna_duenno] == duenno) & (df[columna_fecha_consulta] < fecha_consulta)][columna_fecha_consulta].sort_values()

    annos_cliente = (fechas_consulta.iloc[-1] - fechas_consulta.iloc[0] ) / np.timedelta64(1, "Y")

    return annos_cliente 


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

def parsear_datetime_nueva_columna_mes_annio(df: pd.DataFrame, columna_fecha_hora : str):
    df_nuevo = parsear_a_date_time(df, columna_fecha_hora)

    df_nuevo = nueva_columna_mes_annio(df_nuevo, columna_fecha_hora)

    return df_nuevo


def nueva_columna_annios_atendido(df : pd.DataFrame, columna_dueno = "dueño_email", columa_fecha_consulta = "fecha_consulta", nueva_columna = "años_cliente"):

    indexes = []
    anios_cliente_list = []

    for i, r in df.iterrows():
        indexes.append(i)

        anios_cliente = obtener_annos_duenno_cliente(df, columna_dueno, r[columna_dueno], columa_fecha_consulta, r[columa_fecha_consulta])

        anios_cliente_list.append(anios_cliente)

    df[nueva_columna] = pd.Series(anios_cliente_list, index=indexes)

    return df












def script_transformacion(file_path : str, carpeta_exportacion = "data/transform"):

    path = Path(file_path)

    if(path.exists()):
        df = inge.leer_archivo(file_path, None)
        columna_peso = "peso_kg"
        columna_fecha = "fecha_consulta"

        df_trans = crear_columna_rango_peso_por_especie_raza(df, columna_peso)
        df_trans = parsear_datetime_nueva_columna_mes_annio(df, columna_fecha)
        df_trans = pd.get_dummies(df_trans, columns="especie", sparse=True)
        df_trans = nueva_columna_annios_atendido(df_trans)

        return lgu.exportar_a_csv(df_trans, path.stem, logger, f"tranformacion de {path.stem} exportada a ", carpeta_exportacion, "_transformed")
    else:
        lgu.logger_archivo_inexistente(logger, path.name, "transformacion")

       






    