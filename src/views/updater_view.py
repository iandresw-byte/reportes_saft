# src/views/actualizacion_view.py

import flet as ft


class PantallaActualizacion(ft.Container):

    def __init__(self, page):
        super().__init__()

        self.content = ft.Column(
            controls=[
                ft.Icon(ft.Icons.SYSTEM_UPDATE, size=80),
                ft.Text(
                    "Existe una nueva versión disponible.",
                    size=20
                ),
                ft.ElevatedButton(
                    "Actualizar",
                    on_click=self.actualizar
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def actualizar(self, e):
        print("Descargar actualización")
