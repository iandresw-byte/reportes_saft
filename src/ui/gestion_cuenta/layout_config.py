import flet as ft


def build_layout_config(conten_titulo_cambiarCTA, content_camabiarCTA, conten_titulo_moficarBD, conten_modificarBase, titulo_mensajes, conten_mensajes):

    frame_camabiarCTA = ft.Container(
        expand=True,
        content=ft.ResponsiveRow(
            controls=[
                conten_titulo_cambiarCTA,
                content_camabiarCTA,
            ],
            alignment=ft.MainAxisAlignment.CENTER, col=4
        )
    )

    frame_ModificacionesBD = ft.Container(
        expand=True,
        content=ft.ResponsiveRow(
            controls=[
                conten_titulo_moficarBD,
                conten_modificarBase,
            ],
            alignment=ft.MainAxisAlignment.CENTER, col=4
        )
    )

    frame_mensaje = ft.Container(
        col=12,
        expand=True,
        content=ft.Column(
            height=250,
            controls=[
                titulo_mensajes,
                conten_mensajes,
            ]
        )
    )

    frame_1_2 = ft.Container(
        expand=True,
        content=ft.Column(
            controls=[
                ft.Row([
                    frame_camabiarCTA,
                    frame_ModificacionesBD,
                ])
            ]
        )
    )

    return ft.Container(
        expand=True,
        content=ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                frame_1_2,
                frame_mensaje
            ],
        )
    )
