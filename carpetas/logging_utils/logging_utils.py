import logging as lg
import os 
import pandas as pd


#esto permite crear un logger para registro de acciones en un archivo externo. Esto para cumplir con el principio 
#de trazabilidad
def configurar_logger(componente: str):
    logger = lg.getLogger(f"Logger de {componente}")
    logger.setLevel(lg.INFO)
    logger.propagate = False

    formato = lg.Formatter("| %(asctime)s --- %(levelname)s --- %(message)s |")
    conshandler = lg.StreamHandler()

    conshandler.setFormatter(formato)

    os.makedirs("logs"  , exist_ok=True)

    handler_archivo = lg.FileHandler(f"logs/logs de {componente}.log", encoding = "UTF-8", errors = "ignore", delay=True)
    handler_archivo.setFormatter(formato)
    logger.addHandler(handler_archivo)

    return logger


### asi se crea el logger, debes pasarle el nombre del componente que lo usa. para hacer uso, 
# se puede hacer con los metodos .info, .error, .warning, .exception, .critical, a los cuales se les debe pasar el mensaje en string.
logging_transformacion_limpieza = configurar_logger("limpieza_transformación")

logging_ingesta = configurar_logger("ingesta")


def logger_archivo_inexistente(logger, nombre_arch, componente_pl):
    logger.warning(f"ingreso una url de un archivo inexistente ({nombre_arch}) al pipeline en el componente {componente_pl}")
    raise Exception(f"entro un archivo inexistente a {componente_pl}")



def exportar_a_csv(df : pd.DataFrame, nombre_arch_sin_extencion, logger : lg.Logger, mensaje, carpeta_data, sufijo = "_clean"):
    os.makedirs(carpeta_data, exist_ok=True)
    nuevo_archivo = f"{nombre_arch_sin_extencion}{sufijo}.csv "
    path_file_new = f"{carpeta_data}/" + nuevo_archivo

    try:
        df.to_csv(path_file_new, index=False, encoding="utf-8", errors="ignore")

        logger.info(mensaje + nuevo_archivo)

        return path_file_new
    except Exception as e:
        logger.exception(f"Error de exportación del archivo {nombre_arch_sin_extencion}_clean.csv: {str(e)}")

        raise Exception(f"Error de exportación del archivo {nombre_arch_sin_extencion}_clean.csv: {str(e)}")








