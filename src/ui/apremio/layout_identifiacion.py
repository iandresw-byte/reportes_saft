import flet as ft


def build_layout_identificacion(
        titulo_general,
        barra,
        titulo_bi, contenedor_bi,
        titulo_ip, contenedor_ip,
        titulo_ics, contenedor_ics,
        titulo_sp, contenedor_sp
):

    def crear_frame(titulo, contenido):
        return ft.Container(
            col=6,  # 2 columnas por fila
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            content=ft.Column(
                controls=[
                    titulo,
                    contenido
                ],
                spacing=10,
                expand=True
            )
        )

    frame_1 = crear_frame(titulo_bi, contenedor_bi)
    frame_2 = crear_frame(titulo_ip, contenedor_ip)
    frame_3 = crear_frame(titulo_ics, contenedor_ics)
    frame_4 = crear_frame(titulo_sp, contenedor_sp)

    return ft.Container(
        expand=True,
        padding=10,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            col=12,
                            padding=10,
                            content=ft.Column(
                                controls=[titulo_general, barra
                                          ])
                        ),
                        frame_1,
                        frame_2,
                        frame_3,
                        frame_4,
                    ],
                    spacing=10,
                    run_spacing=10,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                )
            ]
        )
    )
