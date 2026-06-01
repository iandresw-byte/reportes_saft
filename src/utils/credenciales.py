
import configparser
import os
from pathlib import Path
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

CONFIG_FILE = BASE_DIR / "config.ini"


class ManejadorCredenciales:

    @staticmethod
    @staticmethod
    def guardar(usuario: str, password: str):

        config = configparser.ConfigParser()

        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE, encoding="utf-8")

        if "LOGIN" not in config:
            config["LOGIN"] = {}

        config["LOGIN"]["usuario"] = usuario
        config["LOGIN"]["password"] = password

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            config.write(f)

    @staticmethod
    def cargar() -> dict:
        config = configparser.ConfigParser()

        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE, encoding="utf-8")

            return {
                "usuario": config.get("LOGIN", "usuario", fallback=""),
                "password": config.get("LOGIN", "password", fallback="")
            }

        return {
            "usuario": "",
            "password": ""
        }

    @staticmethod
    def borrar():
        config = configparser.ConfigParser()

        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE, encoding="utf-8")

        if "LOGIN" not in config:
            config["LOGIN"] = {}

        config["LOGIN"]["usuario"] = ''
        config["LOGIN"]["password"] = ''

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            config.write(f)
