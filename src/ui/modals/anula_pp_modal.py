import flet as ft
from src.ui.components.ui_botones import create_boton_salir_modal, create_boton_aceptar
from src.ui.components.ui_text import create_sub_titulo_modal, create_texFiel_fijas, create_titulo_modal
from src.ui.components.ui_colors import color_bg


def abrir_anula_plan_pago(vista, e):
    vista.identidad = ft.Ref[ft.TextField]()
    vista.num_plan_pago = ft.Ref[ft.TextField]()

    txt_num_pp = create_texFiel_fijas(
        "Numero Plan de Pago", read_only=False, ref=vista.num_plan_pago)
    btn_aceptar = create_boton_aceptar()
    btn_aceptar.on_click = vista.anular_plan_pago
    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal("Anular Planes de Pago")
    txt_sub_titulo = create_sub_titulo_modal("Ingrese el numero de plan de pago a anular")
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                ft.Divider(),
  
                ft.Divider(),
                txt_num_pp,
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
            btn_aceptar,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
