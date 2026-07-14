
from flet import RadioGroup, Row, CrossAxisAlignment, MainAxisAlignment, Icons, Ref, TextField
from src.ui.components.ui_botones import create_boton
from src.ui.components.ui_radio import create_radio
from src.ui.components.ui_text import create_texFiel_fijas


def from_fiels_encargados(vista):
    width = 400
    muni = vista.datos_muni_admin
    return [
        create_texFiel_fijas(
            'Alcalde (sa)', value=muni['Alcalde'], width=width, read_only=True, disabled=True),
        create_texFiel_fijas(
            'Tesoreria', value=muni['Tesorero'], width=width, read_only=True, disabled=True),
        create_texFiel_fijas(
            'Contabilidad', value=muni['Contabilidad'], width=width, read_only=True, disabled=True),
        create_texFiel_fijas(
            'Administrador', value=muni['Administrador'], width=width, read_only=True, disabled=True),
        create_texFiel_fijas(
            'Presupuesto', value=muni['Presupuesto'], width=width, read_only=True, disabled=True),
        create_texFiel_fijas(
            'Tributaria', value=muni['Tributaria'], width=width, read_only=True, disabled=True),
        create_texFiel_fijas(
            'Unidad Ambiental', value=muni['Ambiental'], width=width, read_only=True, disabled=True),
        create_texFiel_fijas(
            'Justicia Municipal', value=muni['Justicia'], width=width, read_only=True, disabled=True),
        create_texFiel_fijas(
            'Auditor', value=muni['Auditor'], width=width, read_only=True, disabled=True),
        create_texFiel_fijas(
            'R.T.N. Muncipalidad', value=muni['RtnEmpresa'], width=width, read_only=True, disabled=True),
        create_texFiel_fijas('Nombre Municipalidad',
                             value=muni['NombreEmpresa'], width=width, read_only=True, disabled=True),
    ]


def radios_predeterminados(vista):
    muni = vista.datos_muni_admin
    return [RadioGroup(disabled=True,
                       value=muni['FirmaPO_1'],
                       content=Row([
                           create_radio(
                               value="0", label_text="Administración Tributaria"),
                           create_radio(
                               value="1", label_text="Tesoreria Municipal"),
                           create_radio(
                               value="2", label_text="Alcalde (sa) Municipal")
                       ],),
                       )]


def btn_ruta_google(vista) -> Row:
    vista.ruta_google_ref = Ref[TextField]()

    vista.txt_ruta_google = create_texFiel_fijas(
        "Ruta Unidad Local de Google ",
        read_only=True,
        value=vista.ruta_google,
        ref=vista.ruta_google_ref
    )

    boton = create_boton(
        "Selelciona la direccion",

        on_click=vista.abrir_file_picker
    )
    boton.icon = Icons.UPLOAD_FILE

    return Row(
        [vista.txt_ruta_google, boton],
        vertical_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.CENTER
    )


def btn_ruta_carpeta_reportes(vista) -> Row:
    vista.ruta_reportes_ref = Ref[TextField]()

    vista.txt_ruta_reportes = create_texFiel_fijas(
        "Ruta Guardar Reportes",
        read_only=True,
        value=vista.ruta_reportes,
        ref=vista.ruta_reportes_ref
    )

    boton = create_boton(
        "Selelciona la direccion",

        on_click=vista.abrir_file_picker_1
    )
    boton.icon = Icons.UPLOAD_FILE

    return Row(
        [vista.txt_ruta_reportes, boton],
        vertical_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.CENTER
    )


def botones(vista) -> Row:
    return Row([
        create_boton("Editar", on_click=vista.habilitar, width=100),
        create_boton("Cancelar", on_click=vista.deshabilitar,
                     width=100, disabled=True),
        create_boton("Guardar", on_click=vista.actualizar,
                     width=100, disabled=True),
    ], vertical_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.CENTER)
