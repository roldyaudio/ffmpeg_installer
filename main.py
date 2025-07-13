from lib_installer import *

install_requirements_in_directory("C:/Apps/ffmpeg_installer")

from time import time
import os
import subprocess
import requests
import zipfile


def download_file(url, local_filename):
    print(f"⬇ Downloading from {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"✅ Download completed: {local_filename}")
    return local_filename

def extract_zip(zip_path, extract_to):
    print(f"📦 Extracting {zip_path} to {extract_to}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✅ Extraction completed.")

def find_bin_path(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if 'ffmpeg.exe' in files and 'ffprobe.exe' in files:
            print(f"🔍 Found bin directory: {root}")
            return root
    return None

def add_to_user_path_2(new_path):
    import subprocess

    result = subprocess.run(
        'reg query "HKCU\\Environment" /v PATH',
        capture_output=True, text=True, shell=True
    )

    if result.returncode != 0:
        current_path = ""
    else:
        lines = result.stdout.splitlines()
        for line in lines:
            if "PATH" in line:
                current_path = line.split("    ")[-1].strip()
                break
        else:
            current_path = ""

    if new_path.lower() in current_path.lower():
        print(f"✅ PATH already contains: {new_path}")
        return

    print(f"Adding {new_path} to the user PATH...")
    command = f'setx PATH "{current_path};{new_path}"'
    subprocess.run(command, shell=True)
    print(f"✅ User PATH updated with: {new_path}")
    # print("\x1b[0;36mNote: open a new CMD or PowerShell window for it to take effect\x1b[0m")

def check_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    """
    Main function:
    - Checks if ffmpeg is already installed and available in the system PATH.
    - If found, prints a green message and exits.
    - If not, downloads, extracts, finds the bin folder, adds it to PATH and notifies the user.
    """
    if check_ffmpeg_installed():
        print("\x1b[1;32m✅ Ffmpeg is already in your system\x1b[0m")
        return

    url = "https://github.com/GyanD/codexffmpeg/releases/download/2025-07-01-git-11d1b71c31/ffmpeg-2025-07-01-git-11d1b71c31-full_build.zip"
    zip_path = "ffmpeg_full_build.zip"
    extract_dir = r"C:\ffmpeg"

    # Download ZIP file
    download_file(url, zip_path)

    # Create destination folder if it doesn't exist
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    # Extract ZIP contents
    extract_zip(zip_path, extract_dir)

    # Look for the bin directory containing ffmpeg.exe and ffprobe.exe
    bin_path = find_bin_path(extract_dir)
    if bin_path:
        add_to_user_path_2(bin_path)
    else:
        print("⚠️ Could not find a directory with ffmpeg.exe and ffprobe.exe. Please check manually.")

    # Delete the downloaded ZIP
    os.remove(zip_path)
    print("ZIP file deleted.")

    print("\x1b[1;32mFfmpeg successfully installed\x1b[0m")
    print("\x1b[0;36mNote: Re-run the App hub launcher to take effect.\x1b[0m")


if __name__ == "__main__":
    main()
