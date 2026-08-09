import re
import requests
import time
import flet as ft
import subprocess
import os
from src.utils.config_manager import Config
from src.helpers.updater_helper import descargar_actualizacion, reemplazar_archivos
APP_VERSION = Config.obtener("APP", "app_version")


URL_VERSION = "https://raw.githubusercontent.com/iandresw-byte/versionador_saft/refs/heads/main/versiones.py"


class UpdateService:
    def __init__(self, page: ft.Page):
        self.page = page

    def verificar_actualizacion(self, e):
        try:

            version_local = self.leer_version_local()
            version_remota = self.leer_version_remota()

            if version_local != version_remota:
                base_dir = r"C:\Program Files (x86)\SAFT\reportes_py"
                updater_ui = os.path.join(base_dir, "updater.exe")

                if os.path.exists(updater_ui):
                    self.page.open(ft.SnackBar(
                        ft.Text("Iniciando actualización..."), open=True))
                    self.page.update()
                    time.sleep(1)

                    subprocess.Popen([updater_ui], shell=True)
                    self.page.window.close()
                    return
                else:
                    self.page.open(ft.SnackBar(
                        ft.Text(f"⚠ No se encontró el actualizador: {updater_ui}"), open=True))
                    self.page.update()
                    return

            self.page.open(ft.SnackBar(
                ft.Text("Ya cuenta con la última versión disponible"), open=True))
            self.page.update()

        except Exception as ex:
            snackbar = ft.SnackBar(ft.Text(f"❌ Error: {str(ex)}"), open=True)
            self.page.open(snackbar)
            self.page.update()

    def leer_version_remota(self):
        r = requests.get(URL_VERSION, timeout=10)
        r.raise_for_status()
        contenido = r.text
        match = re.search(r'VERSION_APP\s*=\s*["\']([^"\']+)["\']', contenido)
        return match.group(1) if match else "0.0.0"

    def leer_version_local(self):
        return APP_VERSION

    def verificar_actualizacion_inicio(self ,e=None):
        
        
        try:
            version_local = self.leer_version_local()
            version_remota = self.leer_version_remota()
            if version_local != version_remota:
                base_dir = r"C:\Program Files (x86)\SAFT\reportes_py"
                updater_ui = os.path.join(base_dir, "updater.exe")
                if not os.path.exists(updater_ui):
                    tmp_dir = descargar_actualizacion()
                    reemplazar_archivos(tmp_dir,)
                if os.path.exists(updater_ui):
                    time.sleep(1)
                    subprocess.Popen([updater_ui], shell=True)
                    return True
            else:
                return False
        except Exception as ex:
            return False


    

    def actualizacion(self):
        try:
            base_dir = r"C:\Program Files (x86)\SAFT\reportes_py"
            updater_ui = os.path.join(base_dir, "updater.exe")

            if os.path.exists(updater_ui):

                time.sleep(1)

                subprocess.Popen([updater_ui], shell=True)
                self.page.window.close()
                return
            else:

                return

        except Exception as ex:
            return
