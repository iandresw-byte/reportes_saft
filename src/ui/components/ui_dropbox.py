from flet import Dropdown, dropdown, TextStyle, ButtonStyle, Row, MainAxisAlignment, Ref
from src.ui.components.ui_colors import color_texto, color_bg_2, color_borde
from src.ui.components.ui_text import create_text_paginacion
texto_color = color_texto()
border_color = color_borde()
bg_color = color_bg_2()


def dropbox_cuentas_ingreso(cuentas,  ref):
    texto_color = color_texto()
    border_color = color_borde()
    bg_color = color_bg_2()
    cuentas = cuentas

    data_cta = [dropdown.Option(
            data = a,
            key=a["CtaIngreso"],
            text=a["NombreCtaIngreso"],
            text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color),
            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color)))
            for  a in cuentas]
    return Dropdown(
        ref=ref,
        label="Seleccione la cuenta de ingreso",
        width=300,
        options=data_cta,
        color=texto_color,
        border_color=border_color,
        bgcolor=bg_color,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
        text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color))


def dropbox_aldeas(aldeas: list[dict], ref):
    texto_color = color_texto()
    border_color = color_borde()
    bg_color = color_bg_2()
    aldeas.insert(0, {
        'CodAldea': '%', 'NombreAldea': 'Todas Las Aldeas', 'UbicacionAldea': 0})

    data = [dropdown.Option(
            key=str(a["CodAldea"]),
            text=a["NombreAldea"],
            text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color),
            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color)))
            for    
            
            
            a in aldeas]
    return Dropdown(
        ref=ref,
        label="Seleccione la aldea",
        width=300,
        options=data,
        color=texto_color,
        border_color=border_color,
        bgcolor=bg_color,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
        text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color))


def dropbox_departamentos( deptos_municipales: list[dict], ref:Ref, label=None,):
    texto_color = color_texto()
    border_color = color_borde()
    bg_color = color_bg_2()
    if not label:
        label = "Seleccione el Departamento"
    data = [dropdown.Option(
            key=str(a["IdDeptos"]),
            text=a["DeptoDesc"],
            text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color),
            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color)))
            for a in deptos_municipales]
    return Dropdown(
        ref=ref,
        label=label,
        width=300,
        options=data,
        color=texto_color,
        border_color=border_color,
        bgcolor=bg_color,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
        text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color))


def dropbox_barrios(barrios: list[dict], ref):
    texto_color = color_texto()
    border_color = color_borde()
    bg_color = color_bg_2()
    barrios.insert(0,
                   {'CodBarrio': '%', 'NombreBarrio': 'Todos Los Barrios', 'CodAldea': '%'})

    return Dropdown(
        ref=ref,
        label="Seleccione Barrio/Colonia/Caserio",
        width=300,
        options=[dropdown.Option(
            key=str(a["CodBarrio"]),
            text=a["NombreBarrio"],
            text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color),
            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color)))
            for a in barrios],
        color=texto_color,
        border_color=border_color,
        bgcolor=bg_color,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
        text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color))


def horas(label="Hora") -> Dropdown:
    texto_color = color_texto()
    border_color = color_borde()
    bg_color = color_bg_2()
    horas = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
             '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',]
    return Dropdown(
        label=label,
        options=[dropdown.Option(h, text_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color))) for h in horas],
        width=100,
        color=texto_color,
        border_color=border_color,
        bgcolor=bg_color,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
        text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color)
    )


def dias():

    dias = ["LUNES", 'MARTES', 'MIERCOLES',
            'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']
    return Dropdown(
        label="Dias",
        options=[dropdown.Option(m, text_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color))) for m in dias],
        width=100,
        color=texto_color,
        border_color=border_color,
        bgcolor=bg_color,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
        text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color)
    )


def dd_tipo_impuesto(tipo_impuesto):
    return Dropdown(
        ref=tipo_impuesto,
        value="%",
        options=[
            dropdown.Option("0", "Otras Tasas", text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color), style=ButtonStyle(color=texto_color, text_style=TextStyle(
                    size=10, font_family="Tahoma", color=texto_color))),
            dropdown.Option("1", "Bienes Inmuebles", text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color), style=ButtonStyle(color=texto_color, text_style=TextStyle(
                    size=10, font_family="Tahoma", color=texto_color))),
            dropdown.Option("4", "Impuesto Personal", text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color), style=ButtonStyle(color=texto_color, text_style=TextStyle(
                    size=10, font_family="Tahoma", color=texto_color))),
            dropdown.Option("2", "Industria, Comercio y Servicio", text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color), style=ButtonStyle(color=texto_color, text_style=TextStyle(
                    size=10, font_family="Tahoma", color=texto_color))),
            dropdown.Option("5", "Servicios Públicos", text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color), style=ButtonStyle(color=texto_color, text_style=TextStyle(
                    size=10, font_family="Tahoma", color=texto_color))),
            dropdown.Option("7", "Planes de Pago", text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color), style=ButtonStyle(color=texto_color, text_style=TextStyle(
                    size=10, font_family="Tahoma", color=texto_color))),
            dropdown.Option("%", "Todos (General)", text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color), style=ButtonStyle(color=texto_color, text_style=TextStyle(
                    size=10, font_family="Tahoma", color=texto_color))),
        ],
        width=300,
        color=texto_color,
        border_color=border_color,
        bgcolor=bg_color,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
        text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color)
    )


def dd_num_registros(vista) -> Row:
    num_fila = create_text_paginacion("No. Filas")

    dr = Dropdown(
        item_height=10,
        text_size=10,
        width=100,
        value="10",
        options=[
            dropdown.Option("10", text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color),
                            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                                size=10,
                                font_family="Tahoma",
                                color=texto_color))),
            dropdown.Option("15", text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color),
                            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                                size=10,
                                font_family="Tahoma",
                                color=texto_color))),
            dropdown.Option("20", text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color),
                            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                                size=10,
                                font_family="Tahoma",
                                color=texto_color))),

        ], color=texto_color,
        border_color=border_color,
        bgcolor=bg_color,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
        text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color),
        on_change=lambda e: vista.cambiar_filas(int(e.control.value))
    )
    return Row(controls=[num_fila, dr], alignment=MainAxisAlignment.CENTER)
