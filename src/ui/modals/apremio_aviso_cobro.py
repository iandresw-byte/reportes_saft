import flet as ft
from datetime import date
from src.ui.components.ui_radio import rd_tipo_persona
from src.ui.components.ui_dropbox import dropbox_aldeas, dropbox_barrios, dd_tipo_impuesto
from src.ui.components.ui_calendario import create_fecha
from src.ui.components.ui_botones import create_boton_pdf, create_boton_salir_modal
from src.ui.components.ui_text import create_sub_titulo_modal, create_titulo_modal, create_texFiel_fijas
from src.ui.components.ui_colors import color_bg, color_texto
texto_color = color_texto()


def abrir_modal_aviso_cobro(vista, e):

    vista.tipo_impuesto = ft.Ref[ft.RadioGroup]()
    vista.tipo_persona = ft.Ref[ft.RadioGroup]()
    vista.cod_aldea = ft.Ref[ft.Dropdown]()
    vista.cod_barrio = ft.Ref[ft.Dropdown]()
    vista.num_avisos = ft.Ref[ft.Dropdown]()
    vista.mora_mayor = ft.Ref[ft.Dropdown]()
    vista.nombre_aldea = ""
    vista.nombre_barrio = ""
    fecha = date.today()
    anio, mes = fecha.year, fecha.month

    def handle_change_fecha(e):
        vista.fecha_minima = e.control.value.strftime('%Y%m%d')
        fecha_minima.text = e.control.value.strftime('%d-%m-%Y')
        fecha_minima.update()

    def handle_dismissal(e):
        fecha_minima.text = date(anio, mes, 1).strftime('%d/%m/%Y')
        fecha_minima.update()

    fecha_minima = create_fecha(
        vista,
        "Fecha Minima",
        vista.fecha_minima,
        handle_change_fecha,
        handle_dismissal
    )

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
    data_aldeas = vista.aldeas.obtener_aldeas()
    dropbox_aldea = dropbox_aldeas(data_aldeas, vista.cod_aldea)
    data_barrio = vista.aldeas.obtener_barrio('%')
    dropbox_barrio = dropbox_barrios(data_barrio, vista.cod_barrio)
    dropbox_barrio.on_change = handle_barrio
    dropbox_aldea.on_change = handle_aldea
    num_requerimientos = create_texFiel_fijas(value='10',
                                              label_text="Cantidad a Imprimir:", read_only=False, ref=vista.num_avisos)

    saldo_mayor = create_texFiel_fijas(value='0.00',
                                       label_text="Saldo Total Mayor A:", read_only=False, ref=vista.mora_mayor)

    radio_tipo_impuesto = dd_tipo_impuesto(vista.tipo_impuesto)
    radio_tipo_persona = rd_tipo_persona(vista.tipo_persona)

    btn_pdf = create_boton_pdf()
    btn_pdf.on_click = vista.generar_aviso_cobro
    btn_salir = create_boton_salir_modal()

    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(
        "AVISO DE COBRO")
    txt_sub_titulo = create_sub_titulo_modal("Seleccione el Tipo de Impuesto")
    txt_sub_titulo_2 = create_sub_titulo_modal("Tipo de Persona")
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[

                ft.Divider(),
                txt_sub_titulo,
                radio_tipo_impuesto,
                ft.Divider(),
                ft.Row([num_requerimientos, fecha_minima, saldo_mayor]),

                ft.Divider(),
                dropbox_aldea,
                dropbox_barrio,
                ft.Divider(),
                txt_sub_titulo_2,
                radio_tipo_persona,
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
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
