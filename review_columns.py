from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from bs4 import BeautifulSoup
app = Flask(__name__)


FILE = os.path.join('ficheros_csv','traducido_gl_es.csv')  # Cambia "data.csv" por la ruta real de tu archivo

def get_data():
    # Cargar los datos desde el archivo CSV
    # file_out = os.path.join('ficheros_csv','traducido_gl_es_prueba_1.csv')  # Cambia "data.csv" por la ruta real de tu archivo

    data = pd.read_csv(FILE)
    # data.reset_index(inplace=True)  # Agregamos el índice original como columna "index"
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
            data.at[idx, 'Source language (GL)'] = row['original_text']
            data.at[idx, 'Target language (ES)'] = row['translated_text']

        # Guardar los datos actualizados en el archivo CSV
        data.to_csv(FILE, index=False)

        # Devolver una respuesta JSON válida
        return jsonify({"message": "Datos guardados correctamente"})

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
        column = request.args.get('column', type=str, default='Target language (ES)')

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

if __name__ == '__main__':
    app.run(debug=True)
