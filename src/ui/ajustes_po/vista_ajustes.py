

import flet as ft
from src.services.parametro_service import ParametroService
from src.utils.config_manager import Config
from src.ui.ajustes_po.evento_ajustes_po import file_picker_result, file_picker_result_reportes, habilitar_fields, actualizar, deshabilitar_fields
from src.ui.ajustes_po.layout_ajustes_po import build_layout
from src.ui.ajustes_po.fields_ajustes import btn_ruta_google, from_fiels_encargados, radios_predeterminados, botones, btn_ruta_carpeta_reportes
from src.ui.modals.datos_actualizados_modal import abrir_datos_actualizados
from src.ui.components.ui_container import container_titulo, create_container


class VistaAjustesPO:
    def __init__(self, page, context):
        self.page = page
        self.app = context
        self.app.init_saft()
        self.ruta_google = Config.obtener("RUTAS", "carpeta_unidad_google")
        self.ruta_reportes = Config.obtener("RUTAS", "carpeta_reportes")

        self.txt_ruta_google = ft.TextField(value=self.ruta_google)
        self.ruta_google_ref = ''

        self.txt_ruta_reportes = ft.TextField(value=self.ruta_reportes)
        self.ruta_reportes_ref = ''

        # servicios y datos
        self._init_services()

        # titulos
        self.titulo_personal = container_titulo("Personal Administrativo")
        self.titulo_prederminado = container_titulo("Firma Predeterminada")

        self.filds_form = from_fiels_encargados(self)
        self.radios = radios_predeterminados(self)
        self.botones = botones(self)
        self.contenedor_field_personal = create_container(self.filds_form)
        self.contenedor_radios = create_container(self.radios)

        self.contenedor_botones = create_container(content=self.botones)
        self.file_picker = ft.FilePicker(
            on_result=lambda e: file_picker_result(self, e)
        )
        self.file_picker_1 = ft.FilePicker(
            on_result=lambda e: file_picker_result_reportes(self, e)
        )
        self.page.overlay.append(self.file_picker)
        self.page.overlay.append(self.file_picker_1)
        # layout
        self.fields_ruta = btn_ruta_google(self)
        self.reportes_ruta = btn_ruta_carpeta_reportes(self)

        ruta = self.ruta_google
        if ruta:
            self.txt_ruta_google.value = ruta
        ruta_1 = self.ruta_reportes
        if ruta_1:
            self.txt_ruta_reportes.value = ruta_1

        self.layout = build_layout(
            self.titulo_personal,
            self.contenedor_field_personal,
            self.titulo_prederminado,
            self.contenedor_radios,
            self.contenedor_botones,
            self.fields_ruta,
            self.reportes_ruta
        )

    def build(self):
        return self.layout

    def _init_services(self):
        self.datos_muni = self.app.datos_muni
        self.datos_muni_admin = self.app.datos_admin
        self.datos_system = self.app.datos_system

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

    def abrir_file_picker(self, e):

        self.file_picker.get_directory_path()

    def abrir_file_picker_1(self, e):

        self.file_picker_1.get_directory_path()
