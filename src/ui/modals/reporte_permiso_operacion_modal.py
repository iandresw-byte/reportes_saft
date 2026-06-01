
import calendar
import flet as ft
from datetime import date
from src.ui.components.ui_radio import rd_tipo_po
from src.ui.components.ui_dropbox import dropbox_aldeas, dropbox_barrios
from src.ui.components.ui_calendario import create_fecha
from src.ui.components.ui_botones import crear_boton_excel, create_boton_pdf, create_boton_salir_modal
from src.ui.components.ui_text import create_sub_titulo_modal, create_titulo_modal
from src.ui.components.ui_colors import color_bg, color_texto


def abrir_modal_rpt_permiso_operacion(vista, e):
    fecha = date.today()
    anio = fecha.year
    mes = fecha.month
    texto_color = color_texto()
    vista.tipo_po = ft.Ref[ft.RadioGroup]()
    vista.cod_aldea = ft.Ref[ft.Dropdown]()
    vista.cod_barrio = ft.Ref[ft.Dropdown]()
    vista.nombre_aldea = ""
    vista.nombre_barrio = ""
    las_day = calendar.monthrange(year=anio, month=mes)[1]

    def handle_change_fecha_ini(e):
        vista.fecha_ini = e.control.value.strftime('%Y%m%d')
        btn_fecha_ini.text = e.control.value.strftime('%d-%m-%Y')
        btn_fecha_ini.update()

    def handle_change_fecha_fin(e):
        vista.fecha_fin = e.control.value.strftime('%Y%m%d')
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

    def handle_aldea(e):
        cod_aldea = vista.cod_aldea.current.value
        if cod_aldea == "%":
            vista.nombre_aldea = "Todos Las Aldeas"
        else:
            for fila in data_aldeas:
                if fila['CodAldea'] == dropbox_aldea.value:
                    vista.nombre_aldea = fila['NombreAldea']
                    continue
        data_barrio = vista.aldeas.obtener_barrio(cod_aldea)
        data_barrio.append(
            {'CodBarrio': '%', 'NombreBarrio': 'Todos Los Barrios', 'CodAldea': '%'})

        dropbox_barrio.options = [ft.dropdown.Option(
            key=str(a["CodBarrio"]),
            text=a["NombreBarrio"],
            text_style=ft.TextStyle(
                size=10, font_family="Tahoma", color=texto_color),
            style=ft.ButtonStyle(color=texto_color, text_style=ft.TextStyle(
                size=10, font_family="Tahoma", color=texto_color)))
            for a in data_barrio]
        dropbox_barrio.update()

    def handle_barrio(e):
        if dropbox_barrio.value == "%":
            vista.nombre_barrio = "Todos Los Barrios"
        else:
            for fila in data_barrio:
                if fila['CodBarrio'] == dropbox_barrio.value:
                    vista.nombre_barrio = fila['NombreBarrio']
                    continue

    radio_tipo_po = rd_tipo_po(vista.tipo_po)
    data_aldeas = vista.aldeas.obtener_aldeas()
    dropbox_aldea = dropbox_aldeas(data_aldeas, vista.cod_aldea)
    dropbox_aldea.on_change = handle_aldea
    data_barrio = vista.aldeas.obtener_barrio('%')

    dropbox_barrio = dropbox_barrios(data_barrio, vista.cod_barrio)
    dropbox_barrio.on_change = handle_barrio
    btn_fecha_ini = create_fecha(
        vista, "Fecha Inicial", vista.fecha_ini, handle_change_fecha_ini, handle_dismissal_ini)
    btn_fecha_fin = create_fecha(
        vista, "Fecha Final", vista.fecha_fin, handle_change_fecha_fin, handle_dismissal_fin)
    btn_excel = crear_boton_excel()
    btn_excel.on_click = vista.generar_pdf_rpt_permiso_operacion
    btn_pdf = create_boton_pdf()
    btn_pdf.on_click = vista.generar_pdf_rpt_permiso_operacion
    btn_salir = create_boton_salir_modal()

    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(
        "Generar Reporte de Permisos de Operación")
    txt_sub_titulo = create_sub_titulo_modal("Seleccione el tipo:")
    txt_sub_titulo_2 = create_sub_titulo_modal("Periodo de emision:")
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                radio_tipo_po,
                ft.Divider(),
                dropbox_aldea,
                dropbox_barrio,
                ft.Divider(),
                txt_sub_titulo_2,
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
            # btn_excel,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
