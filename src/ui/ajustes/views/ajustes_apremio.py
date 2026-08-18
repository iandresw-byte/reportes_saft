

import flet as ft

from src.utils.config_manager import Config
from src.ui.modals.datos_actualizados_modal import abrir_datos_actualizados
from src.ui.ajustes.layouts.ajustes_apremio import build_layout
from src.ui.components.ui_container import container_titulo, create_container
from src.ui.ajustes.components.ajustes_apremio import botones_tamanio_pdf, list_departamentos_frm_1, list_departamentos_frm_2, numero_firmas
from src.ui.ajustes.components.fields_cuentas import from_fiels_cuentas, botones_cta
from src.ui.ajustes.events.apremio_ajustes import actualizar, deshabilitar_fields, habilitar_fields



class VistaAjustesApremio:
    def __init__(self, page, context):
        self.page = page
        self.app = context

        # servicios y datos
        self._init_services()

        # titulos
        self.titulo_tamanio = container_titulo("TIPO DE DOCUMENTO", 15)
        self.titulo_firmas = container_titulo("FIRMAS PREDETERMINADAS, PROCESO DE APREMIO",15)
        self.titulo_cuentas = container_titulo("DESCRIPCION CUENTAS DE INGRESO",15)


        self.contenedor_tipos_tamanio = botones_tamanio_pdf(self.page,self.app )
        self.departamentos_1 = list_departamentos_frm_1(self.page)
        self.departamentos_2 = list_departamentos_frm_2(self.page)
        self.filds_cuentas = from_fiels_cuentas(self.page)
        
        self.botones = botones_cta(self)
        self.numfirmas = numero_firmas(self, self.page)
        self.contenedor_botones = create_container(content=self.botones)
        self.contenedor_fields = create_container(self.filds_cuentas)
        self.firmas_content = ft.Row([self.numfirmas], ft.MainAxisAlignment.SPACE_AROUND)
        self.departamentos = ft.Row([ self.departamentos_1, self.departamentos_2],alignment = ft.MainAxisAlignment.SPACE_AROUND)
        self.layout = build_layout(
            self.titulo_tamanio,
            self.contenedor_tipos_tamanio,
            self.titulo_firmas,
            self.firmas_content,
            self.departamentos,
            self.titulo_cuentas,
            self.contenedor_fields,
            self.contenedor_botones
        )

    def build(self):
        return self.layout

    def _init_services(self):
        self.datos_muni = self.app.datos_muni
        self.datos_muni_admin = self.app.datos_admin
        self.datos_system = self.app.datos_system
        self.cod_depto = ft.Ref[ft.Dropdown]()

    def habilitar(self, e):
            habilitar_fields(self)
    
    def actualizar(self, e):
        deshabilitar_fields(self)
        if actualizar(self):
            self.abrir_modal_bien(e)
        else:
            self.abrir_modal_mal(e)

    def deshabilitar(self, e):
        deshabilitar_fields(self)

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

