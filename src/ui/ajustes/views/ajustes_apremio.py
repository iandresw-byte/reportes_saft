

import flet as ft

from src.utils.config_manager import Config
from src.ui.modals.datos_actualizados_modal import abrir_datos_actualizados
from src.ui.ajustes.layouts.ajustes_apremio import build_layout
from src.ui.components.ui_container import container_titulo
from src.ui.ajustes.components.ajustes_apremio import botones_tamanio_pdf, list_departamentos_frm_1, list_departamentos_frm_2, numero_firmas

class VistaAjustesApremio:
    def __init__(self, page, context):
        self.page = page
        self.app = context

        # servicios y datos
        self._init_services()

        # titulos
        self.titulo_tamanio = container_titulo("TIPO DE DOCUMENTO", 15)
        self.titulo_firmas = container_titulo("FIRMAS PREDETERMINADAS, PROCESO DE APREMIO",15)


        self.contenedor_tipos_tamanio = botones_tamanio_pdf(self.page,self.app )
        self.departamentos_1 = list_departamentos_frm_1(self.page)
        self.departamentos_2 = list_departamentos_frm_2(self.page)
        self.numfirmas = numero_firmas(self, self.page)
        self.firmas_content = ft.Row([self.numfirmas], ft.MainAxisAlignment.SPACE_AROUND)
        self.departamentos = ft.Row([ self.departamentos_1, self.departamentos_2],alignment = ft.MainAxisAlignment.SPACE_AROUND)
        self.layout = build_layout(
            self.titulo_tamanio,
            self.contenedor_tipos_tamanio,
            self.titulo_firmas,
            self.firmas_content,
            self.departamentos,
        )

    def build(self):
        return self.layout

    def _init_services(self):
        self.datos_muni = self.app.datos_muni
        self.datos_muni_admin = self.app.datos_admin
        self.datos_system = self.app.datos_system
        self.cod_depto = ft.Ref[ft.Dropdown]()

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

