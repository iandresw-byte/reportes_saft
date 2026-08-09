import flet as ft
from src.ui.components.ui_boton_constancias import create_boton_constancia


def botones_uma(vista):
    return ft.Column([
        ft.Row([
            create_boton_constancia(
                "Tasa\nAmbiental", on_click=vista.abrir_licencia_ambiental_modal),

        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
    ],
        alignment=ft.MainAxisAlignment.CENTER
    )


def botones_tributaria(vista):
    return []


def botones_catastro(vista):
    return []


def botones_secretaria(vista):
    return []
