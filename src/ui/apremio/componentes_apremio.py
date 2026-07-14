from datetime import date
import flet as ft
from flet import DataTable
from src.ui.components.ui_botones import create_boton
from src.ui.components.ui_calendario import create_fecha
from src.ui.components.ui_table import table_requeridos, controles_paginacion, table_identifiacion_top, table_identifiacion_top_ics
from src.ui.components.ui_dropbox import dd_num_registros, dropbox_aldeas, dropbox_barrios
from src.ui.components.ui_text import create_texFiel_fijas, create_text_data_general_labes, create_text_data_general_titulo
from src.ui.components.ui_colors import color_texto, color_bg_2
from src.ui.components.ui_cards import card_generales, card_mora, card_proceso

texto_color = color_texto()
bg_color = color_bg_2()


def botones_apremio(vista):
    return [
        # create_boton("Aviso de Cobro", ),
        create_boton("1er Requerimiento", vista.abril_modal_apremio_1er),
        create_boton("2do Requerimiento", vista.abril_modal_apremio_2do),
        create_boton("Certificaciones de Falta de Pago",
                     vista.abril_modal_apremio_cerificacion),
        dd_num_registros(vista)
    ]


def botones_contribuyente(vista):
    return [
        # create_boton("Aviso de Cobro", ),
        create_boton("Iniciar Proceso", vista.generar_apremio_pdf_individual),


    ]


def busqueda_identificacion(vista):
    fecha = date.today()
    anio = fecha.year
    mes = fecha.month
    vista.cod_aldea = ft.Ref[ft.Dropdown]()
    vista.cod_barrio = ft.Ref[ft.Dropdown]()
    vista.val_min = ft.Ref[ft.TextField]()
    vista.nombre_aldea = ""
    vista.nombre_barrio = ""

    def handle_change_fecha_min(e):
        vista.fecha_minima = e.control.value.strftime('%Y%m%d')
        btn_fecha_min.text = e.control.value.strftime('%d-%m-%Y')
        btn_fecha_min.update()

    def handle_dismissal_min(e):
        btn_fecha_min.text = date(
            year=anio, month=mes, day=1).strftime('%d/%m/%Y')
        btn_fecha_min.update()

    def handle_aldea(e):
        cod_aldea = vista.cod_aldea.current.value
        if cod_aldea == "%":
            vista.nombre_aldea = "Todos Las Aldeas"
            cod_aldea = None
        else:
            for fila in data_aldeas:
                if fila['CodAldea'] == dropbox_aldea.value:
                    vista.nombre_aldea = fila['NombreAldea']
                    continue
        data_barrio = vista.aldeas.obtener_barrio(cod_aldea)
        data_barrio.insert(0,
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

    btn_fecha_min = create_fecha(
        vista, "Fecha Inicial", vista.fecha_minima, handle_change_fecha_min, handle_dismissal_min)
    txt_minimo = create_texFiel_fijas(
        "Valor Minimo", read_only=False, value="0.00", ref=vista.val_min, width=200)
    txt_minimo.width = 150
    data_aldeas = vista.aldeas.obtener_aldeas()
    dropbox_aldea = dropbox_aldeas(data_aldeas, vista.cod_aldea)
    dropbox_aldea.width = 200
    dropbox_aldea.on_change = handle_aldea
    data_barrio = vista.aldeas.obtener_barrio()
    dropbox_barrio = dropbox_barrios(data_barrio, vista.cod_barrio)
    dropbox_barrio.width = 200
    dropbox_barrio.on_change = handle_barrio
    boton = create_boton("Consultar", vista.consulta_identificacion)
    return ft.Row([
        # create_boton("Aviso de Cobro", ),
        btn_fecha_min,
        txt_minimo,
        dropbox_aldea,
        dropbox_barrio,
        boton
    ],
        alignment=ft.MainAxisAlignment.CENTER)


def tabla_requeridos(vista) -> DataTable:
    return table_requeridos(vista, vista.df, vista.pagina_actual, vista.filas_por_pagina)


def tabla_identificacion_bi(vista) -> DataTable:
    return table_identifiacion_top(vista, vista.df_identificacion_mora_bi, vista.pagina_actual, vista.filas_por_pagina)


def tabla_identificacion_ics(vista) -> DataTable:
    return table_identifiacion_top_ics(vista, vista.df_identificacion_mora_ics, vista.pagina_actual, vista.filas_por_pagina)


def tabla_identificacion_ip(vista) -> DataTable:
    return table_identifiacion_top(vista, vista.df_identificacion_mora_ip, vista.pagina_actual, vista.filas_por_pagina)


def tabla_identificacion_sp(vista) -> DataTable:
    return table_identifiacion_top(vista, vista.df_identificacion_mora_sp, vista.pagina_actual, vista.filas_por_pagina)


def tabla_identificacion_pp(vista) -> DataTable:
    return table_identifiacion_top(vista, vista.df_identificacion_mora_pp, vista.pagina_actual, vista.filas_por_pagina)


def tabla_paginacion(vista):
    return controles_paginacion(vista, vista.df, vista.pagina_actual, vista.filas_por_pagina)


def cerate_data_general(vista):
    return card_generales(vista, vista.data_contribuyente)


def cerate_data_general_mora(vista):
    return card_mora(vista, vista.data_contribuyente)


def cerate_data_general_proceso(vista):
    return card_proceso(vista, vista.data_contribuyente_proceso)
