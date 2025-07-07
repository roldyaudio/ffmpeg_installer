import os
import zipfile
import requests
import subprocess

def download_file(url, local_filename):
    print(f"⬇ Descargando desde {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"✅ Descarga completada: {local_filename}")
    return local_filename

def extract_zip(zip_path, extract_to):
    print(f"📦 Extrayendo {zip_path} a {extract_to}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✅ Extracción completada.")

def find_bin_path(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if 'ffmpeg.exe' in files and 'ffprobe.exe' in files:
            print(f"🔍 Encontrado bin: {root}")
            return root
    return None

def add_to_user_path(new_path):
    # Obtener PATH actual del usuario
    current_path = os.environ.get("PATH", "")
    # Evitar duplicados (case-insensitive en Windows)
    if new_path.lower() in current_path.lower():
        print(f"✅ El PATH ya contiene: {new_path}")
        return
    # Actualizar usando setx (usuario actual)
    print(f"🔧 Agregando {new_path} al PATH del usuario...")
    command = f'setx PATH "{current_path};{new_path}"'
    subprocess.run(command, shell=True)
    print(f"✅ PATH del usuario actualizado con: {new_path}")
    print("📝 Nota: abre una nueva consola CMD o PowerShell para que surta efecto.")

def main():
    url = "https://github.com/GyanD/codexffmpeg/releases/download/2025-07-01-git-11d1b71c31/ffmpeg-2025-07-01-git-11d1b71c31-full_build.zip"
    zip_path = "ffmpeg_full_build.zip"
    extract_dir = r"C:\ffmpeg"

    # Descargar ZIP
    download_file(url, zip_path)

    # Crear carpeta destino si no existe
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    # Extraer ZIP
    extract_zip(zip_path, extract_dir)

    # Buscar carpeta bin
    bin_path = find_bin_path(extract_dir)
    if bin_path:
        add_to_user_path(bin_path)
    else:
        print("⚠️ No se encontró el directorio con ffmpeg.exe y ffprobe.exe. Verifica manualmente.")

    # Borrar ZIP
    os.remove(zip_path)
    print(f"🗑 ZIP eliminado.")

if __name__ == "__main__":
    main()
