
from flet import Row, CrossAxisAlignment, MainAxisAlignment,  Icons, TextField, TextStyle
from src.ui.components.ui_botones import create_boton
from src.ui.components.ui_text import create_texFiel_fijas
from src.ui.components.ui_colors import color_texto
text_color = color_texto()


def form_num_recibo(vista):
    return [create_texFiel_fijas("Numero de Recibo Pagado en Otras Tasas", read_only=False, ),]


def form_excel(vista):
    vista.txt_ruta_excel = create_texFiel_fijas(
        "Ruta de Acceso de Planilla",
        read_only=True
    )

    boton = create_boton(
        "Seleccionar Excel",

        on_click=vista.abrir_file_picker
    )
    boton.icon = Icons.UPLOAD_FILE

    return Row(
        [vista.txt_ruta_excel, boton],
        vertical_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.CENTER
    )


def form_botones(vista) -> Row:
    return Row([
        create_boton("Cargar", on_click=vista.procesar_excel, width=100),
        # create_boton("Cancelar", width=100, disabled=True),
        create_boton("Limpiar", on_click=vista.limpiar, width=100),
    ], vertical_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.CENTER)


def caja_progreso() -> TextField:
    return TextField(
        label="Progreso",
        multiline=True,
        read_only=True,
        min_lines=8,
        text_style=TextStyle(size=12, font_family="Tahoma", color=text_color),
        max_lines=15,
        expand=True
    )
