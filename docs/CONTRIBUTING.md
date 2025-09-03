# Guía de contribución

¡Gracias por tu interés en colaborar!

## Cómo empezar
1. Haz un *fork* del repositorio.
2. Clona tu fork:
   ```bash
   git clone https://github.com/<tu_usuario>/Traducir_Wix.git
   cd Traducir_Wix
   ```
3. Crea un entorno virtual e instala las dependencias como se describe en [INSTALL.md](INSTALL.md).
4. Crea una rama descriptiva:
   ```bash
   git checkout -b feat/nueva-funcionalidad
   ```

## Estilo y pruebas
- Sigue las convenciones de PEP8.
- Asegúrate de que `python -m py_compile` no reporte errores.

## Pull Requests
1. Ejecuta los chequeos:
   ```bash
   python -m py_compile translate_data_frame.py review_columns.py traductores/*.py conf.py
   ```
2. Describe claramente los cambios y enlaza issues relacionados.
3. Espera la revisión antes de fusionar.

## Reportar problemas
Utiliza el apartado de [Issues](https://github.com/OWNER/Traducir_Wix/issues) para bugs o solicitudes.

Gracias por contribuir ❤️
