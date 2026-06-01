import flet as ft
from src.services.parametro_service import ParametroService
from src.utils.config_manager import Config
from src.ui.components.ui_container import create_container
from src.ui.components.ui_colors import (
    color_bg,
    color_texto,
    color_texto_2,
    color_texto_parrafo
)

APP_VERSION = Config.obtener("APP", "app_version")


class VistaNoDisponible:

    def __init__(self, page, context):

        self.page = page
        self.app = context
        self.ft = ft

        self.app.init_saft()

        self.bg_color = color_bg()
        self.texto_color = color_texto()
        self.texto_color_2 = color_texto_2()
        self.color_parrafo = color_texto_parrafo()

        self.conten_acerca_de = create_container(
            expand=True,
            col=12,
            alineacion_col=self.ft.MainAxisAlignment.CENTER,
            controls=[

                # LOGO
                ft.Container(
                    content=ft.Image(
                        src="/images/saft.png",
                        width=120,
                        height=120,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    alignment=ft.alignment.center
                ),

                # TITULO
                ft.Text(
                    "Reportes SAFT",
                    size=26,
                    weight=self.ft.FontWeight.BOLD,
                    color=self.texto_color,
                    text_align=self.ft.TextAlign.CENTER,
                ),

                # VERSION
                ft.Text(
                    f"Versión {APP_VERSION}",
                    size=15,
                    color=self.texto_color_2,
                    text_align=self.ft.TextAlign.CENTER,
                ),

                ft.Divider(height=25),

                # MENSAJE
                ft.Icon(
                    name=ft.Icons.CONSTRUCTION,
                    size=70,
                    color=self.texto_color,
                ),

                ft.Text(
                    "Sin Acceso al Módulo",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=self.texto_color,
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Text(
                    "Consulte con el administrador del sistema.",
                    size=15,
                    color=self.color_parrafo,
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Container(height=20),

                # FOOTER
                ft.Text(
                    "© 2025 Asociación de Municipios de Honduras (AMHON)",
                    size=11,
                    italic=True,
                    color=self.color_parrafo,
                    text_align=self.ft.TextAlign.CENTER,
                ),

                ft.Row(
                    alignment=self.ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Image(
                            src="/images/Logo_amhon.png",
                            width=90,
                            height=80
                        )
                    ]
                )
            ],
        )

        self.conten_acerca_de.alignment = self.ft.alignment.center

    def build(self):
        return self.conten_acerca_de
