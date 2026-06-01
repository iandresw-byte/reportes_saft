import flet as ft
from src.ui.components.ui_colors import color_bg, color_texto, color_bg_2
from src.ui.components.ui_text import create_texFiel_fijas, create_text_data_general_labes, create_text_data_general_titulo
from src.ui.components.ui_botones import create_boton


def metric_card(title, value, color="#1976D2"):
    return ft.Container(
        padding=20,
        bgcolor=color_bg(),
        border_radius=10,
        expand=True,
        content=ft.Column(
            [
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD),
                ft.Text(value, size=24,
                        weight=ft.FontWeight.BOLD, color=color),
            ],
            spacing=5,
        ),
    )


def card_generales(vista, data_contribuynete):

    vista.identidad = ft.Ref[ft.TextField]()
    contribuyente = data_contribuynete
    txt_bucar = create_texFiel_fijas(
        "Buscar Identidad", read_only=False, ref=vista.identidad)
    btn_buscar = create_boton("Consultar", )
    btn_buscar.on_click = vista.get_contribuyente
    fila = ft.Row([txt_bucar, btn_buscar])

    titulo = create_text_data_general_titulo("Datos del contribuyente")
    if contribuyente:
        direccion = create_text_data_general_labes(
            f"Dirección: {contribuyente["Direccion"]}")
        nombre = create_text_data_general_labes(
            f"Nombre: {contribuyente["Pnombre"]}")
        dni = create_text_data_general_labes(f"DNI: {contribuyente["DNI"]}")
        barrio = create_text_data_general_labes(
            f"Barrio: {contribuyente["NombreBarrio"]}")
        aldea = create_text_data_general_labes(
            f"Aldea: {contribuyente["NombreAldea"]}")
    else:
        direccion = create_text_data_general_labes(f"Dirección: ")
        nombre = create_text_data_general_labes(f"Nombre: ")
        dni = create_text_data_general_labes(f"DNI: ")
        barrio = create_text_data_general_labes(f"Barrio: ")
        aldea = create_text_data_general_labes(f"Aldea: ")
    return ft.Column([
        fila,
        titulo,
        ft.Divider(),
        ft.Row([dni, nombre,]),
        direccion,
        ft.Row([aldea,  barrio,
                ]),
    ])


def card_mora(vista, data_contribuynete):
    mora = data_contribuynete
    if mora:
        mora_bi = mora["bi"]
        titulo = create_text_data_general_titulo("Resumen de Mora")
        mora_saldo = create_text_data_general_labes(
            f"Total Mora: {mora["total"]:,.2f}")
        periodo = create_text_data_general_labes(
            f"Nombre: {str(mora["mes_ini"])}  {str(mora["mes_fin"])}")
    else:
        titulo = create_text_data_general_titulo("Resumen de Mora")
        mora_saldo = create_text_data_general_labes(f"Total Mora:")
        periodo = create_text_data_general_labes(f"Nombre: ")

    return ft.Column([
        titulo,
        ft.Divider(),
        ft.Row([mora_saldo]),
        ft.Row([periodo]),
    ])


def card_proceso(vista, data_contribuyente_proceso):
    proceso = data_contribuyente_proceso

    def step(label, estado):
        color = (
            ft.Colors.GREEN if estado == "Entregado"
            else ft.Colors.ORANGE if estado == "Generado"
            else ft.Colors.GREY
        )

        return ft.Column([
            ft.Icon(ft.Icons.CHECK_CIRCLE if estado == "Entregado" else ft.Icons.CIRCLE,
                    color=color),
            ft.Text(label, size=12),
        ], alignment=ft.MainAxisAlignment.CENTER)

    titulo = create_text_data_general_titulo("Proceso de Cobro")

    if proceso:
        if len(proceso) >= 3:
            step2 = step("1er Requerimiento", proceso[0]["Estado"])
            step3 = step("2do Requerimiento", proceso[1]["Estado"])
            step4 = step("Certificación", proceso[3]["Estado"])
        elif len(proceso) == 2:

            step2 = step("1er Requerimiento", proceso[0]["Estado"])
            step3 = step("2do Requerimiento", proceso[1]["Estado"])
            step4 = step("Certificación", 'No Generado')
        elif len(proceso) == 1:
            step2 = step("1er Requerimiento", proceso[0]["Estado"])
            step3 = step("2do Requerimiento", 'No Generado')
            step4 = step("Certificación", 'No Generado')
        else:

            step2 = step("1er Requerimiento", "No Generado")
            step3 = step("2do Requerimiento", 'No Generado')
            step4 = step("Certificación", 'No Generado')

    else:

        step2 = step("1er Requerimiento", '')
        step3 = step("2do Requerimiento", '')
        step4 = step("Certificación", '')
    return ft.Column([
        titulo,
        ft.Divider(),
        ft.Row([
            step2,
            ft.Container(width=30),
            step3,
            ft.Container(width=30),
            step4
        ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND),

    ])
