# src/views/splash_view.py

import flet as ft


class SplashView(ft.Container):
    def __init__(self):
        super().__init__(
            # width=720,
            # height=440,
            alignment=ft.Alignment(0, 0),
            expand=True,
            content=ft.Column(
                controls=[
                    ft.ProgressRing(),
                    ft.Text(
                        "Iniciando experiencia personalizada...",
                        size=18
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
