import flet as ft


def build_layout(titulo_apremio, contenedor_mosoros,botones, control_paginas):

    frame_1 = ft.Container(
        expand=True,
        col=12,
        content=ft.Column(
            expand=True,
            controls=[
                titulo_apremio,
                ft.Row(botones),
                contenedor_mosoros,
                control_paginas
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=5
        )
    )

   

    return ft.Container(
        expand=True,
        col=12,
        content=ft.ResponsiveRow(   # 👈 IMPORTANTE
            controls=[
                frame_1,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )
