import flet as ft
from src.services.parametro_service import ParametroService
from src.services.finarlizar_pago_ip_otras_service import FinalizarPagosIPService
from src.ui.PagosIP.componentes import form_botones, form_num_recibo, form_excel, caja_progreso
from src.ui.reports.utils_reportes import snack_error_reporte, snack_inicio_reporte
from src.ui.components.ui_container import container_titulo, create_container
from src.ui.PagosIP.layout import build_layout
from src.ui.PagosIP.eventos import file_picker_result


class VistaPagosIP:
    def __init__(self, page, context):

        self.page = page
        self.app = context
        self.app.init_saft()
        self.txt_ruta_excel = None

        self._init_services()

        # UI
        self.titulo = container_titulo(
            "Cargar Pagos Impuesto Personal",
            label_size=20
        )
        self.file_picker = ft.FilePicker(
            on_result=lambda e: file_picker_result(self, e)
        )
        self.page.overlay.append(self.file_picker)
        self.fields = form_num_recibo(self)
        self.fields_archivo = form_excel(self)
        self.botones = form_botones(self)
        self.caja = caja_progreso()
        self.contenedor_progreso = create_container(controls=[self.caja])
        self.contenedor_fields = create_container(self.fields)
        self.contenedor_archivo = create_container(content=self.fields_archivo)
        self.contenedor_botones = create_container(content=self.botones)

        self.layout = build_layout(
            self.titulo,
            self.contenedor_fields,
            self.contenedor_botones,
            self.contenedor_archivo,
            self.contenedor_progreso
        )

    def build(self):
        return self.layout

    def _init_services(self):

        self.datos_system = self.app.datos_system

        self.manejador = FinalizarPagosIPService(
            self.app, self.datos_system)

    # 👉 Acción del botón
    def abrir_file_picker(self, e):

        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["xlsx", "xls"]
        )

    def procesar_excel(self, e):
        ruta_excel = self.txt_ruta_excel.value
        num_recibo = self.fields[0].value
        try:
            self.manejador.relacionar_pago_otras_tasas(self,
                                                       self.caja, num_recibo, ruta_excel)
            snack_inicio_reporte(
                self.page, "Todo Listo!", e)
        except Exception as e:
            snack_error_reporte(self.page, str(e))

    def escribir_progreso(self, mensaje):
        self.caja.value += mensaje + "\n"
        self.caja.update()

    def limpiar(self, e):
        self.caja.value = ""
        self.txt_ruta_excel.value = ""
        self.fields[0].value = ""

        self.caja.update()
        self.txt_ruta_excel.update()
        self.fields[0].update()
