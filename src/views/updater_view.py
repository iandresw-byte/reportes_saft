# src/views/actualizacion_view.py

import flet as ft
from src.ui.components.ui_btn_actualizar import create_update_button, actualizar_base_boton
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



class PantallaActualizacionBD(ft.Container):

    def __init__(self, page):
        super().__init__()
        self.page = page
        

        self.btn_update_base = actualizar_base_boton()
        self.btn_update_base.on_click = self.alterar_base
        self.content_base = ft.Column(
            controls=[
                ft.Icon(ft.Icons.SYSTEM_UPDATE, size=80),
                ft.Text(
                    "Existe una nueva estructura de la base de datos.",
                    size=20
                ),
                self.btn_update_base
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    async def alterar_base(self, e):

        from src.services.data_base_services import DataBaseService
        from contexts.app_context import AppContext
        context = AppContext()
        try:
            context.init_saft()
        except Exception as ex:
            context.initial_login()
            logging = DataBaseService(context.conexion_logging)
            logging.alterar_login()
        context.init_saft()
        servicio = DataBaseService(context.conexion_saft)
        servicio.alterar_parametro_cont()
        servicio.alterar_apremio()
        servicio.create_vistas()
