import pandas as pd
from traductores import traductor_open_ai, traductor_microsoft
import os
import time, math
import tqdm
import difflib

MAX_CHARS = 5000

apis = ['Microsoft', 'OpenAI']

COLUMNS = {
    'Source': 'Source',
    'Target': 'Target'
}

def traducir_data_frame(API:str,
    source_lenguage:str, target_language:str, others_languages = [],
    source_column = 'Source', target_column='Target',
    save=True,output_path = 'traducido.csv',inpunt_file='source_language.csv',data=None,ten_en_cuenta=''):
    """
    Traduce un DataFrame de pandas de un idioma a otro, detectando automáticamente el idioma de origen.
    
    Args:
        source_lenguage (str): Idioma de origen.
        target_language (str): Idioma de destino.
        others_languages (list, optional): Lista de otros idiomas que pueden estar presentes en los datos. Por defecto es una lista vacía.
        source_column (str, optional): Nombre de la columna que contiene el texto de origen. Por defecto es 'Source'.
        target_column (str, optional): Nombre de la columna donde se guardará el texto traducido. Por defecto es 'Target'.
        save (bool, optional): Si es True, guarda el DataFrame traducido en un archivo CSV. Por defecto es True.
        output_path (str, optional): Ruta del archivo CSV donde se guardará el DataFrame traducido. Por defecto es 'traducido.csv'.
        inpunt_file (str, optional): Ruta del archivo CSV de entrada que contiene los datos a traducir. Por defecto es 'source_language.csv'.
        data (pandas.DataFrame, optional): DataFrame de pandas que contiene los datos a traducir. Si es None, se leerá desde el archivo `inpunt_file`.
    
    Returns:
        pandas.DataFrame: DataFrame con los textos traducidos.
    """
    
    if data is None:
        data = pd.read_csv(inpunt_file, encoding='utf-8')
    
    paquetes = []
    indices = {}
    traducir = {}
    current_chars = {}
    
    columns = []
    
    names_columns = data.columns
    columns = {}
    for column_name in names_columns:
        if 'Source' in column_name:
            columns['Source'] = column_name
        if 'Target' in column_name:
            columns['Target'] = column_name
    
    barra_dectectar_idioma = tqdm.tqdm(total=len(data), desc='Empaquetando y detectando idioma')
    
    for index, row in data.iterrows():
        if not pd.isnull(row[columns[source_column]]):
            text = row[columns[source_column]]
            
            text_length = len(text)
            
            if API == apis[0]:
                response = traductor_microsoft.detect_language([text])
                idioma = response[0]['language']
            elif API == apis[1]:
                idioma = source_lenguage
                
            if idioma not in indices: indices[idioma] = []
            if idioma not in traducir: traducir[idioma] = []
            if idioma not in current_chars: current_chars[idioma] = 0
            
            if current_chars[idioma] + text_length > MAX_CHARS:
                paquetes.append((traducir[idioma],indices[idioma],idioma))
                indices[idioma] = []
                traducir[idioma] = []
                current_chars[idioma] = 0
            
            indices[idioma].append(index)
            traducir[idioma].append(text)
            current_chars[idioma] += text_length
        barra_dectectar_idioma.update(1)
         
    
    barra_de_carga = tqdm.tqdm(total=len(paquetes), desc='Traduciendo')
    for paquete in paquetes:
        
        traducir, indices, idioma = paquete
        
        
        if API == apis[0]:
            traducciones = traductor_microsoft.translate_text(traducir, idioma, target_language)
        elif API == apis[1]:
            
            traducciones = traductor_open_ai.translate_text(traducir, idioma, target_language, ten_en_cuenta=ten_en_cuenta)
            
        for i, index in enumerate(indices):
            data.at[index, columns[target_column]] = traducciones[i]['translations'][0]['text']
        barra_de_carga.update(1)
            
    if save:
        # Guardar el archivo traducido
        
        data.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Archivo traducido guardado en: {output_path}")
    return data

if __name__ == "__main__":
    # Cargar el archivo
    file_path = os.path.join('ficheros_csv', 'traducido.csv')
    
    original = 'gl'
    translate = 'es'
    
    lista_palabras = ['Xogo de fios', 'Lorena Quintas Rejo', 'Name of persons' , 'places like "A coruña"']  # Lista de palabras que no se deben traducir
    ten_en_cuenta = f' This word should not be translated: {", ".join(lista_palabras)}'
    
    
    # data_gl = traducir_data_frame(API=apis[1],
    #     save=True,source_lenguage=original,target_language=original,
    #     target_column='Source',source_column='Source',
    #     others_languages=['es'],inpunt_file=file_path,output_path='traducido_gl.csv')
    
            
    data_traducida = traducir_data_frame(API=apis[1],inpunt_file=file_path,
        save=True,source_lenguage=original,target_language=translate,
        target_column=COLUMNS['Target'],source_column=COLUMNS['Source'],output_path='traducido_gl_es.csv',ten_en_cuenta=ten_en_cuenta)
    
    exit(0)
