import flet as ft


def build_layout(titulo, contenedor_fiels, contenedor_botones, contenedor_archivo, contenedor_progreso):

    frame_fiels_form = ft.Container(

        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            #  expand=True,
            controls=[
                titulo,
                contenedor_fiels,
                contenedor_archivo,

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )
    frame_resultado = ft.Container(
        #  height=250,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            height=250,
            controls=[
                contenedor_progreso
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    frame_botones = ft.Container(

        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            #    expand=True,
            controls=[
                contenedor_botones
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    return ft.Container(

        content=ft.Column(
            # expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                frame_fiels_form,
                frame_resultado,
                frame_botones
            ],
        )
    )
