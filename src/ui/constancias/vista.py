# ui/reportes/vista_reportes.py

import asyncio
from src.services.constancias_services import ConstanciasService
from src.ui.constancias.layout import build_layout
from src.ui.constancias.componentes import botones_catastro, botones_secretaria, botones_uma
from src.ui.constancias.eventos import cargar_data_licencia_uma_ics
from src.ui.constancias.modals.licencia_ambiental_data_modal import abrir_modal_licencia_ics_data
from src.ui.components.ui_container import container_titulo, create_container
from src.ui.constancias.modals.licencia_ambiental import abrir_modal_licencia_ics
from src.ui.constancias.modals.licencia_ambiental import abrir_modal_licencia_ics


class VistaConstancias:
    def __init__(self, page, context):
        self.page = page
        self.app = context
        self.app.init_saft()

        # servicios y datos
        self._init_services()

        # titulos
        self.titulo_mora = container_titulo("LICENCIAS PERMISOS")
        self.titulo_otros = container_titulo("OTROS REPORTES")
        self.titulo_ingresos = container_titulo("OTROS DE INGRESOS")

        # botones
        self.contenedor_mora = create_container(content=botones_uma(self))
        self.contenedor_ingreso = create_container(botones_catastro(self))
        self.contenedor_otros = create_container(botones_secretaria(self))

        # layout
        self.layout = build_layout(
            self.titulo_mora,
            self.contenedor_mora,
            self.titulo_otros,
            self.contenedor_otros,
            self.contenedor_ingreso,
            self.titulo_ingresos
        )

    def build(self):
        return self.layout

    def _init_services(self):
        self.datos_muni = self.app.datos_muni
        self.administracion = self.app.datos_admin
        self.datos_system = self.app.datos_system
        self.constancias = ConstanciasService(
            self.app.conexion_saft)
        self.licencia_ambiental = None

    def abrir_licencia_ambiental_modal(self, e):
        self.num_recibo = 0
        self.dialog = abrir_modal_licencia_ics(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def cerrar_modal(self):
        self.dialog.open = False
        self.page.update()

    def generar_pdf_licencia_ambiental_ics(self, e):
        num_recibo = self.num_recibo.current.value
        data = self.constancias.obtener_licencia_uma_ics(num_recibo),
        self.dialog = abrir_modal_licencia_ics_data(self,data, e)
        self.page.open(self.dialog)
        self.page.update()

    def actualizar_pdf_licencia_ambiental_ics(self, e):
            num_recibo = self.num_recibo.current.value
            data = self.constancias.obtener_licencia_uma_ics(num_recibo),
            self.dialog = abrir_modal_licencia_ics_data(self,data, e)
            self.page.open(self.dialog)
            self.page.update()
    
