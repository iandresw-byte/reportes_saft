import flet as ft
from src.ui.components.ui_botones import create_boton_salir_modal, create_boton_aceptar
from src.ui.components.ui_text import create_sub_titulo_modal, create_texFiel_fijas, create_titulo_modal
from src.ui.components.ui_colors import color_bg


def abrir_tarjeta_unica(vista, e):
    vista.identidad = ft.Ref[ft.TextField]()


    txt_dni = create_texFiel_fijas(
        "Numero de DNI o RTM.", read_only=False, ref=vista.identidad)
    txt_dni.value = "0101197200627"
    btn_aceptar = create_boton_aceptar()
    btn_aceptar.on_click = vista.generar_ver_tarjeta_unica
    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal("Tarjeta Unica de Contribuyente")
    txt_sub_titulo = create_sub_titulo_modal("Ingrese el numero de Documento Nacional de Identificacion (DNI) o Registro Tributario Municipal (RTM)")
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
                txt_dni,
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
