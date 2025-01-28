from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from bs4 import BeautifulSoup
from googletrans import Translator
import re
app = Flask(__name__)



FILE = os.path.join('ficheros_csv','traducido_gl_es.csv')  # Cambia "data.csv" por la ruta real de tu archivo
FILE_PARSER = os.path.join('ficheros_csv','traducido_gl_es_original.csv')  # Cambia "data.csv" por la ruta real de tu archivo

COLUMNS = {
    'Source_language': 'Source language (GL)',
    'Target_language': 'Target language (ES)',
    'check': 'check',
}

translator = Translator()
def get_data():
    # Cargar los datos desde el archivo CSV
    data = pd.read_csv(FILE)
    original_columns = data.columns.tolist()
    
    if COLUMNS['check'] not in data.columns: data[COLUMNS['check']] = False
        
    # Cambiar nombre de la columna source y target
    
    data.rename(columns={
        COLUMNS['Source_language']: 'Source_language',
        COLUMNS['Target_language']: 'Target_language',
        }, inplace=True)
    
    data = data[['ID (do not edit)','Content type','Element type','Source_language', 'Target_language']]
    
    if 'index' not in data.columns: data.reset_index(inplace=True)
    
    return data

data = get_data()

@app.route('/')
def index():
    global data
    data = get_data()
    # Renderizar la tabla con textos y sus índices
    return render_template('index.html', texts=data.to_dict(orient="records"))


@app.route('/update', methods=['POST'])
def update():
    try:
        global data
        updated_data = request.json  # Lista de filas con índice, texto original y traducción

        # Actualizar el DataFrame
        for row in updated_data:
            idx = int(row['index'])  # Asegúrate de que el índice sea un entero
            data.at[idx, 'Source_language'] = row['original_text']
            data.at[idx, 'Target_language'] = row['translated_text']
            data.at[idx, COLUMNS['check']] = row['check']
        
        
        # Guardar los datos actualizados en el archivo CSV
        data.to_csv(FILE,index=False)

        # Devolver una respuesta JSON válida
        return jsonify({"message": "Datos guardados en bruto guardados correctamente"})

    except Exception as e:
        # Manejar errores del servidor
        return jsonify({"error": str(e)}), 500

@app.route('/save_data_original', methods=['POST'])
def save_data_original():
    try:
        global data
        data.rename(
            columns={
                'Source_language': COLUMNS['Source_language'],
                'Target_language': COLUMNS['Target_language']},
            inplace=True
            )
        
        data = data[['ID (do not edit)','Content type','Element type',COLUMNS['Source_language'], COLUMNS['Target_language']]]
        data = data.loc[:, ~data.columns.duplicated()]
        
        # Guardar los datos actualizados en el archivo CSV
        data.to_csv(FILE_PARSER, index=False)

        # Devolver una respuesta JSON válida
        return jsonify({"message": "Datos originales guardados correctamente"})

    except Exception as e:
        # Manejar errores del servidor
        return jsonify({"error": str(e)}), 500

@app.route('/edit_text/<int:index>/<string:column>')
def edit_text(index, column):
    # Verificar si el índice existe
    if index not in data.index:
        return jsonify({"error": "Índice no encontrado en el DataFrame"}), 404

    # Obtener el HTML desde el DataFrame
    html = data.loc[index][column]

    # Validar que el HTML sea válido
    try:
        if not isinstance(html, str) or html.strip() == '':
            return render_template('edit.html', text=html, index=index, column=column)

        # Procesar y formatear el HTML
        soup = BeautifulSoup(html, "html.parser")
        formatted_html = soup.prettify()

        # Renderizar el HTML formateado en el template
        return render_template('edit.html', text=formatted_html, index=index, column=column)

    except Exception as e:
        return jsonify({"error": f"Error al procesar el HTML: {str(e)}"}), 500

@app.route('/update_edit', methods=['POST'])
def update_edit():
    try:
        global data
        index = request.args.get('index', type=int)
        updated_text = request.form['text']
        column = request.args.get('column', type=str, default=COLUMNS['Source_language'])

        # Verificar si el índice existe
        if index not in data.index:
            return jsonify({"error": "Índice no encontrado en el DataFrame"}), 404

        # Actualizar el DataFrame
        data.at[index, column] = updated_text

        # Guardar los datos actualizados en el archivo CSV
        data.to_csv(FILE, index=False)

        # Renderizar la tabla actualizada
        return render_template('index.html', texts=data.to_dict(orient="records"))

    except Exception as e:
        # Manejar errores del servidor
        return jsonify({"error": str(e)}), 500


@app.route('/translate_text', methods=['POST'])
def translate_text():
    try:
        index = int(request.json['index'])
        column = request.json['translate_to']
        
        # Verificar si el índice existe
        if index not in data.index:
            return jsonify({"error": "Índice no encontrado en el DataFrame"}), 404

        if column == 'Source_language':
            dest_idioma = COLUMNS['Source_language'].split('(')[1].split(')')[0].lower()
            src_idioma = COLUMNS['Target_language'].split('(')[1].split(')')[0].lower()
            colums_source = 'Target_language'
        elif column == 'Target_language':
            src_idioma = COLUMNS['Source_language'].split('(')[1].split(')')[0].lower()
            dest_idioma = COLUMNS['Target_language'].split('(')[1].split(')')[0].lower()
            colums_source = 'Source_language'
            
        text = data.loc[index][colums_source]
        if not isinstance(text, str) or text.strip() == '':
            translated_text = translator.translate(tag, src=src_idioma, dest=dest_idioma).text
        
        else:
            soup = BeautifulSoup(text, "html.parser")
            # Traducir el contenido de las etiquetas
            word_pattern = re.compile(r'[a-zA-Z]{2,}')  # Al menos dos letras, incluyendo ñ y caracteres acentuados


            for tag in soup.find_all(string=True):  # Encuentra solo texto, ignora las etiquetas
                if word_pattern.search(tag):  # Ignorar cadenas vacías o espacios en blanco
                    translated_text = translator.translate(tag, src=src_idioma, dest=dest_idioma).text
                    tag.replace_with(translated_text)

            translated_html = str(soup)
            
        data.at[index, column] = translated_html
        
        return jsonify(
                {   
                    "message": "Datos originales guardados correctamente",
                    "translated_text": translated_html
                }
            )

    except Exception as e:
        # Manejar errores del servidor
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
