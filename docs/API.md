# API

## Funciones principales
### `traducir_data_frame`
Traduce un `DataFrame` o archivo CSV.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `API` | `str` | Proveedor a usar (`apis['Microsoft']` o `apis['OpenAI']`). |
| `source_lenguage` | `str` | Idioma de origen. |
| `target_language` | `str` | Idioma de destino. |
| `source_column` | `str` | Columna con el texto original. |
| `target_column` | `str` | Columna donde guardar la traducción. |
| `save` | `bool` | Guarda el resultado en CSV si es `True`. |
| `output_path` | `str` | Ruta del archivo de salida. |
| `inpunt_file` | `str` | Archivo de entrada si no se pasa `data`. |
| `data` | `pd.DataFrame` | Datos a traducir. |
| `do_not_translate` | `list` | Palabras que se deben preservar. |

Retorna un `pandas.DataFrame` con las traducciones.

### `traductor_microsoft.translate_text`
Envía paquetes de texto a la API de Microsoft respetando palabras protegidas.

### `traductor_microsoft.detect_language`
Detecta el idioma de una lista de textos.

## Endpoints Flask (`review_columns.py`)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Lista los textos y traducciones cargados desde CSV. |
| `/update` | POST | Guarda en CSV los cambios realizados en la tabla principal. |
| `/save_data_original` | POST | Exporta los datos con sus nombres de columna originales. |
| `/edit_text/<index>/<column>` | GET | Abre un editor HTML para una celda. |
| `/update_edit` | POST | Guarda los cambios del editor HTML. |
| `/translate_text` | POST | Traduce dinámicamente una celda usando Google Translate. |
