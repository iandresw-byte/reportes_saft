import flet as ft
import calendar
from datetime import date
from src.ui.components.ui_botones import create_boton_pdf, create_boton_salir_modal
from src.ui.components.ui_text import create_sub_titulo_modal, create_texFiel_fijas, create_titulo_modal
from src.ui.components.ui_calendario import create_fecha
from src.ui.components.ui_colors import color_bg


def abrir_trancicicon_traspaso(vista, e):

    fecha = date.today()
    anio = fecha.year
    mes = fecha.month
    las_day = calendar.monthrange(year=anio, month=mes)[1]

    def handle_change_fecha_ini(e):
        vista.fecha_inicial = e.control.value.strftime('%Y%m%d')
        btn_fecha_ini.text = e.control.value.strftime('%d-%m-%Y')
        btn_fecha_ini.update()

    def handle_change_fecha_fin(e):
        vista.fecha_final = e.control.value.strftime('%Y%m%d')
        btn_fecha_fin.text = e.control.value.strftime('%d-%m-%Y')
        btn_fecha_fin.update()

    def handle_dismissal_ini(e):
        btn_fecha_ini.text = date(
            year=anio, month=mes, day=1).strftime('%d/%m/%Y')
        btn_fecha_ini.update()

    def handle_dismissal_fin(e):
        btn_fecha_fin.text = date(
            year=anio, month=mes, day=las_day).strftime('%d/%m/%Y')
        btn_fecha_fin.update()

    btn_fecha_ini = create_fecha(
        vista, "Fecha Inicial", vista.fecha_inicial, handle_change_fecha_ini, handle_dismissal_ini)
    btn_fecha_fin = create_fecha(
        vista, "Fecha Final", vista.fecha_final, handle_change_fecha_fin, handle_dismissal_fin)

    btn_pdf = create_boton_pdf()
    btn_pdf.on_click = vista.generar_rpt_trancicion_traspaso
    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal("Reporte de Trancicion Y Traspaso")
    txt_sub_titulo = create_sub_titulo_modal("Ingrese las fechas del periodo:")
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                ft.Divider(),
                ft.Row([btn_fecha_ini,
                        btn_fecha_fin],
                       alignment=ft.MainAxisAlignment.CENTER),
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
            btn_pdf,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
    )
