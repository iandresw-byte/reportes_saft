import flet as ft
from src.ui.components.ui_botones import create_boton_aceptar, create_boton_salir_modal
from src.ui.components.ui_text import create_sub_titulo_modal, create_texFiel_fijas, create_titulo_modal
from src.ui.components.ui_colors import color_bg


def abrir_modal_licencia_ics(vista, e) -> ft.AlertDialog:
    vista.num_recibo = ft.Ref[ft.TextField]()

    txt_recibo = create_texFiel_fijas(
        "Numero de Recibo", read_only=False, ref=vista.num_recibo)
    btn_liciencia = create_boton_aceptar()
    btn_liciencia.on_click = vista.generar_pdf_licencia_ambiental_ics
    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(
        "TASA AMBIENTAL\nESTABLECIMEINTOS COMERCIALES")
    txt_sub_titulo = create_sub_titulo_modal(
        "Ingrese el numero de recibo con el que pago la tasa ambiental:")
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                txt_recibo,
                ft.Divider()
            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            col=12,
            alignment=ft.MainAxisAlignment.CENTER,         # centra verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centra horizontalmente
            expand=True
        ),
        actions=[
            btn_liciencia,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
