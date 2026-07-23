import flet as ft


def build_layout_principal( fechas, botones):



    frame_2 = ft.Container(
        expand=True,
        col=12,
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
                frame_2
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )