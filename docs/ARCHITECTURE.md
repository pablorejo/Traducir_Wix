# Arquitectura

El proyecto se divide en dos componentes principales:

1. **Motor de traducción**
   - `translate_data_frame.py`: orquesta la traducción de archivos CSV o `pandas.DataFrame`.
   - `traductores/`: conectores a servicios externos.
     - `traductor_microsoft.py`: usa Microsoft Translator y permite excluir palabras.
     - `traductor_open_ai.py`: ejemplo de integración con OpenAI.
   - `conf.py`: constantes globales como `MAX_CHARS` o el modelo de OpenAI.

2. **Interfaz de revisión**
   - `review_columns.py`: aplicación Flask para validar y corregir traducciones.
   - `templates/` y `static/`: recursos HTML, CSS y JS para la UI.

## Diagrama de flujo
```
CSV/DF -> traducir_data_frame -> traductor_microsoft | traductor_open_ai -> CSV traducido
                                                 \
                                                  \-> review_columns (Flask UI)
```

## Estructura del repositorio
```
├── conf.py
├── translate_data_frame.py
├── traductores/
│   ├── traductor_microsoft.py
│   └── traductor_open_ai.py
├── review_columns.py
├── templates/
└── static/
```
