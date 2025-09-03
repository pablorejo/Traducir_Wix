# Instalación

Sigue estos pasos para configurar el entorno de desarrollo.

## Requisitos previos
- Python 3.10 o superior
- `pip` y `virtualenv`
- Claves de API para [Microsoft Translator](https://azure.microsoft.com/services/cognitive-services/translator/) u [OpenAI](https://platform.openai.com/)

## Entorno virtual
```bash
python -m venv venv
# Activar
#   Windows: venv\Scripts\activate
#   macOS/Linux: source venv/bin/activate
```

## Dependencias
Instala los paquetes necesarios desde `requirements.txt`:
```bash
pip install -r requirements.txt
```

Si prefieres `pyproject.toml`, instala con:
```bash
pip install .
# o
pip install -e .
```

## Variables de entorno
Crea un archivo `.env` con las claves de los proveedores que vayas a usar:
```env
microsoft_key1="<tu_clave>"
microsoft_location="<tu_region>"
openai_api_key="<tu_clave>"
```

> No compartas este archivo ni lo subas al repositorio.

## Verificación
Compila los módulos para asegurarte de que todo está listo:
```bash
python -m py_compile translate_data_frame.py review_columns.py traductores/*.py conf.py
```
