import flet as ft


def build_layout_config(titulo_gestor, titulo_radio, form_radio, rd_opt_tipo_cuenta, conten_gestor, titulo_mensajes, conten_mensajes):

    frame1 = ft.Container(
        col=3,
        content=ft.Column(
            controls=[
                titulo_radio,
                ft.ResponsiveRow(controls=[rd_opt_tipo_cuenta]),
                form_radio,
            ]
        )
    )

    frame3 = ft.Container(
        col=9,
        width=800,
        height=500,
        content=ft.Column(
            controls=[

                conten_gestor,
            ]
        )
    )

    frame4 = ft.Container(
        col=12,
        height=100,
        content=ft.Column(
            controls=[
                titulo_mensajes,
                conten_mensajes,
            ]
        )
    )

    return ft.Column(
        controls=[
            ft.Container(
                col=9,
                content=ft.ResponsiveRow(
                    controls=[
                        titulo_gestor,
                        frame1,
                        frame3,
                        frame4,
                    ]
                )
            )
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
    )
