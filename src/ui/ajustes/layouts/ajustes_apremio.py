import flet as ft


def build_layout(titulo_tamanio, tipos_tamanio, titulo_firmas, contenedor_firmas,contenerdor_deptos, titulo_cuentas,
                    contenedor_cuentas, contenedor_botones):

    frame_tamanio_reporte = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            expand=True,
            controls=[
                titulo_tamanio,
                tipos_tamanio
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    frame_firmas_documento = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            expand=True,
            controls=[
                titulo_firmas,
                contenedor_firmas,
                contenerdor_deptos
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    frame_cta_ingresos = ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 0),
            content=ft.Column(
                expand=True,
                controls=[
                    titulo_cuentas,
                    contenedor_cuentas,
                    contenedor_botones
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )

    return ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                frame_tamanio_reporte,
                frame_firmas_documento,
                frame_cta_ingresos
            ],
        )
    )
