

import configparser
import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

CONFIG_FILE = BASE_DIR / "config.ini"


class Config:

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")

    @classmethod
    def obtener(cls, seccion, clave, log=None, default=""):
        if log:
            log.error(f"CONFIG_FILE {CONFIG_FILE}")
            log.info(f"CONFIG_FILE {CONFIG_FILE}")
        return cls.config.get(seccion, clave, fallback=default)

    @staticmethod
    def guardar_ruta_google(ruta_google: str):

        config = configparser.ConfigParser()

        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE, encoding="utf-8")

        if "RUTAS" not in config:
            config["RUTAS"] = {}

        config["RUTAS"]["carpeta_unidad_google"] = ruta_google

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            config.write(f)

    @staticmethod
    def guardar_ruta_reportes(ruta_google: str):

        config = configparser.ConfigParser()

        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE, encoding="utf-8")

        if "RUTAS" not in config:
            config["RUTAS"] = {}

        config["RUTAS"]["carpeta_reportes"] = ruta_google

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            config.write(f)

    @staticmethod
    def guardar_tamanio_reporte(tamanio_reporte: str):

        config = configparser.ConfigParser()

        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE, encoding="utf-8")

        if "APREMIO" not in config:
            config["APREMIO"] = {}

        config["APREMIO"]["tipo_documento"] = tamanio_reporte

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            config.write(f)
    @staticmethod
    def guardar_cargo_firma(cargo_1 :str| None = None,
                            firma_1 :str| None = None,
                            cargo_2 :str| None = None,
                            firma_2 :str| None = None,
                            numfirmas: str| None = None):
    
            config = configparser.ConfigParser()
    
            if os.path.exists(CONFIG_FILE):
                config.read(CONFIG_FILE, encoding="utf-8")
    
            if "APREMIO" not in config:
                config["APREMIO"] = {}
            if numfirmas:
                config["APREMIO"]["numfirmas"] = numfirmas
            if cargo_1:
                config["APREMIO"]["cargo_1"] = cargo_1
            if cargo_2:
                config["APREMIO"]["cargo_2"] = cargo_2
            if firma_1:
                config["APREMIO"]["firma_1"] = firma_1
            if firma_2:
                config["APREMIO"]["firma_2"] = firma_2
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                config.write(f)