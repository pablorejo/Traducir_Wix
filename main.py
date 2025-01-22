import pandas as pd
import traductor
import os
import time, math
import tqdm
import difflib

MAX_CHARS = 5000

def traducir_data_frame(
    source_lenguage:str, target_language:str, data, others_languages = [],
    source_column = 'Source', target_column='Target',
    save=True,output_path = 'traducido.csv'):
    
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
        if pd.isnull(row[columns['Target']]) and not pd.isnull(row[columns['Source']]):
            text = row[columns[source_column]]
            
            text_length = len(text)
            
            response = traductor.detect_language([text])
            try:
                idioma = response[0]['language']
            except:
                continue

            
            if idioma not in [target_language, source_lenguage] + others_languages:
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
        
        traducciones = traductor.translate_text(traducir, idioma, target_language)
        
        for i, index in enumerate(indices):
            # print(f"Traduciendo {idioma} a {target_language}")
            # diff = difflib.unified_diff(
            #     traducir[i].splitlines(), 
            #     traducciones[i]['translations'][i]['text'].splitlines(), 
            #     lineterm=''
            # )
            # for line in diff:
            #     print(line)
            data.at[index, columns[target_column]] = traducciones[i]['translations'][0]['text']
        barra_de_carga.update(1)
            
    if save:
        # Guardar el archivo traducido
        
        data.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Archivo traducido guardado en: {output_path}")
    return data

if __name__ == "__main__":
    # Cargar el archivo
    file_path = os.path.join('ficheros_csv', 'export_es.csv')
    data = pd.read_csv(file_path, encoding='utf-8')
    
    data_gl = traducir_data_frame(
        data=data,save=False,source_lenguage='gl',target_language='gl',
        target_column='Source',source_column='Source',
        others_languages=['es'])
    
    
    data_traducida = traducir_data_frame(
        data=data_gl,save=True,source_lenguage='gl',target_language='es',
        target_column='Target',source_column='Source')
    exit()
