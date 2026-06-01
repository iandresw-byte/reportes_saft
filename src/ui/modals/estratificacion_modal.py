import flet as ft
from src.ui.components.ui_radio import rd_estratificacion
from src.ui.components.ui_botones import crear_boton_excel, create_boton_pdf, create_boton_salir_modal
from src.ui.components.ui_text import create_sub_titulo_modal, create_texFiel_fijas, create_titulo_modal
from src.ui.components.ui_colors import color_bg


def abrir_modal_estratificacion(vista, e) -> ft.AlertDialog:
    vista.tipo_empresa = ft.Ref[ft.RadioGroup]()
    vista.anio = ft.Ref[ft.TextField]()
    txt_anio = create_texFiel_fijas(
        "Año Estratificacion", read_only=False, ref=vista.anio)
    radio_group = rd_estratificacion(vista.tipo_empresa)
    btn_excel = crear_boton_excel()
    btn_excel.on_click = vista.generar_excel_estratificacion
    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(
        "Clasificación de establecimientos por su estatificación económica")
    txt_sub_titulo = create_sub_titulo_modal(
        "Seleccione el tipo:")
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                txt_anio,
                radio_group,
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
            btn_excel,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
