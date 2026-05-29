import pandas as pd


def encontrar_id_nulo_y_no_int(dataFrame : pd.DataFrame) -> pd.DataFrame:
    return dataFrame[~(dataFrame["id"].apply(lambda x: isinstance(x, int))) | 
                     dataFrame["id"].isna()]
   

def especies_no_permitidas(data:pd.DataFrame) -> pd.DataFrame:
    especies_per = ["perro", "gato", "conejo", "pez", "loro"]
    return data[~(data["especie"].str.lower().isin(especies_per))]


def peso_fuera_rango(data:pd.DataFrame) -> pd.DataFrame:
    return data[~(0.05 < data["peso_kg"] < 120 )]
    
    
def validar_estructuralmente(directorio : str) -> pd.DataFrame:
    pd.read_csv(directorio)
    



    
    

    
    


    
    



