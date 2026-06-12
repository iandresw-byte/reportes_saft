
import os
import webbrowser
import flet as ft
from src.models.tra_permop import Tra_PermOpe
from src.reports.per_ope_tocoa import PermisoOperacionTocoaReport
from src.services.parametro_service import ParametroService
from src.services.permiso_operacion_services import PermisooperacionServices
from src.reports.permiso_operacion_report import PermisoOperacionReport
from src.reports.per_ope_la_esperanza import PerOpeLaEsperanzaReport
from src.reports.per_ope_concepcion_report import PerOpeConcepcionReport
from src.ui.modals.venta_alcohol_modal import abril_venta_alcohol_modal
from src.ui.components.ui_container import create_container
from src.ui.components.ui_checkBox import createCheckBox
from src.ui.components.ui_colors import color_bg, color_bg_2, color_texto, color_texto_2, color_texto_parrafo
from src.ui.components.ui_radio import create_radio
from src.ui.components.ui_botones import create_boton
from src.ui.components.ui_text import create_texFiel_fijas
from src.ui.components.ui_alertas import AlertaGeneral
from src.utils.config_manager import Config
from src.ui.ajustes_po.fields_create import create_botones_gestion, create_horiario_alcohol, create_solicitud, create_tipo_firma_eza, create_titulo, from_fields_create
from ui.ajustes_po.layout_create_po import build_layout_create

RESULTADO_DIR = Config.obtener("RUTAS", "carpeta_reportes")


class VistaPermisoOperacion:
    def __init__(self, page, context):
        self.page = page
        self.app = context
        self.app.init_saft()
        self.ft = ft
        self.bg_color = color_bg()
        self.bg_2_color = color_bg_2()
        self.texto_color = color_texto()
        self.texto_color_2 = color_texto_2()
        self.color_parrafo = color_texto_parrafo()
        self.datos_muni = self.app.datos_muni
        self.datos_muni_admin = self.app.datos_admin
        self.datos_system = self.app.datos_system
        self.repo_permiso = PermisooperacionServices(
            self.app, self.datos_system)

        self.chk_firma_justicia = createCheckBox("¿Firma Justicia?")
        self.chk_horario_alcohol = createCheckBox(
            "¿Horario Venta de Alcohol?", on_change=self.is_Horario_venta_alcol, disable=True)
        self.rd_horario_alcohol = create_horiario_alcohol(self)
        self.rd_tipo_solcitud = create_solicitud()
        self.rd_firma = create_tipo_firma_eza(self)
        if self.datos_muni["CodMuni"] == "1001":
            self.firma = ft.Row([self.rd_firma, ft.VerticalDivider(
                width=1, color="black", thickness=1,), self.rd_horario_alcohol])
        else:
            self.firma = self.chk_firma_justicia

        # ALERTAS
        self.alert_recibo = AlertaGeneral(
            titulo=ft.Text("Permiso de Operación"),
            contenido=ft.Text(
                "¡No se encontro Informacion para el numero de recibo ingresado!"),
            actions=[ft.OutlinedButton("Aceptar", on_click=self.acetar_reg),],)
        # BOTONES
        self.permiso: Tra_PermOpe | None
        self.titulo = create_titulo(self)
        self.btn_consulta = create_boton(
            "Consulta", on_click=self.consultar_recibo)
        self.botones = create_botones_gestion(self)
        if self.datos_muni["CodMuni"] == "1001":
            self.botones[2].visible = True
        else:
            self.botones[2].visible = False

        self.cajas_texto = from_fields_create(self)
        self.frame = build_layout_create(
            self.titulo, self.cajas_texto, self.btn_consulta, self.firma, self.rd_tipo_solcitud, self.botones)

    def build(self):
        return ft.Column(expand=True, controls=[
            self.frame
        ])

    def is_firma_justicia(self, e):
        if self.rd_firma.value == '1':

            self.rd_horario_alcohol.disabled = False
            self.rd_horario_alcohol.update()
        else:
            self.rd_horario_alcohol.value = '0'
            self.rd_horario_alcohol.disabled = True
            self.rd_horario_alcohol.update()

    def is_Horario_venta_alcol(self, e):
        if e.target.value:
            self.btn_horario.disabled = False
        else:
            self.btn_horario.disabled = True

    def abrir_modal_venta_bebida(self, e):
        self.dialog = abril_venta_alcohol_modal(self)
        self.page.open(self.dialog)
        self.page.update()

    def acetar_reg(self, e):
        self.alert_recibo.open = False
        self.alert_recibo.update()

    def consultar_recibo(self, e):
        num_recibo = self.cajas_texto[0].value
        existe = self.repo_permiso.existe_po(num_recibo)
        if self.datos_muni["CodMuni"] == "1001":
            justicia = self.rd_firma.value
            horario = self.chk_firma_justicia.value
        else:
            justicia = self.chk_firma_justicia.value
            horario = False
        tipo_per = self.rd_tipo_solcitud.value
        self.permiso = self.repo_permiso.crear_permiso_operacion(
            int(num_recibo), justicia, tipo_per, horario)  # type: ignore
        if not self.permiso:
            self.page.open(self.alert_recibo)
            return None
        self.txt_no_permiso.value = str(self.permiso.NoPermiso)
        self.txt_periodo.value = str(self.permiso.Periodo)
        self.txt_ini_operaion.value = self.permiso.FechaNac.strftime(
            "%d/%m/%Y")
        self.txt_telefono.value = self.permiso.Telefono
        self.txt_rtm.value = self.permiso.Identidad
        self.txt_rtn.value = self.permiso.rtn
        self.txt_fecha_emission.value = self.permiso.Fecha.strftime("%d/%m/%Y")
        self.txt_nombre_establecimiento.value = self.permiso.Negocio
        self.txt_identidad.value = self.permiso.idrepresentante
        self.txt_nombrePropietario.value = self.permiso.Propietario
        self.txt_claveCatastral.value = self.permiso.ClaveCatastro
        self.txt_ubicacion.value = self.permiso.Ubicacion
        self.txt_act_economica.value = self.permiso.Actividad
        self.txt_tipo_establecimiento.value = self.permiso.CodProfesion
        self.rd_tipo_solcitud.value = self.permiso.Observacion
        self.txt_num_renovacion.value = self.permiso.NumeroRenovacion
        self.rd_tipo_solcitud.update()

        if not existe:
            self.btn_guardar.disabled = False
            self.btn_guardar.style.bgcolor = self.bg_color
            self.btn_guardar.update()
            self.btn_imprimir.style.bgcolor = self.bg_2_color
            self.btn_imprimir.disabled = True
            self.btn_imprimir.update()
            if self.datos_muni["CodMuni"] == "1001":
                self.rd_horario_alcohol.value = '0'
                self.rd_horario_alcohol.update()
                self.rd_firma.disabled = False
                self.rd_firma.update()
            else:
                self.chk_firma_justicia.value = False
                self.chk_firma_justicia.disabled = False
                self.chk_firma_justicia.update()
            self.rd_tipo_solcitud.update()

        else:
            self.btn_guardar.disabled = True
            self.btn_guardar.update()
            self.btn_guardar.style.bgcolor = self.bg_2_color
            self.btn_imprimir.disabled = False
            self.btn_imprimir.style.bgcolor = self.bg_color
            self.btn_imprimir.update()
            if self.datos_muni["CodMuni"] == "1001":
                self.rd_firma.value = str(self.permiso.FirmaJ)
                self.rd_firma.update()
                self.rd_horario_alcohol.value = str(
                    self.permiso.HorarioAlcohol)
                self.rd_horario_alcohol.update()
            else:
                self.firma.value = bool(self.permiso.FirmaJ)
            self.firma.disabled = True
            self.firma.update()
        self.page.update()

    def guardar_recibo_po(self, e):
        if self.datos_muni["CodMuni"] == "1001":
            self.permiso.FirmaJ = self.rd_firma.value
            if self.permiso.FirmaJ == 1:
                self.permiso.HorarioAlcohol = self.rd_horario_alcohol.value
            else:
                self.permiso.HorarioAlcohol = '0'
        else:
            self.permiso.FirmaJ = self.chk_firma_justicia.value
        if self.repo_permiso.guardar_perm_operacion(self.permiso):
            self.botones[0].disabled = True
            self.botones[0].style.bgcolor = self.bg_2_color
            self.botones[0].update()
            self.botones[1].disabled = False
            self.botones[1].style.bgcolor = self.bg_color
            self.botones[1].update()
            self.page.update()

    def imprimir_rept_po(self, e):
        try:
            if self.datos_muni["CodMuni"] == "1001":
                justicia = self.rd_firma.value
                if justicia == '1':
                    horario_alcoho = self.rd_horario_alcohol.value
                else:
                    horario_alcoho = '0'
            else:
                justicia = self.chk_firma_justicia.value
                horario_alcoho = '0'

            if self.datos_muni["CodMuni"] == "1001":
                reporte = PerOpeLaEsperanzaReport(
                    self.permiso, self.datos_muni, "", justicia, self.datos_muni_admin, horario_alcohol=horario_alcoho)  # type: ignore
            elif self.datos_muni["CodMuni"] == "0209":
                reporte = PermisoOperacionTocoaReport(
                    self.permiso, self.datos_muni, "", justicia, self.datos_muni_admin)  # type: ignore
            elif self.datos_muni["CodMuni"] == "1403":
                reporte = PerOpeConcepcionReport(
                    self.permiso, self.datos_muni, "", justicia, self.datos_muni_admin)  # type: ignore
            else:
                reporte = PermisoOperacionReport(
                    self.permiso, self.datos_muni, "", justicia, self.datos_muni_admin)
            nombre_archivo = "po_report.pdf"

            ruta = os.path.join(RESULTADO_DIR, "pdf", nombre_archivo)

            reporte.generar_pdf(ruta)
            webbrowser.open_new_tab(f"file://{ruta}")
            # Mostrar notificación
            fila_nack_bar = ft.Row([ft.ProgressRing(height=20, width=20), ft.Text(
                f"Reporte generado: {nombre_archivo}", size=14)])
            self.page.open(self.ft.SnackBar(fila_nack_bar,
                                            bgcolor=ft.Colors.GREEN_700, duration=20
                                            ))
            self.botones[0].disabled = True
            self.botones[0].style.bgcolor = self.bg_2_color
            self.botones[0].update()

            self.botones[1].disabled = True
            self.botones[1].style.bgcolor = self.bg_2_color
            self.botones[1].update()
            self.txt_no_permiso.value = str(self.permiso.NoPermiso)

            for caja in self.cajas_texto:
                caja.value = ""
            if self.datos_muni["CodMuni"] == "1001":
                self.firma.value = "0"
            else:
                self.firma.value = False

            self.page.update()

        except Exception as ex:
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Error: {str(ex)}", size=14),
                bgcolor=ft.Colors.RED_700,
            ))
            self.botones[0].disabled = True
            self.botones[0].style.bgcolor = self.bg_color
            self.botones[0].update()

            self.botones[1].disabled = True
            self.botones[1].style.bgcolor = self.bg_color
            self.botones[1].update()
            self.page.update()

    def cerrar_modal(self):
        self.dialog.open = False
        self.page.update()
