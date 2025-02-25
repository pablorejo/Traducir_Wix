# Traductor para paginas creadas en wix
## Implementación

### API
Tendremos que usar alguna API que nos permita traducir el texto de un idioma al otro y tenemos dos posibilidades:
1. [Azure](#azure): usar azure y el servicio `Traductor`. 
2. [OpenAI](#openai): usar `chatGPT-4o` para traducir pasandole una serie de instrucciones.

Para elegir la API tendremos que configurarla en el [main.py](main.py) 
#### Azure
Para usar el programa primero tendremos que tener una maquina de azure donde tengamos la api de traducción.
##### Variables de entorno
Tendremos que btener las claves y el location y crear un fichero .env donde tengamos.

```bash
microsoft_key1="clave_1"
microsoft_key2="clave_2"
microsoft_location="location"
```

#### OpenAI
Para usar el programa con openAI primero es imprescindible tener una clave de uso para usarlo que a fecha de creación de este documento la única forma es pagando.
En la documentación se nos explica como tenemos que exportarla para que la use nuestro programa.



### Entorno python
Para poder usar el repositorio recomendamos crear un entorno virtual de python y instalar los requerimientos en este.


1. Crear un entorno virtual
```bash
python -m venv venv
```

2. Activar el entorno virtual
* En Windows
``` Bash
venv\Scripts\activate
```

* En macOS/Linux
``` bash
source venv/bin/activate
```

3. Instalar los requerimientos
```bash
pip install -r requirements.txt
```


### Configuración
En el main tenemos la funcion [translate_text](main.py) que tiene la siguiente estructura.

```python
def traducir_data_frame(
    API,
    source_lenguage:str, target_language:str, others_languages = [],
    source_column = 'Source', target_column='Target',
    save=True,output_path = 'traducido.csv',inpunt_file='source_language.csv',data=None,ten_en_cuenta='')
```

Donde cada una de sus componentes es la siguiente:
* `API` (str): Api que usaremos para la traducción, (openAI o Azure).
* `source_lenguage` (str): Idioma de origen.
* `target_language` (str): Idioma de destino.
* `others_languages` (list, optional): Lista de otros idiomas que pueden estar presentes en los datos. Por defecto es una lista vacía.
* `source_column` (str, optional): Nombre de la columna que contiene el texto de origen. Por defecto es 'Source'.
* `target_column` (str, optional): Nombre de la columna donde se guardará el texto traducido. Por defecto es 'Target'.
* `save` (bool, optional): Si es True, guarda el DataFrame traducido en un archivo CSV, el path es `output_file`. Por defecto es True.
* `output_path` (str, optional): Ruta del archivo CSV donde se guardará el DataFrame traducido. Por defecto es 'traducido.csv'.
* `inpunt_file` (str, optional): Ruta del archivo CSV de entrada que contiene los datos a traducir. Por defecto es 'source_language.csv'.
* `data` (pandas.DataFrame, optional): DataFrame de pandas que contiene los datos a traducir. Si es None, se leerá desde el archivo `inpunt_file`.
* `ten_en_cuenta` (str): En la API de openAI podemos usar este campo para idicarle mas funcionalidades como por ejemplo palabras que no queremos traducir etc, ejm: "do not translate 'A Coruña'".

Que devuelve?
* Devuelve un `data frame` con las columnas ya traducidas.

