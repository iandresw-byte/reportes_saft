
import calendar
import flet as ft
from datetime import date
from src.ui.components.ui_calendario import create_fecha
from src.ui.components.ui_botones import crear_boton_excel, create_boton_pdf, create_boton_salir_modal
from src.ui.components.ui_text import create_sub_titulo_modal, create_titulo_modal
from src.ui.components.ui_colors import color_bg, color_texto


def abrir_modal_rpt_ingresos_depto(vista, e):
    fecha = date.today()
    anio = fecha.year
    mes = fecha.month
    texto_color = color_texto()

    las_day = calendar.monthrange(year=anio, month=mes)[1]

    def handle_change_fecha_ini(e):
        vista.fecha_ini = e.control.value.strftime('%d-%m-%Y')
        btn_fecha_ini.text = e.control.value.strftime('%d-%m-%Y')
        btn_fecha_ini.update()

    def handle_dismissal_ini(e):
        btn_fecha_ini.text = date(
            year=anio, month=mes, day=1).strftime('%d/%m/%Y')
        btn_fecha_ini.update()

    def handle_change_fecha_fin(e):
        vista.fecha_fin = e.control.value.strftime('%d-%m-%Y')
        btn_fecha_fin.text = e.control.value.strftime('%d-%m-%Y')
        btn_fecha_fin.update()

    def handle_dismissal_fin(e):
        btn_fecha_fin.text = date(
            year=anio, month=mes, day=las_day).strftime('%d/%m/%Y')
        btn_fecha_fin.update()

    btn_fecha_ini = create_fecha(
        vista, "Fecha Inicial", vista.fecha_ini, handle_change_fecha_ini, handle_dismissal_ini)
    btn_fecha_fin = create_fecha(
        vista, "Fecha Final", vista.fecha_fin, handle_change_fecha_fin, handle_dismissal_fin)
    btn_excel = crear_boton_excel()
    btn_excel.on_click = vista.generar_excel_ingreso_depto
    btn_pdf = create_boton_pdf()
    btn_pdf.on_click = vista.generar_pdf_ingreso_depto
    btn_salir = create_boton_salir_modal()

    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(
        "Ingresos Generales por Departamento")
    txt_sub_titulo = create_sub_titulo_modal("Periodo a Consultar:")

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
            btn_excel,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
