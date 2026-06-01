
import webbrowser
import flet as ft
from src.services.update_services import UpdateService
from src.utils.config_manager import Config
from src.ui.components.ui_container import create_container
from src.ui.components.ui_btn_actualizar import create_update_button
from src.ui.components.ui_colors import color_bg, color_texto, color_texto_2, color_texto_parrafo
APP_VERSION = Config.obtener("APP", "app_version")
FECHA_LANZAMIENTO = Config.obtener("APP", "fecha_lanzamiento")
FECHA_ACTUALIZACION = Config.obtener("APP", "fecha_actualizacion")


class VistaAbout:
    def __init__(self, page, context):
        self.page = page
        self.app = context
        self.app.init_saft()
        self.ft = ft

        self.bg_color = color_bg()
        self.texto_color = color_texto()
        self.texto_color_2 = color_texto_2()
        self.color_parrafo = color_texto_parrafo()
        self.update_app = UpdateService(self.page)

        # BOTONES
        self.btn_update = create_update_button(
            self.page, on_click=self.update_app.verificar_actualizacion)

        self.conten_acerca_de = create_container(
            expand=True,
            col=12,
            alineacion_col=self.ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Image(src=r"\assets\images\saft.png"),
                ft.Text(
                    "Reportes SAFT",
                    size=24,
                    weight=self.ft.FontWeight.BOLD,
                    text_align=self.ft.TextAlign.CENTER,
                    color=self.texto_color,
                ),
                ft.Text(
                    f"Versión {APP_VERSION}",
                    size=16,
                    color=self.texto_color_2,
                ),

                ft.Text(
                    f"Fecha de actualización: {FECHA_ACTUALIZACION}",
                    size=12,
                    color=self.color_parrafo,
                ),
                ft.Text(
                    "Herramienta desarrollada en el Depto. de Modernización de la Gestión Pública Municipal por la Unidad SAFT - AMHON.\n"
                    "Permite la generación de reportes, consultas datos municipales.\n\n",
                    size=14,
                    color=self.color_parrafo,
                    text_align=self.ft.TextAlign.CENTER,
                ),
                ft.Row(
                    alignment=self.ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.TextButton(
                            "🌍 Página AMHON",
                            style=ft.ButtonStyle(
                                color=self.texto_color, overlay_color=self.bg_color),
                            on_click=lambda e: webbrowser.open(
                                "https://www.amhon.hn"

                            ),
                        ),
                        ft.TextButton(
                            "🔗 Portal SAFT",
                            style=ft.ButtonStyle(
                                color=self.texto_color, overlay_color=self.bg_color),
                            on_click=lambda e: webbrowser.open(
                                "http://saftamhon.com"
                            ),
                        ),
                        ft.TextButton(
                            "📞 Jefe Depto. de Modernización",
                            style=ft.ButtonStyle(
                                color=self.texto_color, overlay_color=self.bg_color),
                            on_click=lambda e: webbrowser.open(
                                "https://wa.me/+50488004902"
                            ),
                        )
                    ],
                ),
                ft.Divider(),
                self.btn_update,
                ft.Text(
                    "© 2025 Asociación de Municipios de Honduras (AMHON)",
                    size=12,
                    color=self.color_parrafo,
                    italic=True,
                    text_align=self.ft.TextAlign.CENTER,
                ),
                ft.Row([
                    ft.Container(
                        ft.Image(src='/images/saft.png', width=50, height=40)),
                    ft.Container(
                        ft.Image(src='/images/Logo_amhon.png', width=100, height=90))
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
        )
        self.conten_acerca_de.alignment = self.ft.alignment.center

    def build(self):
        return self.conten_acerca_de
