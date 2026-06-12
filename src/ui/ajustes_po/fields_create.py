
from flet import FontWeight, RadioGroup, Row, CrossAxisAlignment, MainAxisAlignment, Text, Icons, Ref, TextAlign
from src.ui.components.ui_botones import create_boton
from src.ui.components.ui_radio import create_radio
from src.ui.components.ui_text import create_texFiel_fijas


def from_fields_create(vista):
    width = 400
    muni = vista.datos_muni_admin
    return [
        create_texFiel_fijas('No. de Recibo', value="",
                             width=width,  disabled=True),
        create_texFiel_fijas('No. de Permiso', value="",
                             width=width, disabled=True),
        create_texFiel_fijas('Periodo', value="", width=width, disabled=True),
        create_texFiel_fijas('Inicio Operacion', value="",
                             width=width, disabled=True),
        create_texFiel_fijas('Telefono', value="",
                             width=width,  disabled=True),
        create_texFiel_fijas('Numero de Renovacion',
                             value="", width=width,  disabled=True),
        create_texFiel_fijas('R.T.N', value="", width=width,  disabled=True),
        create_texFiel_fijas('R.T.M.', value="", width=width,  disabled=True),
        create_texFiel_fijas('Fecha Emision', value="",
                             width=width,  disabled=True),
        create_texFiel_fijas('Nombre del Establecimiento',
                             value="", width=width, disabled=True),
        create_texFiel_fijas('Nombre del Propietario',
                             value="", width=width, disabled=True),
        create_texFiel_fijas('Identidad del Propietario',
                             value="", width=width, disabled=True),
        create_texFiel_fijas('Direccion', value="",
                             width=width, disabled=True),
        create_texFiel_fijas('Clave Catastral', value="",
                             width=width, disabled=True),
        create_texFiel_fijas('Actividad Economica',
                             value="", width=width, disabled=True),
        create_texFiel_fijas('Tipo Establecimiento',
                             value="", width=width, disabled=True),
    ]


def create_titulo(vista):
    return Text(
        "PERMISO DE OPERACION DE NEGOCIOS",
        size=24,
        weight=FontWeight.BOLD,
        color=vista.texto_color,
        text_align=TextAlign.CENTER,
    )


def create_botones_gestion(vista):
    return [
        create_boton(
            "Guardar",
            width=130,
            disabled=True,
            on_click=vista.guardar_recibo_po),
        create_boton(
            "Imprimir",
            width=130,
            disabled=True,
            on_click=vista.imprimir_rept_po),
        create_boton(
            "Horario Venta de Alcohol",
            width=130,
            disabled=False,
            on_click=vista.abrir_modal_venta_bebida),
        create_boton("Editar", width=130, disabled=True)
    ]


def create_solicitud():
    return RadioGroup(disabled=True, content=ft.Row(
        [create_radio(value="Apertura", label_text="Apertura"),
         create_radio(value="Renovacion", label_text="Renovación")],),
    )


def create_tipo_firma_eza(vista):
    return RadioGroup(disabled=False, value='0',
                      on_change=vista.is_firma_justicia, content=Row([
                          create_radio(value="0", label_text="Ninguno"),
                          create_radio(
                              value="1", label_text="Firma Justicia Municipal"),
                          create_radio(value="2", label_text="Firma Unidad Ambiental")],),
                      )


def create_horiario_alcohol(vista):
    return RadioGroup(disabled=True, value='0', on_change=vista.is_firma_justicia,
                      content=Row([create_radio(value="0", label_text="Ninguno"),
                                   create_radio(
                                       value="1", label_text="¿Horario Venta de Alcohol?"),
                                   create_radio(value="2", label_text="No se Permite la Venta")],),
                      )
