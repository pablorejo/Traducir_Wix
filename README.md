# 🌐 Traducir Wix

[![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![Dependencies](https://img.shields.io/badge/dependencies-pinned-blue)](requirements.txt)

## Descripción
**ES:** Herramientas para automatizar la traducción de contenidos de sitios Wix usando servicios como Microsoft Translator u OpenAI.

**EN:** Tools to automate Wix site translations leveraging services such as Microsoft Translator or OpenAI.

## Índice
- [Instalación](#instalación)
- [Uso básico](#uso-básico)
- [Ejemplos avanzados](#ejemplos-avanzados)
- [Arquitectura](#arquitectura)
- [API](#api)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)
- [English Summary](#english-summary)

## Instalación
Instala rápidamente:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> Consulta [docs/INSTALL.md](docs/INSTALL.md) para instrucciones detalladas, incluido el uso de `pyproject.toml`.

## Uso básico
Traduce un CSV de origen a destino con Microsoft Translator:

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

Más ejemplos en [docs/USAGE.md](docs/USAGE.md).

## Ejemplos avanzados
- Proteger palabras que no deben traducirse.
- Revisar y editar traducciones vía interfaz web (`review_columns.py`).

Consulta [docs/USAGE.md](docs/USAGE.md#ejemplos-avanzados).

## Arquitectura
El proyecto se organiza en módulos independientes para la traducción y la revisión:
```
Traducir_Wix/
├── translate_data_frame.py
├── traductores/
│   ├── traductor_microsoft.py
│   └── traductor_open_ai.py
├── review_columns.py
├── templates/
└── static/
```
Detalles en [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## API
Funciones y endpoints documentados en [docs/API.md](docs/API.md).

## Contribuir
¿Quieres colaborar? Lee [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) y envía tu PR.

## Licencia
Este proyecto está bajo licencia [MIT](LICENSE).

## Contacto
- 📧 Email: `info@example.com`
- 🐦 Twitter: [@example](https://twitter.com/example)

## English Summary
Quick start for international users:
1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. Use `traducir_data_frame` to translate CSV data or launch `review_columns.py` to review translations.

For detailed docs see the `/docs` folder.
