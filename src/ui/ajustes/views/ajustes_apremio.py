

import flet as ft

from src.utils.config_manager import Config
from src.ui.modals.datos_actualizados_modal import abrir_datos_actualizados
from src.ui.ajustes.layouts.ajustes_apremio import build_layout
from src.ui.components.ui_container import container_titulo
from src.ui.ajustes.components.ajustes_apremio import botones_tamanio_pdf, numero_firmas

class VistaAjustesApremio:
    def __init__(self, page, context):
        self.page = page
        self.app = context
        self.app.init_saft()


        # servicios y datos
        self._init_services()

        # titulos
        self.titulo_tamanio = container_titulo("Personal Administrativo")
        self.titulo_firmas = container_titulo("Firma Predeterminada Proceso de Apremio")


        self.contenedor_tipos_tamanio = botones_tamanio_pdf(self.page)
        self.contenedor_firmas = container_titulo("Firma Predeterminada Proceso de Apremio")

        self.layout = build_layout(
            self.titulo_tamanio,
            self.contenedor_tipos_tamanio,
            self.titulo_firmas,
            self.contenedor_firmas,
        )

    def build(self):
        return self.layout

    def _init_services(self):
        self.datos_muni = self.app.datos_muni
        self.datos_muni_admin = self.app.datos_admin
        self.datos_system = self.app.datos_system

    def cerrar_modal(self):
        self.dialog.open = False
        self.page.update()

    def abrir_modal_bien(self, e):
        self.tipo_impuesto = 0
        self.dialog = abrir_datos_actualizados(
            self, e, "Datos Actualizados", "Los datos administrativos han sido actualizados")
        self.page.open(self.dialog)
        self.page.update()

    def abrir_modal_mal(self, e):
        self.tipo_impuesto = 0
        self.dialog = abrir_datos_actualizados(
            self, e, "Errro al actualizar", "Los datos administrativos no se han actualizado")
        self.page.open(self.dialog)
        self.page.update()

