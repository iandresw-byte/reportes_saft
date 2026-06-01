import flet as ft
from src.ui.components.ui_botones import create_boton_salir_modal
from src.ui.components.ui_text import create_sub_titulo_modal,  create_titulo_modal
from src.ui.components.ui_colors import color_bg


def abrir_datos_actualizados(vista, e, titulo, mensaje):

    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(titulo)
    txt_sub_titulo = create_sub_titulo_modal(
        mensaje)
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                ft.Divider(),

            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            col=12,
            alignment=ft.MainAxisAlignment.CENTER,         # centra verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centra horizontalmente
            expand=True
        ),
        actions=[
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
