import pandas as pd
import pipeline_ingesta.ingesta as ingesta
import logging_utils.logging_utils as lgu
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import os

logger = lgu.configurar_logger("limpieza")

carpeta_data = "data/clean"




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


def crear_columna_outlier_detectado(df, columna = "peso_kg"):
    z_scaler = StandardScaler()
    z_scores = z_scaler.fit_transform(df[[columna]]).ravel()
   
    df["es_outlier_peso_kg"] = ((z_scores > 3) | (z_scores < -3))

    return df


def detectar_id_duplicado_logging(columna_es_id):
    valores_repetidos = columna_es_id.value_counts()
    id_duplicados = valores_repetidos[valores_repetidos > 1]




    






def estandarizar_columna_especie(df: pd.DataFrame):
    
    nombres_gato_incorre = ["cat", "gata", "gáto", "gató"]
    nombre_gato_correcto = "gato"

    df["especie"] = df["especie"].str.lower()

    df["especie"] = df["especie"].replace(nombres_gato_incorre, nombre_gato_correcto)

    return df



def imputar_edad_años_con_media_especie(df : pd.DataFrame):

    

    df_age_year_mean = df.groupby(["especie"], sort=False)["edad_años"].transform("mean")


    df["edad_años"] = df["edad_años"].fillna(df_age_year_mean)

    return df

def limpiar(df: pd.DataFrame, nombre_arch) -> str:
    
    df_clean = df.drop_duplicates(subset=["id_mascota"], keep="first")

    df_clean = estandarizar_columna_especie(df_clean)

    df_clean = imputar_edad_años_con_media_especie(df_clean)

    return df_clean

def deteccion(df, nombre_arch):
    detectar_id_duplicado_logging(df["id_mascota"])
    obtener_nulos_por_columna_loggear(df, nombre_arch)
    df_clean = crear_columna_outlier_detectado(df)
    
    return df_clean









def script_limpieza(ruta_arch, sheet_excel_si_excel = None):


    path = Path(ruta_arch)

    if(path.exists()):
        df = ingesta.leer_archivo(ruta_arch, sheet_excel_si_excel)
        

        df_clean = deteccion(df, path.name)

        df_clean = limpiar(df_clean, path.name)


        return lgu.exportar_a_csv(df_clean, path.stem, logger, f"limpieza de {path.stem} exportada a ", carpeta_data)


    else:
        lgu.logger_archivo_inexistente(logger, path.name, "Limpieza")

        raise Exception("ingreso una url inexistente al componente limpieza")
    










    





    



    






