
import tempfile
import requests
import os
import time
import zipfile
import shutil
URL_ZIP = "https://drive.usercontent.google.com/download?id=1bDADZxcmucEOb-hslTmxnPGrU_mh_ZNK&export=download&authuser=0&confirm=t&uuid=f77b9191-d60b-428a-88d9-ea56411f35ac&at=AAINaILXE0gUl6rcAgIjrIUrjL7K%3A1781056956858"
EXCLUDE = ["config.ini", "user_data",]


def descargar_actualizacion(url=None):
    if not url:
        url = URL_ZIP

    tmp_dir = tempfile.mkdtemp(prefix="update_")
    zip_path = os.path.join(tmp_dir, "update.zip")
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(1024 * 256):
                if chunk:
                    f.write(chunk)

    if zipfile.is_zipfile(zip_path):
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(tmp_dir)
        time.sleep(0.5)
        return tmp_dir


def reemplazar_archivos(src_dir,):

    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        APP_DIR = r"C:\Program Files (x86)\SAFT\reportes_py"
        print(rel_path)
        dest_dir = os.path.join(APP_DIR)
        os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            if any(ex in root for ex in EXCLUDE) or file in EXCLUDE:
                continue
            if file.endswith(".zip"):
                continue
            src = os.path.join(root, file)
            dst = os.path.join(dest_dir, file)
            # Reintentos si el archivo está bloqueado
            for intento in range(5):
                try:
                    shutil.copy2(src, dst)
                    break
                except PermissionError as e:
                    print(e)
                    time.sleep(0.5)
                except Exception as e:
                    break
