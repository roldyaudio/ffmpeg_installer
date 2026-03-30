import os
import subprocess
import sys
import importlib.metadata # Modern replacement for pkg_resources
from packaging import version # Standard way to handle versions

def ensure_pip():
    """Checks if pip is available; installs it if missing."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                       check=True, capture_output=True)
        print("✅ pip is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ pip not found. Installing with ensurepip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
        print("✅ pip installed successfully.")

def check_ffmpeg_installed():
    """Checks if ffmpeg is accessible in the system PATH."""
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_requirements_in_directory(base_dir):
    """
    Scans for requirements.txt and manages installations.
    Replaces pkg_resources with importlib.metadata for a setuptools-free approach.
    """
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "requirements.txt":
                req_path = os.path.join(root, file)
                print(f"\n🔍 Found requirements: {req_path}")

                with open(req_path, 'r') as f:
                    # Clean lines and ignore comments
                    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

                for req in requirements:
                    # Basic parsing: separates 'package_name' from '>=version'
                    # Works for simple 'package==1.2.3' or 'package' formats
                    pkg_name = req.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].strip()
                    
                    try:
                        # Check if package is installed using standard library
                        dist_version = importlib.metadata.version(pkg_name)
                        print(f"✅ {pkg_name} ({dist_version}) is already installed.")
                        
                        # Note: Deep version comparison (like pkg_resources.require) 
                        # usually requires the 'packaging' library. 
                        # For a lightweight script, checking existence is often enough.
                        
                    except importlib.metadata.PackageNotFoundError:
                        print(f"📦 {req} is not installed. Installing...")
                        result = subprocess.run([sys.executable, "-m", "pip", "install", req])
                        if result.returncode == 0:
                            print(f"✅ Successfully installed {req}")
                        else:
                            print(f"❌ Failed to install {req}")
                            sys.exit(1)

if __name__ == "__main__":
    # The script remains compatible with Python 3.12 logic
    print("🔧 Checking pip...")
    ensure_pip()
    
    target_dir = "C:/Apps/Audio_analyzer"
    if os.path.exists(target_dir):
        print(f"🚀 Processing requirements in {target_dir}...")
        install_requirements_in_directory(target_dir)
    else:
        print(f"⚠️ Directory {target_dir} not found.")
        
    print("✅ Process completed.")
