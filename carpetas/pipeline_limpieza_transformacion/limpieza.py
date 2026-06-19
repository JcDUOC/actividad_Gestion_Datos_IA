import pandas as pd
import pipeline_ingesta.ingesta as ingesta
import logging_utils.logging_utils as lgu
from pathlib import Path
from sklearn.preprocessing import StandardScaler

logger = lgu.configurar_logger("limpieza")



def obtener_nulos_por_columna_loggear(df: pd.DataFrame, nombre_archivo):
    
    def logging_columnas_nulas(dict_columnas_nulos, nombre_archivo):
        mensaje = f"nulos encontrados por columnas en el archivo {nombre_archivo}: "
        
        for k in dict_columnas_nulos.keys():
            mensaje += f" {k} = {dict_columnas_nulos[k]} ;"

        logger.warning(mensaje)

    columnas = df.columns.values
    nulos_columna = {}
    for c in columnas:
        nulos_columna[c] = df[c].isnull().sum()

    
    logging_columnas_nulas(nulos_columna, nombre_archivo)

    return nulos_columna


def crear_columna_outlier_detectado(df):
    columna_buscar_outliers = ["peso_kg"]
    z_scaler = StandardScaler()
    z_scores = z_scaler.fit_transform(df[columna_buscar_outliers])

    df["es_outlier_peso_kg"] = ((z_scores > 3) | (z_scores < -3))

    return df


def detectar_id_duplicado_logging(columna_es_id):
    valores_repetidos = columna_es_id.value_counts()
    id_duplicados = valores_repetidos[valores_repetidos > 1]


    


def deteccion(df, nombre_arch):
    detectar_id_duplicado_logging(df["id_mascota"])
    obtener_nulos_por_columna_loggear(df, nombre_arch)
    df_clean = crear_columna_outlier_detectado(df_clean)
    
    return df_clean







def limpiar(df, nombre_arch, hoja_excel=0) -> str:
    
    df_clean = df.drop_duplicates(subset=["id_mascota"], keep="first")

    



    






