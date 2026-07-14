
import flet as ft
from src.ui.components.ui_colors import color_bg, color_bg_2
from src.utils.config_manager import Config
_color_bg = color_bg()
_color_bg_2 = color_bg_2()


def habilitar_fields(vista):
    rd = vista.radios[0]
    rd.disabled = False
    rd.update()
    vista.botones.controls[1].disabled = False
    vista.botones.controls[2].disabled = False
    vista.botones.controls[1].bgcolor = _color_bg
    vista.botones.controls[2].bgcolor = _color_bg
    vista.botones.controls[1].update()
    vista.botones.controls[2].update()
    for field in vista.filds_form:
        field.read_only = False
        field.disabled = False
        field.update()


def deshabilitar_fields(vista):
    rd = vista.radios[0]
    rd.disabled = True
    rd.update()
    vista.botones.controls[1].disabled = True
    vista.botones.controls[2].disabled = True
    vista.botones.controls[1].bgcolor = _color_bg_2
    vista.botones.controls[2].bgcolor = _color_bg_2
    vista.botones.controls[1].update()
    vista.botones.controls[2].update()
    for field in vista.filds_form:
        field.read_only = True
        field.disabled = True
        field.update()


def actualizar(vista):
    data = []
    rd = vista.radios[0]
    for field in vista.filds_form:
        data.append(field.value)
    data.append(rd.value)
    return vista.app.administracion_service.actualizar_admin(data)


def file_picker_result(vista, e: ft.FilePickerResultEvent):

    if not e.path:
        return

    ruta_google = e.path

    vista.txt_ruta_google.value = ruta_google
    vista.txt_ruta_google.update()

    Config.guardar_ruta_google(ruta_google)


def file_picker_result_reportes(vista, e: ft.FilePickerResultEvent):

    if not e.path:
        return

    ruta = e.path

    vista.txt_ruta_reportes.value = ruta
    vista.txt_ruta_reportes.update()

    Config.guardar_ruta_reportes(ruta)
