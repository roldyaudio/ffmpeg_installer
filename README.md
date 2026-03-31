# FFmpeg Installer

Script en Python para instalar **FFmpeg en Windows** automáticamente.

El proyecto:
- Verifica si `ffmpeg` ya está disponible en el `PATH`.
- Descarga una build precompilada de FFmpeg desde GitHub.
- Extrae el ZIP en `C:\ffmpeg`.
- Busca la carpeta `bin` con `ffmpeg.exe` y `ffprobe.exe`.
- Agrega esa ruta al `PATH` del usuario.

## Requisitos

- Windows (usa comandos de registro `reg` y `setx`).
- Python 3.10+ (recomendado 3.12).
- Conexión a Internet para descargar FFmpeg.

## Instalación

1. Clona este repositorio.
2. Instala dependencias:

```bash
pip install -r requirements.txt
```

## Uso

Ejecuta:

```bash
python main.py
```

Si FFmpeg ya está instalado, el script lo detecta y no vuelve a descargarlo.

## ¿Qué hace internamente?

`main.py` realiza este flujo:
1. Intenta ejecutar `ffmpeg -version`.
2. Si no existe, descarga un ZIP de FFmpeg.
3. Lo extrae en `C:\ffmpeg`.
4. Recorre carpetas hasta ubicar la ruta `bin` válida.
5. Agrega esa ruta al `PATH` del usuario con `setx`.
6. Elimina el ZIP descargado.

## Nota importante

Después de actualizar el `PATH`, abre una **nueva** terminal (CMD/PowerShell) para que los cambios tengan efecto.

## Dependencias

- `requests` (descarga del archivo ZIP)

## Estructura del proyecto

- `main.py`: instalación principal de FFmpeg.
- `lib_installer.py`: utilidades para validar/instalar dependencias de `requirements.txt`.
- `requirements.txt`: dependencias de Python.
