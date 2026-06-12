import flet as ft

from src.ui.components.ui_container import create_container, create_row


def build_layout_create(titulo, fields, btn_consulta, rd_firma, rd_tipo_solcitud, contenedor_botones,):

    conten_create = create_container(
        expand=True,
        col=12,
        controls=[
            ft.Image(src=r"\assets\saft.png"),
            titulo,
            ft.Divider(),
            create_row([fields[0], btn_consulta]),
            ft.Divider(),
            create_row(
                [fields[1], fields[2], fields[3], fields[4], fields[5]]),
            create_row([fields[6], fields[7], fields[8],]),
            create_row([fields[9]],),
            create_row([fields[10], fields[11]],),
            create_row([fields[12], fields[13]],),
            create_row([fields[14], fields[15]],),
            ft.Divider(),
            create_row([
                rd_firma,
                rd_tipo_solcitud,
            ],
            ),
            ft.Divider(),
            create_row(contenedor_botones,
                       ),
        ],
    )

    return ft.Container(
        expand=True,
        content=ft.ResponsiveRow(
            expand=True,
            controls=[
                conten_create,
            ],
            alignment=ft.MainAxisAlignment.CENTER, col=12
        )
    )
