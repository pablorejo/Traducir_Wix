# Uso

Esta guía muestra cómo utilizar las herramientas del proyecto.

## Traducción básica
```python
from translate_data_frame import traducir_data_frame, apis

traducir_data_frame(
    API=apis['Microsoft'],
    source_lenguage='gl',
    target_language='es',
    inpunt_file='export_gl.csv',
    output_path='traducido_es.csv'
)
```

## Proteger palabras
```python
do_not = ['Wix', 'Xogo de fíos']
traducir_data_frame(
    API=apis['Microsoft'],
    source_lenguage='gl',
    target_language='es',
    inpunt_file='export_gl.csv',
    output_path='traducido_es.csv',
    do_not_translate=do_not
)
```

## Interfaz de revisión
Lanza la aplicación Flask para revisar y editar traducciones:
```bash
python review_columns.py
```
La interfaz permite:
- Buscar y reemplazar palabras.
- Marcar traducciones como validadas.
- Editar HTML individualmente.
- Traducir una celda concreta usando Google Translate.

La aplicación espera archivos CSV en la carpeta `ficheros_csv`.
