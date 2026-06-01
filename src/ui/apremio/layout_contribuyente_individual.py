import flet as ft
from src.ui.components.ui_colors import color_bg_2, color_texto
from src.ui.components.ui_text import create_texFiel_fijas
from src.ui.components.ui_botones import create_boton
bg_color = color_bg_2()
texto_color = color_texto()


def build_layout_contribuyente(vista, card_generales, card_mora, card_proceso, botones):

    card_datos = card_generales

    mora_card = card_mora

    proceso_card = card_proceso

    return ft.Container(
        padding=20,
        content=ft.Column([
            ft.Row([card_datos, botones]),
            ft.Container(height=10),
            mora_card,
            ft.Container(height=10),
            proceso_card,
        ],
            scroll=ft.ScrollMode.AUTO)
    )
