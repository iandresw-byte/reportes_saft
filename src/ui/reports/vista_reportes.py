# ui/reportes/vista_reportes.py

import asyncio
import datetime
from src.services.reportes_ingresos_deptos_diario_services import RptIngresosDeptosDiarioService
from src.services.reportes_ingresos_deptos_mensual_services import RptIngresosDeptosMensualService
from src.services.apremio_service import ApremioService
from src.services.aldea_servives import AldeaService
from src.services.parametro_service import ParametroService
from src.services.mora_bi_services import MoraBIService
from src.services.rpt_bomberos_services import RptBomberosService
from src.services.mora_ip_services import MoraIPService
from src.services.mora_ics_sevices import MoraICSService
from src.services.mora_sp_services import MoraSPService
from src.services.update_services import UpdateService
from src.services.permiso_operacion_services import PermisooperacionServices
from src.services.plan_pago_services import PlanesPagoService
from src.services.mora_aldea_services import MoraAldeaService
from src.services.trancicion_traspaso_servivces import TrancicionTraspasoService
from src.services.trancicion_traspaso_det_services import TrancicionTraspasoDetalleService
from src.services.analisis_ingresos_services import AnalisisIngresosService
from src.services.estratificacion_services import EstratificacionService
from src.services.reportes_ingresos_deptos_services import RptIngresosDeptosService
from src.services.reportes_sar_services import SARReportesService
from src.ui.modals.estratificacion_modal import abrir_modal_estratificacion
from src.ui.modals.modal_ingresos_depto import abrir_modal_rpt_ingresos_depto
from src.ui.modals.modal_ingresos_depto_detallado import abrir_modal_rpt_ingresos_detallados_depto
from src.ui.modals.modal_ingresos_depto_diarios import abrir_modal_rpt_ingresos_diarios_depto
from src.ui.modals.modal_ingresos_depto_mensual import abrir_modal_rpt_ingresos_mensual_depto
from src.ui.modals.reporte_permiso_operacion_modal import abrir_modal_rpt_permiso_operacion
from src.ui.modals.rpt_sar_modal import abrir_modal_estratificacion_sar
from src.ui.modals.trancicion_traspaso_modal import abrir_trancicicon_traspaso
from src.ui.reports.layout_reportes import build_layout
from src.ui.reports.botones_reportes import botones_mora, botones_otros, botones_ingresos
from src.ui.components.ui_container import container_titulo, create_container
from src.ui.reports.eventos_reportes import (anula_plan_pago, generar_analisis_ingresos, generar_excel_estratificacion, generar_excel_estratificacion_sar,
                                             generar_mora_bi, generar_mora_bi_aldea_anio_excel,
                                             generar_mora_bi_aldea_anio_pdf, generar_mora_ics, generar_mora_ip,
                                             generar_mora_sp, generar_pdf_mora_vs_ingresos, generar_excel_mora_vs_ingresos, generar_reporte_excel_bomberos,
                                             generar_reporte_excel_ingreso_depto,
                                             generar_reporte_excel_ingreso_depto_detallado, generar_reporte_excel_ingreso_depto_diario, generar_reporte_pdf_bomberos, generar_reporte_pdf_ingreso_depto,
                                             generar_reporte_pdf_ingreso_depto_detallado, generar_reporte_pdf_ingreso_depto_diario, generar_reporte_pdf_ingreso_depto_mensual,  generar_reporte_trancicicon,
                                             generar_reporte_trancicicon_det_amb, generar_reporte_trancicicon_det_bi,
                                             generar_reporte_trancicicon_det_ics, generar_reporte_trancicicon_det_ip,
                                             generar_reporte_trancicicon_det_ist, generar_reporte_trancicicon_det_sp, generar_rpt_permiso_operacion_pdf)
from src.ui.modals.mora_aldea_bi_modal import abrir_modal_mora_bi_aldea_anio
from src.ui.modals.mora_vs_ingresos_aldea_modal import abrir_modal_mora_vs_ingresos
from src.ui.components.analisi_ingresos_modal import abrir_analisis_ingresos
from src.ui.modals.anula_pp_modal import abrir_anula_plan_pago
from src.ui.modals.apremio_modal import abrir_modal_rpt_apremio_1er
from src.ui.modals.modal_ingresos_bomberos import abrir_modal_rpt_bomberos


class VistaReportes:
    def __init__(self, page, context):
        self.page = page
        self.app = context
        self.app.init_saft()

        # servicios y datos
        self._init_services()

        # titulos
        self.titulo_mora = container_titulo("REPORTES DE MORA")
        self.titulo_otros = container_titulo("OTROS REPORTES")
        self.titulo_ingresos = container_titulo("OTROS DE INGRESOS")

        # botones
        self.contenedor_mora = create_container(botones_mora(self))
        self.contenedor_ingreso = create_container(botones_ingresos(self))
        self.contenedor_otros = create_container(botones_otros(self))

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
        self.mora_bi = MoraBIService(self.app.conexion_saft, self.datos_system)
        self.ingresos_bombero = RptBomberosService(
            self.app.conexion_saft, self.datos_system)
        self.mora_ip = MoraIPService(self.app.conexion_saft, self.datos_system)
        self.apremio = ApremioService(
            self.app.conexion_saft, self.datos_system, self.app.usuario_actual)
        self.mora_ics = MoraICSService(
            self.app.conexion_saft, self.datos_system)
        self.mora_sp = MoraSPService(self.app.conexion_saft, self.datos_system)
        self.update_app = UpdateService(self.page)
        self.trancicion = TrancicionTraspasoService(
            self.app.conexion_saft, self.datos_system)
        self.trancicion_detalle = TrancicionTraspasoDetalleService(
            self.app.conexion_saft, self.datos_system)
        self.aldeas = AldeaService(self.app.conexion_saft)
        self.mora_aldea = MoraAldeaService(
            self.app.conexion_saft, self.datos_system)
        self.analisis = AnalisisIngresosService(
            self.app.conexion_saft, self.datos_system)
        self.plan_pago = PlanesPagoService(self.app.conexion_saft)
        self.permiso_operacion = PermisooperacionServices(
            self.app, self.datos_system)
        self.estratificacion = EstratificacionService(
            self.app.conexion_saft, self.datos_system)
        self.estratificacion_sar = SARReportesService(
            self.app.conexion_saft, self.datos_system)
        self.ingresos_deptos = RptIngresosDeptosService(
            self.app.conexion_saft, self.datos_system)
        self.ingresos_deptos_diario = RptIngresosDeptosDiarioService(
            self.app.conexion_saft, self.datos_system)
        self.ingresos_deptos_mensual = RptIngresosDeptosMensualService(
            self.app.conexion_saft, self.datos_system)

    # BOTONES DE TRANCISION

    def rpt_trancicion_det_ip(self, e):
        asyncio.run(generar_reporte_trancicicon_det_ip(self, e))

    def rpt_trancicion_det_bi(self, e):
        asyncio.run(generar_reporte_trancicicon_det_bi(self, e))

    def rpt_trancicion_det_ics(self, e):
        asyncio.run(generar_reporte_trancicicon_det_ics(self, e))

    def rpt_trancicion_det_amp(self, e):
        asyncio.run(generar_reporte_trancicicon_det_amb(self, e))

    def rpt_trancicion_det_ist(self, e):
        asyncio.run(generar_reporte_trancicicon_det_ist(self, e))

    def rpt_trancicion_det_sp(self, e):
        asyncio.run(generar_reporte_trancicicon_det_sp(self, e))

    # BOTONES MORA

    def on_mora_bi(self, e):
        asyncio.run(generar_mora_bi(self, e))

    def on_mora_ip(self, e):
        asyncio.run(generar_mora_ip(self, e))

    def on_mora_ics(self, e):
        asyncio.run(generar_mora_ics(self, e))

    def on_mora_sp(self, e):
        asyncio.run(generar_mora_sp(self, e))
    # ABRIR MODALS

    def abrir_modal_mora_vs_ingresos(self, e):
        self.tipo_impuesto = 0
        self.dialog = abrir_modal_mora_vs_ingresos(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abrir_modal_mora_aldea_anio(self, e):
        self.ubicacion = 0
        self.cod_aldea = ''
        self.dialog = abrir_modal_mora_bi_aldea_anio(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abrir_modal_estratificacion_ine(self, e):
        self.tipo_empresa = 0
        self.anio = ''
        self.dialog = abrir_modal_estratificacion(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abrir_modal_estratificacion_sar(self, e):
        self.tipo_empresa = 0
        self.anio = ''
        self.dialog = abrir_modal_estratificacion_sar(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abril_modal_analisi_ingresos(self, e):
        self.anio = (datetime.date.year)
        self.dialog = abrir_analisis_ingresos(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abril_modal_trancicion(self, e):
        self.fecha_inicial = ''
        self.fecha_final = ''
        self.dialog = abrir_trancicicon_traspaso(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abril_modal_anula_pp(self, e):
        self.identidad = ''
        self.num_plan_pago = 0
        self.dialog = abrir_anula_plan_pago(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abril_modal_rpt_permisos_operacion(self, e):
        self.tipo_po = ''
        self.cod_aldea = ''
        self.cod_barrio = ''
        self.nombre_aldea = ''
        self.nombre_barrio = ''
        self.fecha_ini = ''
        self.fecha_fin = ''
        self.dialog = abrir_modal_rpt_permiso_operacion(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abril_modal_apremio_1er(self, e):
        self.tipo_impuesto = '%'
        self.tipo_persona = '%'
        self.dialog = abrir_modal_rpt_apremio_1er(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abrir_modal_ingresos_depto(self, e):
        self.fecha_ini = ''
        self.fecha_fin = ''
        self.dialog = abrir_modal_rpt_ingresos_depto(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abrir_modal_ingresos_detallados_depto(self, e):
        self.fecha_ini = ''
        self.fecha_fin = ''
        self.cod_depto = ''
        self.tipo_impuesto = ""
        self.dialog = abrir_modal_rpt_ingresos_detallados_depto(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abrir_modal_ingresos_bomberos(self, e):
        self.fecha_ini = ''
        self.fecha_fin = ''
        self.dialog = abrir_modal_rpt_bomberos(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abrir_modal_ingresos_diarios_depto(self, e):
        self.fecha_ini = ''
        self.fecha_fin = ''
        self.dialog = abrir_modal_rpt_ingresos_diarios_depto(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abrir_modal_ingresos_mensual_depto(self, e):
        self.anio = ''
        self.cod_depto = ''
        self.tipo_impuesto = ""
        self.dialog = abrir_modal_rpt_ingresos_mensual_depto(self, e)
        self.page.open(self.dialog)
        self.page.update()

    # CERRAR MODALS

    def cerrar_modal(self):
        self.dialog.open = False
        self.page.update()

    def generar_apremio_pdf(self, e):
        tipo_impuesto = self.tipo_impuesto.current.value
        tipo_persona = self.tipo_persona.current.value
        self.apremio.obtener_mora_gob(tipo_impuesto, tipo_persona)

    def generar_excel_aldea_mora(self, e):
        asyncio.run(generar_excel_mora_vs_ingresos(self, e))

    def generar_pdf_aldea_mora(self, e):
        asyncio.run(generar_pdf_mora_vs_ingresos(self, e))

    def generar_excel_mora_bi_aldea_anio(self, e):
        asyncio.run(generar_mora_bi_aldea_anio_excel(self, e))

    def generar_excel_estratificacion(self, e):
        asyncio.run(generar_excel_estratificacion(self, e))

    def generar_excel_estratificacion_sar(self, e):
        asyncio.run(generar_excel_estratificacion_sar(self, e))

    def generar_pdf_mora_bi_aldea_anio(self, e):
        asyncio.run(generar_mora_bi_aldea_anio_pdf(self, e))

    def generar_pdf_rpt_permiso_operacion(self, e):
        asyncio.run(generar_rpt_permiso_operacion_pdf(self, e))

    def generar_excel_rpt_permiso_operacion(self, e):
        asyncio.run(generar_rpt_permiso_operacion_pdf(self, e))

    def generar_exel_analisi_ingresos(self, e):
        asyncio.run(generar_analisis_ingresos(self, e))

    def generar_rpt_trancicion_traspaso(self, e):
        asyncio.run(generar_reporte_trancicicon(self, e))

    def generar_excel_ingreso_depto(self, e):
        asyncio.run(generar_reporte_excel_ingreso_depto(self, e))

    def generar_pdf_ingreso_depto(self, e):
        asyncio.run(generar_reporte_pdf_ingreso_depto(self, e))

    # 1 CATASTRO
    def generar_excel_ingreso_depto_detallado_catastro(self, e):
        asyncio.run(
            generar_reporte_excel_ingreso_depto_detallado_catastro(self, e))

    def generar_pdf_ingreso_depto_detallado_catastro(self, e):
        asyncio.run(
            generar_reporte_pdf_ingreso_depto_detallado_catastro(self, e))
    # 3 AMBIENTE

    def generar_excel_ingreso_depto_detallado_uma(self, e):
        asyncio.run(generar_reporte_excel_ingreso_depto_detallado_uma(self, e))

    def generar_pdf_ingreso_depto_detallado_uma(self, e):
        asyncio.run(generar_reporte_pdf_ingreso_depto_detallado_uma(self, e))

    def anular_plan_pago(self, e):
        asyncio.run(anula_plan_pago(self, e))

    # INGRESOS GENERALES POR DEPARTAMENTO

    def generar_excel_ingreso_depto(self, e):
        asyncio.run(generar_reporte_excel_ingreso_depto(self, e))

    def generar_pdf_ingreso_depto(self, e):
        asyncio.run(generar_reporte_pdf_ingreso_depto(self, e))

    # INGRESOS GENERALES POR DEPARTAMENTO DETALLADO
    def generar_excel_ingreso_depto_detallado(self, e):
        asyncio.run(
            generar_reporte_excel_ingreso_depto_detallado(self, e))

    def generar_pdf_ingreso_depto_detallado(self, e):
        asyncio.run(generar_reporte_pdf_ingreso_depto_detallado(self, e))

    def generar_excel_ingreso_depto_diario(self, e):
        asyncio.run(
            generar_reporte_excel_ingreso_depto_diario(self, e))

    def generar_pdf_ingreso_depto_diario(self, e):
        asyncio.run(generar_reporte_pdf_ingreso_depto_diario(self, e))

    def generar_pdf_ingreso_depto_mensual(self, e):
        asyncio.run(generar_reporte_pdf_ingreso_depto_mensual(self, e))

    # INGRESOS BOMBEROS
    def generar_excel_ingreso_bomberos(self, e):
        asyncio.run(generar_reporte_excel_bomberos(self, e))

    def generar_pdf_ingreso_bomberos(self, e):
        asyncio.run(generar_reporte_pdf_bomberos(self, e))
