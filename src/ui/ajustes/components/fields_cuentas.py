
import os

from flet import RadioGroup, Row, CrossAxisAlignment, Column, MainAxisAlignment, Icons, Ref, TextField
from src.ui.components.ui_botones import create_boton
from src.ui.components.ui_radio import create_radio
from src.ui.components.ui_text import create_texFiel_fijas
from pathlib import Path
import sys

import json
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = r"C:\Users\iAndresw\RepositorioLocal\reportes_saft"
def cargar_cuentas():
    DIR_JSON= os.path.join(BASE_DIR,  "assets", "json","cuentas_apremio.json")
    with open(DIR_JSON, "r", encoding="utf-8") as archivo:
        cuentas = json.load(archivo)

    return {
        cuenta["cta_ingreso"]: cuenta["nombre"]
        for cuenta in cuentas
    }

def botones_cta(vista) -> Row:
    return Row([
        create_boton("Editar", on_click=vista.habilitar, width=100),
        create_boton("Cancelar", on_click=vista.deshabilitar,
                     width=100, disabled=True),
        create_boton("Guardar", on_click=vista.actualizar,
                     width=100, disabled=True),
    ], vertical_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.CENTER)

def from_fiels_cuentas(vista):
    cuentas_dict = cargar_cuentas()
    width_cta = 400
    filas = []
    for cuenta, nombre in cuentas_dict.items():
        campo = create_texFiel_fijas(cuenta, value=nombre, width=width_cta, read_only=True, disabled=True)
        campo.data = cuenta
        filas.append(campo)

    return filas