# src/views/actualizacion_view.py

import flet as ft
from src.ui.components.ui_btn_actualizar import create_update_button
from src.services.update_services import UpdateService


class PantallaActualizacion(ft.Container):

    def __init__(self, page):
        super().__init__()
        self.btn_update = create_update_button(
            page, on_click=UpdateService.actualizacion)
        self.content = ft.Column(
            controls=[
                ft.Icon(ft.Icons.SYSTEM_UPDATE, size=80),
                ft.Text(
                    "Existe una nueva versión disponible.",
                    size=20
                ),
                self.btn_update
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def actualizar(self, e):
        print("Descargar actualización")
