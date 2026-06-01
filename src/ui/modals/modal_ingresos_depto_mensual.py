
import calendar
import flet as ft
from datetime import date
from src.ui.components.ui_text import create_texFiel_fijas
from src.ui.components.ui_botones import crear_boton_excel, create_boton_pdf, create_boton_salir_modal
from src.ui.components.ui_text import create_sub_titulo_modal, create_titulo_modal
from src.ui.components.ui_colors import color_bg, color_texto
from src.ui.components.ui_radio import rd_tipo_factura
from src.ui.components.ui_dropbox import dropbox_departamentos


def abrir_modal_rpt_ingresos_mensual_depto(vista, e):
    vista.anio = ft.Ref[ft.TextField]()
    vista.tipo_impuesto = ft.Ref[ft.RadioGroup]()
    vista.cod_depto = ft.Ref[ft.Dropdown]()
    vista.nombre_depto = ft.Ref[ft.Dropdown]()
    anio_txt = create_texFiel_fijas(
        "Año a consultar", read_only=False, ref=vista.anio)

    data_deptos = vista.app.administracion_service.obtener_deptos()

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

    btn_excel = crear_boton_excel()
    btn_excel.on_click = vista.generar_excel_ingreso_depto
    btn_pdf = create_boton_pdf()
    btn_pdf.on_click = vista.generar_pdf_ingreso_depto_mensual
    btn_salir = create_boton_salir_modal()

    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(
        'Ingresos por Departamento Mensual')
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
                ft.Row([anio_txt],
                       alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                dropbox_deptos,
                ft.Divider(),
                radio_factura,

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
