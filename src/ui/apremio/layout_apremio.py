import flet as ft


def build_layout(titulo_apremio, contenedor_mosoros, fechas, botones, control_paginas):

    frame_1 = ft.Container(
        expand=True,
        col=10.5,
        content=ft.Column(
            expand=True,
            controls=[
                titulo_apremio,

                contenedor_mosoros,
                control_paginas
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=10
        )
    )

    frame_2 = ft.Container(
        expand=True,
        col=1.5,
        content=ft.Column(
            expand=True,
            controls=[fechas, botones],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

    return ft.Container(
        expand=True,
        col=12,
        content=ft.ResponsiveRow(   # 👈 IMPORTANTE
            controls=[
                frame_1,
                frame_2
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )
