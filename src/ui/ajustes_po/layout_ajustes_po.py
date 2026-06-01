import flet as ft


def build_layout(titulo_personal, contenedor_personal, titulo_predeterminado, contenedor_predeterminado, contenedor_botones, fields_ruta, fiels_reportes_ruta):

    frame_fiels_form = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            expand=True,
            controls=[
                titulo_personal,
                contenedor_personal
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    frame_predeterminado = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            expand=True,
            controls=[
                titulo_predeterminado,
                contenedor_predeterminado,
                contenedor_botones,
                fields_ruta,
                fiels_reportes_ruta
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    return ft.Container(
        expand=True,
        content=ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                frame_fiels_form,
                frame_predeterminado
            ],
        )
    )
