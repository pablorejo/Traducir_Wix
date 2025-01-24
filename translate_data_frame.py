import pandas as pd
from traductores import traductor_microsoft
import os
import tqdm
import asyncio
from conf import *
import platform

apis = {
        'Microsoft' : 1, 
        'OpenAI': 0
    }

COLUMNS = {
    'Source': 'Source',
    'Target': 'Target'
}

# traductor_open_ai.model = MODEL
def detectar_idioma(text: str, API:str):
    if API == apis['Microsoft']:
        response = traductor_microsoft.detect_language([text])
        return response[0]['language']
    else:
        return None
    
        
    
def traducir_data_frame(API:str,
    source_lenguage:str, target_language:str,
    source_column = 'Source', target_column='Target',
    save=True,output_path = 'traducido.csv',inpunt_file='source_language.csv',data=None,do_not_translate=[]):
    
    output_path = os.path.join('ficheros_csv', output_path)
    inpunt_file = os.path.join('ficheros_csv', inpunt_file)
    
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
    
    
    for index, row in tqdm.tqdm(data.iterrows(), total=len(data), desc='Empaquetando y detectando idioma'):
        if not pd.isnull(row[columns[target_column]]):
            idioma = detectar_idioma(row[columns[target_column]],API)
            if idioma == target_language: continue
                                                             
        if not pd.isnull(row[columns[source_column]]):
            text = row[columns[source_column]]
            
            text_length = len(text)
            
            if idioma is None: idioma = source_lenguage
            
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
         
         
    if API == apis['Microsoft']:
        for paquete in tqdm.tqdm(paquetes, total=len(paquetes), desc='Traduciendo'):
            traducir, indices, idioma = paquete
            traducciones = traductor_microsoft.translate_text(traducir, from_lang=idioma, to_langs=target_language,do_not_translate=do_not_translate)
            for i, index in enumerate(indices):
                data.at[index, columns[target_column]] = traducciones[i]
                
    # elif API == apis['OpenAI']:
    #     barra_de_carga = tqdm.tqdm(total=len(paquetes), desc='Traduciendo')
        
    #     async def translate_async(paquete):
    #         traducir, indices, idioma = paquete
    #         ten_en_cuenta = f' This word should not be translated: {", ".join(do_not_translate)}'
    
    #         traducciones = await traductor_open_ai.translate_text(traducir, idioma, target_language, ten_en_cuenta=ten_en_cuenta)
    #         for i, index in enumerate(indices):
    #             data.at[index, columns[target_column]] = traducciones[i]
    #         barra_de_carga.update(1)

    #     async def main():
    #         tasks = [translate_async(paquete) for paquete in paquetes]
    #         await asyncio.gather(*tasks)

    #     asyncio.run(main())
            
    if save:
        data.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Archivo traducido guardado en: {output_path}")
        
    return data

def play_sound(
        duration = 3,
        freq = 700
    ):
    
    if platform.system() == 'Windows':
        import winsound
        winsound.Beep(freq, duration * 1000)  # winsound.Beep expects duration in milliseconds
    else:
        import os
        os.system(f'play -nq -t alsa synth {duration} sine {freq}')
        
if __name__ == "__main__":
    
    input_file = 'export_es (1).csv'
    
    data_gl = traducir_data_frame(API=apis['Microsoft'],
        save=True,source_lenguage='gl',target_language='gl',
        target_column='Source',source_column='Source'
        ,inpunt_file=input_file,output_path='traducido_gl.csv')
            
            
    lista_palabras = ['Xogo de fíos', 'Lorena Quintas Rejo']
    data_traducida = traducir_data_frame(API=apis['Microsoft'],data=data_gl,
        save=True,source_lenguage='gl',target_language='es',
        target_column=COLUMNS['Target'],source_column=COLUMNS['Source'],output_path='traducido_gl_es.csv',do_not_translate=lista_palabras)
    
    play_sound()
    exit(0)
