

import flet as ft
from src.services.parametro_service import ParametroService
from src.utils.config_manager import Config
from src.ui.ajustes.evento_ajustes_po import file_picker_result, file_picker_result_reportes, habilitar_fields, actualizar, deshabilitar_fields
from src.ui.ajustes.layout_ajustes_po import build_layout

from src.ui.ajustes.views.ajustes_apremio import VistaAjustesApremio
from src.ui.ajustes.fields_ajustes import btn_ruta_google, from_fiels_encargados, radios_predeterminados, botones, btn_ruta_carpeta_reportes
from src.ui.modals.datos_actualizados_modal import abrir_datos_actualizados
from src.ui.components.ui_container import container_titulo, create_container
from src.ui.components.ui_colors import color_texto, color_borde

texto_color = color_texto()
borde_color = color_borde()
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

        vista = VistaAjustesApremio(self.page, self.app)
        self.lauout_apremio = vista.build()

    def build(self):
        return ft.Tabs(
            selected_index=0,
            expand=1,
            unselected_label_color=texto_color,
            unselected_label_text_style=ft.TextStyle( size=12.5,  weight=ft.FontWeight.W_400),

            label_color=texto_color,
            label_text_style=ft.TextStyle( size=12.5,  weight=ft.FontWeight.W_800),

            indicator_border_radius=0.5,
            indicator_color=borde_color,
            tabs=[


                ft.Tab(
                    text="AJUSTES DE PERSONAL ADMINISTRATIVO",
                    content=self.layout
                ),
                ft.Tab(
                    text="PROCESO DE APREMIO",
                    content=self.lauout_apremio
                ),
                ft.Tab(
                    text="IDENTIFIACION DE MORA",
                   content=ft.Text("Ajustes Permido Operacion")
                ),
            ]
        )


    

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
