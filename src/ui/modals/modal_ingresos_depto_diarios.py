
import calendar
import flet as ft
from datetime import date
from src.ui.components.ui_radio import rd_tipo_po
from src.ui.components.ui_dropbox import dropbox_departamentos
from src.ui.components.ui_radio import rd_tipo_factura
from src.ui.components.ui_calendario import create_fecha
from src.ui.components.ui_botones import crear_boton_excel, create_boton_pdf, create_boton_salir_modal
from src.ui.components.ui_text import create_sub_titulo_modal, create_titulo_modal
from src.ui.components.ui_colors import color_bg, color_texto


def abrir_modal_rpt_ingresos_diarios_depto(vista, e):
    vista.tipo_impuesto = ft.Ref[ft.RadioGroup]()
    fecha = date.today()
    anio = fecha.year
    mes = fecha.month

    texto_color = color_texto()
    vista.cod_depto = ft.Ref[ft.Dropdown]()
    vista.nombre_depto = ft.Ref[ft.Dropdown]()

    data_deptos = vista.app.administracion_service.obtener_deptos()

    las_day = calendar.monthrange(year=anio, month=mes)[1]
    cod_depto = 0

    radio_factura = rd_tipo_factura(vista.tipo_impuesto, mostrar_todos=False)
    radio_factura.visible = False

    def handle_deptos(e):
        cod_depto = vista.cod_depto.current.value
        if cod_depto == "%":
            vista.nombre_depto = "Todos Los Deptos"
        else:
            for fila in data_deptos:
                if fila['IdDeptos'] == dropbox_deptos.value:
                    vista.nombre_depto = fila['DeptoDesc']
                    continue
        radio_factura.visible = False
        radio_factura.update()
        if cod_depto == '2':
            radio_factura.visible = True
            radio_factura.update()

    dropbox_deptos = dropbox_departamentos(data_deptos, vista.cod_depto)
    dropbox_deptos.on_change = handle_deptos

    def handle_change_fecha_ini(e):
        vista.fecha_ini = e.control.value.strftime('%Y%m%d')
        btn_fecha_ini.text = e.control.value.strftime('%d-%m-%Y')
        btn_fecha_ini.update()

    def handle_dismissal_ini(e):
        btn_fecha_ini.text = date(
            year=anio, month=mes, day=1).strftime('%d/%m/%Y')
        btn_fecha_ini.update()

    def handle_change_fecha_fin(e):
        vista.fecha_fin = e.control.value.strftime('%Y%m%d')
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
    btn_pdf = create_boton_pdf()
    btn_pdf.on_click = vista.generar_pdf_ingreso_depto_diario
    btn_excel.on_click = vista.generar_excel_ingreso_depto_diario

    btn_salir = create_boton_salir_modal()

    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(
        'Ingresos por Departamento Diario')
    txt_sub_titulo = create_sub_titulo_modal("Periodo a Consultar:")

    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                dropbox_deptos,
                ft.Divider(),
                radio_factura,
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
