
import os
from pathlib import Path
import sys

import flet as ft
from src.ui.components.ui_colors import color_bg, color_bg_2
from src.utils.config_manager import Config
_color_bg = color_bg()
_color_bg_2 = color_bg_2()
import json
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = r"C:\Users\iAndresw\RepositorioLocal\reportes_saft"

def habilitar_fields(vista):
 
    vista.botones.controls[1].disabled = False
    vista.botones.controls[2].disabled = False
    vista.botones.controls[1].bgcolor = _color_bg
    vista.botones.controls[2].bgcolor = _color_bg
    vista.botones.controls[1].update()
    vista.botones.controls[2].update()
    for field in vista.filds_cuentas:
        field.read_only = False
        field.disabled = False
        field.update()


def deshabilitar_fields(vista):

    vista.botones.controls[1].disabled = True
    vista.botones.controls[2].disabled = True
    vista.botones.controls[1].bgcolor = _color_bg_2
    vista.botones.controls[2].bgcolor = _color_bg_2
    vista.botones.controls[1].update()
    vista.botones.controls[2].update()
    for field in vista.filds_cuentas:
        field.read_only = True
        field.disabled = True
        field.update()


def actualizar(vista):
    DIR_JSON= os.path.join(BASE_DIR,  "assets", "json","cuentas_apremio.json")

    cuentas = []

    for campo in vista.filds_cuentas:
        cuentas.append({
            "cta_ingreso": campo.data,
            "nombre": campo.value.strip()
        })

    with open(DIR_JSON, "w", encoding="utf-8") as archivo:
        json.dump(
            cuentas,
            archivo,
            ensure_ascii=False,
            indent=4
        )