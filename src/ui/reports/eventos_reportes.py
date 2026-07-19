# ui/reportes/eventos_reportes.py

import os
import asyncio
from src.reports.pfds.rpt_abonados_x_servicio import RptAbonadosServicioReport
from src.reports.excel.mora_abonados_sp import AbonadosServiciosExcelReport
from src.reports.excel.mora_establecimientos import EstablecimientosExcelReport
from src.reports.pfds.rpt_establecimientos_x_actividad import RptEstablecimientosActividadReport
from src.reports.pfds.rpt_ingresos_depto_mensual import RptIngresosDeptoMensualReport
from src.reports.excel.ingresos_depto_detallado_tributaria import IngresosDeptosDetalladosTributariaReport
from src.reports.excel.ingresos_depto_detallado_justicia import IngresosDeptosDetalladosJusticiaReport
from src.reports.excel.ingresos_depto_detallado_procamut import IngresosDeptosDetalladosProcamutReport
from src.reports.excel.ingresos_depto_detallado_urbanismo import IngresosDeptosDetalladosUrbanismoReport
from src.reports.excel.ingresos_depto_detallado_secretaria import IngresosDeptosDetalladosSecretariaReport
from src.reports.pfds.tarjeta_unica import TarjetaUnicaReport
from src.reports.excel.ingresos_depto_diario import IngresosDeptosDiarioReport
from src.reports.pfds.rpt_ingresos_depto_general import RptIngresosDeptoGeneralReport
from src.reports.pfds.rpt_ingresos_depto_diario import RptIngresosDeptoDiarioReport
from src.reports.excel.rpt_pagos_bomberos import PagosBomberoReport
from src.reports.excel.estratificacion_rpt import EstratificacionReport
from src.reports.excel.estratificacion_sar import EstratificacionSARReport
from src.reports.excel.ingreso_deptos_rpt import IngresosDeptosReport
from src.reports.excel.ingresos_deptos_detallado_rpt_uma import IngresosDeptosDetalladosUMAReport
from src.reports.excel.ingresos_deptos_detallado_catastro_rpt import IngresosDeptosDetalladosCatastroReport
from src.reports.excel.analisis_ingresos_rpt import AnalisisIngresosReport
from src.reports.pfds.rpt_ingresos_depto_detallado import RptIngresosDeptoDetalladoReport
from src.reports.mora_bi_aldea_anio_report import MoravsBIAldeaAnioReport
from src.reports.reporte_permisos_operacion_report import RptPermisoOperacionReport
from src.reports.mora_bi_report import MoraBIReport
from src.reports.mora_ics_report import MoraICSReport
from src.reports.mora_sp_report import MoraSPReport
from src.reports.mora_vs_ingresos_aldea_report import MoravsIngresosAldeaReport
from src.reports.trancicion_report import TrancicionReport
from src.ui.reports.utils_reportes import (
    ejecutar_reporte, snack_inicio_reporte, snack_final_reporte, snack_error_reporte
)
from src.utils.config_manager import Config

RESULTADO_DIR = Config.obtener("RUTAS", "carpeta_reportes")


def obtener_titulo_impuesto(impuesto):
    return {
        "1": "BIENES INMUEBLES",
        "2,3": "INDUSTRIA COMERCIO Y SERVICIOS",
        "4": "IMPUESTO PERSONAL",
        "5": "SERVICIOS PUBLICOS",
        "7": "PLANES DE PAGO",
        "0,1,2,3,4,5,7": "TODAS LAS FACTURAS",
        "0": "OTRAS TASAS E IMPUESTOS"
    }.get(impuesto, "DESCONOCIDO, NO-CLASIFICADO")


async def generar_mora_bi(vista, e):
    await ejecutar_reporte(
        vista,
        e,
        "mora_bi_report.pdf",
        obtener_datos=lambda: (
            vista.mora_bi.obtener_mora_bi_sami()
            if vista.datos_system["TpoCuenta"]
            else vista.mora_bi.obtener_mora_bi_gob()
        ),
        construir_reporte=lambda datos: MoraBIReport(
            datos, vista.datos_muni, "BIENES INMUEBLES"
        ),
        tipo="pdf"
    )


async def generar_mora_ip(vista, e):
    await ejecutar_reporte(
        vista,
        e,
        "mora_ip_report.pdf",
        obtener_datos=lambda: vista.mora_ip.obtener_mora_ip(),
        construir_reporte=lambda datos: MoraBIReport(
            datos, vista.datos_muni, "IMPUESTO PERSONAL"
        ),
        tipo="pdf"
    )


async def generar_mora_ics(vista, e):
    await ejecutar_reporte(
        vista,
        e,
        "mora_ics_report.pdf",
        obtener_datos=lambda: (
            vista.mora_ics.obtener_mora_ics_sami()
            if vista.datos_system['TpoCuenta']
            else vista.mora_ics.obtener_mora_ics_gob()
        ),
        construir_reporte=lambda datos: MoraICSReport(
            *datos, municipio=vista.datos_muni, titulo_reporte="INDUSTRIA, COMERCIO Y SERVICIO"
        ),
        tipo="pdf"
    )


async def generar_mora_sp(vista, e):
    if vista.datos_system['TpoCuenta'] == 1:
        funcion = vista.mora_sp.obtener_mora_sp_sami
    else:
        funcion = vista.mora_sp.obtener_mora_sp_gob
    await ejecutar_reporte(
        vista,
        e,
        "mora_sp_report.pdf",
        obtener_datos=lambda: funcion(),
        construir_reporte=lambda datos: MoraSPReport(
            *datos, municipio=vista.datos_muni, titulo_reporte="SERVICIOS Y TASAS MUNICIPALES"
        ),
        tipo="pdf"
    )


async def generar_excel_mora_vs_ingresos(vista, e):
    impuesto = vista.tipo_impuesto.current.value
    titulo_rpt = obtener_titulo_impuesto(impuesto)

    if not impuesto:
        snack_error_reporte(vista.page, "Tipo de factura no selecionado")
        return

    vista.cerrar_modal()

    await ejecutar_reporte(
        vista,
        e,
        "mora_vs_ingresos_gral.xlsx",
        obtener_datos=lambda: vista.mora_aldea.mora_vs_ingresos_general(
            impuesto),
        construir_reporte=lambda datos: MoravsIngresosAldeaReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="excel"
    )


async def generar_tarjeta_unica(vista, e):
    identidad = vista.identidad.current.value
    titulo_rpt = "Tarjera Unica de Contribuyente"
    if not identidad:
        snack_error_reporte(vista.page, "Ingrese una Idetidad (Vacio)")
        return

    vista.cerrar_modal()

    await ejecutar_reporte(
        vista,
        e,
        "tarjeta_unica.pdf",
        obtener_datos=lambda: vista.registro.obtener_ruc(identidad),
        construir_reporte=lambda datos: TarjetaUnicaReport(
            datos, vista.datos_muni,vista.administracion, titulo_rpt
        ),
        tipo="pdf"
    )



async def generar_reporte_pdf_abonado_x_cuenta(vista, e):
    cta_cuentas = vista.cuenta_sp
    if not cta_cuentas:
        snack_error_reporte(vista.page, "No hay Cuentas para mostar")
        return
    titulo_rpt = "Abonados de Servicios Publicos - Detalle de Mora Por Servicio"
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "abonados_por_servicio.pdf",
        obtener_datos=lambda: vista.abonados_sp.get_abonado_x_servicio(cta_cuentas),
        construir_reporte=lambda datos: RptAbonadosServicioReport(
            datos, vista.datos_muni, vista.administracion,titulo_rpt
        ),
        tipo="pdf"
    )

async def generar_reporte_excel_abonado_x_cuenta(vista, e):
    cta_cuentas = vista.cuenta_sp
    if not cta_cuentas:
        snack_error_reporte(vista.page, "No hay Cuentas para mostar")
        return
    titulo_rpt = "Abonados de Servicios Publicos - Detalle de Mora Por Servicio"
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "abonados_por_servicio.xlsx",
        obtener_datos=lambda: vista.abonados_sp.get_abonado_x_servicio(cta_cuentas),
        construir_reporte=lambda datos: AbonadosServiciosExcelReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="excel"
    )

async def generar_reporte_pdf_establecimiento_por_actividad(vista, e):
    cta_cuentas = vista.cuenta_ics
    if not cta_cuentas:
        snack_error_reporte(vista.page, "No hay Cuentas para mostar")
        return
    titulo_rpt = "Establecimientos I.C.S. - Detalle de Mora por Actividad Economica"
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "rpt_mora_establecimientos_x_actividad.pdf",
        obtener_datos=lambda: vista.rpt_establecimientos.get_rpt_mora_x_actividad(cta_actividad=cta_cuentas["CtaIngreso"]),
        construir_reporte=lambda datos: RptEstablecimientosActividadReport(
            datos, vista.datos_muni, vista.administracion,titulo_rpt
        ),
        tipo="pdf"
    )

async def generar_reporte_excel_establecimiento_por_actividad(vista, e):
    cta_cuentas = vista.cuenta_ics

    if not cta_cuentas:
        snack_error_reporte(vista.page, "No hay Cuentas para mostar")
        return
    titulo_rpt = "Establecimientos I.C.S. - Detalle de Mora por Actividad Economica"

    vista.cerrar_modal()

    await ejecutar_reporte(
        vista,
        e,
        "rpt_mora_establecimientos_x_actividad.xlsx",
        obtener_datos=lambda: vista.rpt_establecimientos.get_rpt_mora_x_actividad(cta_actividad=cta_cuentas["CtaIngreso"]),
        construir_reporte=lambda datos: EstablecimientosExcelReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="excel"
    )

async def generar_pdf_mora_vs_ingresos(vista, e):
    impuesto = vista.tipo_impuesto.current.value
    titulo_rpt = obtener_titulo_impuesto(impuesto)

    if not impuesto:
        snack_error_reporte(vista.page, "Tipo de factura no selecionado")
        return

    vista.cerrar_modal()

    await ejecutar_reporte(
        vista,
        e,
        "mora_vs_ingresos_gral.pdf",
        obtener_datos=lambda: vista.mora_aldea.mora_vs_ingresos_general(
            impuesto),
        construir_reporte=lambda datos: MoravsIngresosAldeaReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="pdf"
    )


async def generar_reporte_trancicicon(vista, e):
    fecha_ini = vista.fecha_inicial
    fecha_fin = vista.fecha_final
    await ejecutar_reporte(
        vista,
        e,
        "transicion_report.pdf",
        obtener_datos=lambda: vista.trancicion.obtener_contribuyentes(
            fecha_ini, fecha_fin),
        construir_reporte=lambda datos: TrancicionReport(
            *datos, municipio=vista.datos_muni, titulo_reporte="TRANCISIÓN Y TRASPASO"
        ),
        tipo="pdf"
    )


async def generar_reporte_trancicicon_det_ip(vista, e):
    nombre_archivo = "trancicion_report_detalle_ip.xlsx"
    ruta = os.path.join(RESULTADO_DIR, "excel", nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_ip(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_trancicicon_det_bi(vista, e):
    nombre_archivo = "trancicion_report_detalle_bi.xlsx"
    ruta = os.path.join(RESULTADO_DIR, "excel", nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_bi(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_trancicicon_det_ics(vista, e):
    nombre_archivo = "trancicion_report_detalle_ics.xlsx"
    ruta = os.path.join(RESULTADO_DIR, "excel", nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_ics(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_trancicicon_det_ist(vista, e):
    nombre_archivo = "trancicion_report_detalle_ist.xlsx"
    ruta = os.path.join(RESULTADO_DIR, "excel", nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_ist(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_trancicicon_det_amb(vista, e):
    nombre_archivo = "trancicion_report_detalle_amb.xlsx"
    ruta = os.path.join(RESULTADO_DIR, "excel", nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_amb(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_trancicicon_det_sp(vista, e):
    nombre_archivo = "trancicion_report_detalle_sp.xlsx"
    ruta = os.path.join(RESULTADO_DIR, "excel", nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_sp(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_mora_bi_aldea_anio_pdf(vista, e):
    ubicacion = vista.ubicacion.current.value
    cod_aldea = vista.cod_aldea.current.value
    titulo_rpt = "Reporte Mora vs Ingresos BI - Año"

    if not cod_aldea:
        snack_error_reporte(vista.page, "No ha Seleccionada una Aldea")
        return
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "moral_vs_aldea_bi_anio.pdf",
        obtener_datos=lambda: vista.mora_aldea.mora_bi_ubicacion(
            cod_aldea, ubicacion),
        construir_reporte=lambda datos: MoravsBIAldeaAnioReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="pdf"
    )


async def generar_mora_bi_aldea_anio_excel(vista, e):
    ubicacion = vista.ubicacion.current.value
    cod_aldea = vista.cod_aldea.current.value
    titulo_rpt = "Reporte Mora vs Ingresos BI - Año"

    if not cod_aldea:
        snack_error_reporte(vista.page, "No ha Seleccionada una Aldea")
        return
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "moral_vs_aldea_bi_anio.xlsx",
        obtener_datos=lambda: vista.mora_aldea.mora_bi_ubicacion(
            cod_aldea, ubicacion),
        construir_reporte=lambda datos: MoravsBIAldeaAnioReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="excel"
    )


async def generar_excel_estratificacion(vista, e):
    tipo_empresa = vista.tipo_empresa.current.value
    anio = vista.anio.current.value

    titulo_rpt = "Reporte Estratificación Económica de Establecimientos"

    if not tipo_empresa:
        snack_error_reporte(
            vista.page, "No ha Seleccionada una estratificacion para la Empresa")
        return
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "moral_vs_aldea_bi_anio.xlsx",
        obtener_datos=lambda: vista.rpt_establecimientos.estratificacion(
            tipo_empresa, anio),
        construir_reporte=lambda datos: EstratificacionReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="excel"
    )


async def generar_excel_estratificacion_sar(vista, e):
    val_min = vista.val_min.current.value
    anio = vista.anio.current.value
    titulo_rpt = "Reporte Estratificación Económica de Establecimientos"

    if not anio:
        snack_error_reporte(
            vista.page, "No ha Seleccionada una estratificacion para la Empresa")
        return
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "moral_vs_aldea_bi_anio.xlsx",
        obtener_datos=lambda: vista.estratificacion_sar.declaraciones_sar(
            val_min, anio),
        construir_reporte=lambda datos: EstratificacionSARReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="excel"
    )


async def generar_analisis_ingresos(vista, e):
    anio = vista.anio.current.value
    titulo_rpt = f"Analis de Ingresos  vs"

    if not anio:
        snack_error_reporte(vista.page, "debe de ingresar un año")
        return
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "analisis_ingresos.xlsx",
        obtener_datos=lambda: vista.analisis.analisis_ingresos_anio_act_anio_ant(
            anio),
        construir_reporte=lambda datos: AnalisisIngresosReport(
            datos, vista.datos_muni, titulo_rpt, anio
        ),
        tipo="excel"
    )


async def anula_plan_pago(vista, e):
 
    num_plan_pago = int(vista.num_plan_pago.current.value)

    vista.cerrar_modal()
    vista.plan_pago.anular_plan_de_pago(vista, num_plan_pago=num_plan_pago)


async def generar_rpt_permiso_operacion_pdf(vista, e):
    tipo_po = vista.tipo_po.current.value
    fecha_ini = vista.fecha_ini
    fecha_fin = vista.fecha_fin
    cod_aldea = vista.cod_aldea.current.value
    cod_barrio = vista.cod_barrio.current.value
    nombre_aldea = vista.nombre_aldea
    nombre_barrio = vista.nombre_barrio
    titulo_rpt = "PERMISOS DE OPERACIÓN DE NEGOCIOS"

    if not cod_aldea:
        snack_error_reporte(vista.page, "No ha Seleccionada una Aldea")
        return
    if not cod_barrio:
        snack_error_reporte(
            vista.page, "No ha Seleccionado una Aldea/Barrio/Caserio")
        return
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "rpt_permiso_operacion.pdf",
        obtener_datos=lambda: vista.permiso_operacion.reporte_permiso_operacion(
            fecha_ini, fecha_fin, cod_aldea, cod_barrio, tipo_po),
        construir_reporte=lambda datos: RptPermisoOperacionReport(
            datos, vista.datos_muni, titulo_rpt, nombre_aldea, nombre_barrio, fecha_ini, fecha_fin, tipo_po
        ),
        tipo="pdf"
    )

# ingreso por departamento


async def generar_reporte_excel_ingreso_depto(vista, e):
    fecha_ini = vista.fecha_ini
    fecha_fin = vista.fecha_fin
    titulo_rpt = "REPORTE INGRESOS GENERALES POR DEPARTAMENTO"
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "rpt_ingresos_generl_depto.xlsx",
        obtener_datos=lambda: vista.ingresos_deptos.ingresos_general_deptos(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini),
        construir_reporte=lambda datos: IngresosDeptosReport(
            datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin
        ),
        tipo="excel"
    )


async def generar_reporte_pdf_ingreso_depto(vista, e):
    fecha_ini = vista.fecha_ini
    fecha_fin = vista.fecha_fin
    titulo_rpt = "REPORTE INGRESOS GENERALES POR DEPARTAMENTO"
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "reporte_ingreso_depto.pdf",
        obtener_datos=lambda: vista.ingresos_deptos.ingresos_general_deptos(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini),
        construir_reporte=lambda datos: RptIngresosDeptoGeneralReport(
            datos, vista.datos_muni, vista.administracion, titulo_rpt, fecha_ini, fecha_fin
        ),
        tipo="pdf"
    )
# EXCEL - GENERA EXCEL - GENERAL - EXCEL


async def generar_reporte_pdf_ingreso_depto_detallado(vista, e):
    fecha_ini = vista.fecha_ini
    fecha_fin = vista.fecha_fin
    cod_depto = vista.cod_depto.current.value
    tipo_impuesto = vista.tipo_impuesto.current.value
    vista.cerrar_modal()
    if cod_depto == "1":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE CATASTRO"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_catastro(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_detallado_catastro.pdf"
    elif cod_depto == "2":
        if tipo_impuesto == "0":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - OTRAS TASAS"
            fun_obtener = vista.ingresos_deptos.ingresos_diarios_tributaria_otras_tasas(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)
            nombre_archivo = "ingreso_depto_detallado_tributaria_ot.pdf"

        elif tipo_impuesto == "1":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - BIENES INMUEBLES"
            fun_obtener = vista.ingresos_deptos.ingresos_diarios_tributaria_inmuebles(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)
            nombre_archivo = "ingreso_depto_detallado_tributaria_bi.pdf"

        elif tipo_impuesto == "2,3":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - INDUSTRIA, COMERCIO Y SERVICIO"
            fun_obtener = vista.ingresos_deptos.ingresos_diarios_tributaria_comercio(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)
            nombre_archivo = "ingreso_depto_detallado_tributaria_ics.pdf"
        elif tipo_impuesto == "4":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - IMPUESTO PERSONAL"
            fun_obtener = vista.ingresos_deptos.ingresos_diarios_tributaria_personal(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)
            nombre_archivo = "ingreso_depto_detallado_tributaria_ip.pdf"

        elif tipo_impuesto == "8":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - ABONOS A FACTURA"
            fun_obtener = vista.ingresos_deptos.ingresos_diarios_tributaria_abonos(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)
            nombre_archivo = "ingreso_depto_detallado_tributaria_ab.pdf"

        else:
            return
    elif cod_depto == "3":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS A LA UNIDAD MUNICIPAL AMBIENTAL - UMA"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_uma(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_detallado_uma.pdf"
    elif cod_depto == "4":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DE LA DIRECCION DE JUSTICIA MUNICIPAL"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_justicia(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_detallado_justicia.pdf"
    elif cod_depto == "6":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO SECRETARIA MUNICIPAL"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_secretaria(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_detallado_secretaria.pdf"
    elif cod_depto == "7":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DE PROCAMUT"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_procamut(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_detallado_procamut.pdf"
    elif cod_depto == "8":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS UNIDAD DE DESARROLLO URBANO"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_desarrollo_urbano(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_detallado_desarrollo_urbano.pdf"

    else:
        return
    try:
        await ejecutar_reporte(
            vista,
            e,
            nombre_archivo,
            obtener_datos=lambda: fun_obtener,
            construir_reporte=lambda datos: RptIngresosDeptoDetalladoReport(
                datos, vista.datos_muni,  vista.administracion, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin, depto=cod_depto, tipo_fact=tipo_impuesto
            ),
            tipo="pdf"
        )
    except Exception as ex:
        snack_error_reporte(vista.page, ex)

# EXCEL - GENERAL - EXCEL - GENERAL - EXCEL


async def generar_reporte_excel_ingreso_depto_detallado(vista, e):
    fecha_ini = vista.fecha_ini
    fecha_fin = vista.fecha_fin
    cod_depto = vista.cod_depto.current.value
    tipo_impuesto = vista.tipo_impuesto.current.value
    if cod_depto == "1":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS A LA UNIDAD DE CATASTRO - CA"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_catastro(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        def reporte_excel(datos): return IngresosDeptosDetalladosCatastroReport(
            datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin
        )
        nombre_archivo = "ingreso_depto_detallado_catastro.xlsx"
    elif cod_depto == "2":
        if tipo_impuesto == "0":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - OTRAS TASAS"
            fun_obtener = vista.ingresos_deptos.ingresos_diarios_tributaria_otras_tasas(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)

            def reporte_excel(datos): return IngresosDeptosDetalladosTributariaReport(
                datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin, tipo_impuesto=tipo_impuesto
            )
            nombre_archivo = "ingreso_depto_detallado_tributaria_ot.xlsx"

        elif tipo_impuesto == "1":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - BIENES INMUEBLES"
            fun_obtener = vista.ingresos_deptos.ingresos_diarios_tributaria_inmuebles(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)

            def reporte_excel(datos): return IngresosDeptosDetalladosTributariaReport(
                datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin, tipo_impuesto=tipo_impuesto
            )
            nombre_archivo = "ingreso_depto_detallado_tributaria_bi.xlsx"

        elif tipo_impuesto == "2,3":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - INDUSTRIA, COMERCIO Y SERVICIO"
            fun_obtener = vista.ingresos_deptos.ingresos_diarios_tributaria_comercio(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)

            def reporte_excel(datos): return IngresosDeptosDetalladosTributariaReport(
                datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin, tipo_impuesto=tipo_impuesto
            )
            nombre_archivo = "ingreso_depto_detallado_tributaria_ics.xlsx"
        elif tipo_impuesto == "4":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - IMPUESTO PERSONAL"
            fun_obtener = vista.ingresos_deptos.ingresos_diarios_tributaria_personal(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)

            def reporte_excel(datos): return IngresosDeptosDetalladosTributariaReport(
                datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin, tipo_impuesto=tipo_impuesto
            )
            nombre_archivo = "ingreso_depto_detallado_tributaria_ip.xlsx"
        elif tipo_impuesto == "8":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - ABONOS A FACTURAS"
            fun_obtener = vista.ingresos_deptos.ingresos_diarios_tributaria_abonos(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)

            def reporte_excel(datos): return IngresosDeptosDetalladosTributariaReport(
                datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin, tipo_impuesto=tipo_impuesto
            )
            nombre_archivo = "ingreso_depto_detallado_tributaria_ab.xlsx"
        else:
            return None
    elif cod_depto == "3":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS A LA UNIDAD MUNICIPAL AMBIENTAL - UMA"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_uma(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        def reporte_excel(datos): return IngresosDeptosDetalladosUMAReport(
            datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin
        )  # type: ignore
        nombre_archivo = "ingreso_depto_detallado_uma.xlsx"
    elif cod_depto == "4":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS A LA DIRECCION MUNICIPAL DE JUSTICIA - UJM"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_justicia(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        def reporte_excel(datos): return IngresosDeptosDetalladosJusticiaReport(
            datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin
        )
        nombre_archivo = "ingreso_depto_detallado_justicia.xlsx"
    elif cod_depto == "5":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS CONTABILIDAD"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_justicia(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        def reporte_excel(datos): return IngresosDeptosDetalladosUMAReport(
            datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin
        )
        nombre_archivo = "ingreso_depto_detallado_contabilidad.xlsx"
    elif cod_depto == "6":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS SECRETARIA"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_secretaria(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        def reporte_excel(datos): return IngresosDeptosDetalladosSecretariaReport(
            datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin
        )
        nombre_archivo = "ingreso_depto_detallado_secretaria.xlsx"
    elif cod_depto == "7":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS PROCAMUD"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_procamut(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        def reporte_excel(datos): return IngresosDeptosDetalladosProcamutReport(
            datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin
        )
        nombre_archivo = "ingreso_depto_detallado_procamud.xlsx"
    elif cod_depto == "8":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DESARROLLO URBANO"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_desarrollo_urbano(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        def reporte_excel(datos): return IngresosDeptosDetalladosUrbanismoReport(
            datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin
        )
        nombre_archivo = "ingreso_depto_detallado_desarrollo_urbano.xlsx"
    elif cod_depto == "9":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS TESORERIA"
        fun_obtener = vista.ingresos_deptos.ingresos_diarios_uma(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        def reporte_excel(datos): return IngresosDeptosDetalladosUMAReport(
            datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin
        )
        nombre_archivo = "ingreso_depto_detallado_tesoreria.xlsx"

    else:
        return None
    vista.cerrar_modal()
    try:
        await ejecutar_reporte(
            vista,
            e,
            nombre_archivo,
            obtener_datos=lambda: fun_obtener,
            construir_reporte=reporte_excel,
            tipo="excel"
        )
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_excel_ingreso_depto_diario(vista, e):
    fecha_ini = vista.fecha_ini
    fecha_fin = vista.fecha_fin
    cod_depto = vista.cod_depto.current.value
    tipo_impuesto = vista.tipo_impuesto.current.value
    if cod_depto == "1":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS A LA UNIDAD DE CATASTRO - CA"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_catastro(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_diario_catastro.xlsx"
    elif cod_depto == "2":
        if tipo_impuesto == "0":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - OTRAS TASAS"
            fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_tributaria_otras_tasas(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)

            nombre_archivo = "ingreso_deptodiario_tributaria_ot.xlsx"

        elif tipo_impuesto == "1":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - BIENES INMUEBLES"
            fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_tributaria_inmuebles(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)

            nombre_archivo = "ingreso_depto_diario_tributaria_bi.xlsx"

        elif tipo_impuesto == "2,3":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - INDUSTRIA, COMERCIO Y SERVICIO"
            fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_tributaria_comercio(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)

            nombre_archivo = "ingreso_depto_diario_tributaria_ics.xlsx"
        elif tipo_impuesto == "4":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - IMPUESTO PERSONAL"
            fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_tributaria_personal(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)

            nombre_archivo = "ingreso_depto_diario_tributaria_ip.xlsx"
        elif tipo_impuesto == "8":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - ABONOS A FACTURAS"
            fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_tributaria_abonos(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)

            nombre_archivo = "ingreso_depto_diario_tributaria_ab.xlsx"

        else:
            return None
    elif cod_depto == "3":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS A LA UNIDAD MUNICIPAL AMBIENTAL - UMA"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_uma(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        nombre_archivo = "ingreso_depto_diario_uma.xlsx"
    elif cod_depto == "4":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS A LA DIRECCION MUNICIPAL DE JUSTICIA - UJM"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_justicia(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        nombre_archivo = "ingreso_depto_diario_justicia.xlsx"
    elif cod_depto == "5":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS CONTABILIDAD"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_justicia(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        nombre_archivo = "ingreso_depto_diario_contabilidad.xlsx"
    elif cod_depto == "6":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS SECRETARIA"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_secretaria(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        nombre_archivo = "ingreso_depto_diairio_secretaria.xlsx"
    elif cod_depto == "7":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS PROCAMUD"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_procamut(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        nombre_archivo = "ingreso_depto_diario_procamud.xlsx"
    elif cod_depto == "8":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DESARROLLO URBANO"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_desarrollo_urbano(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        nombre_archivo = "ingreso_depto_diario_desarrollo_urbano.xlsx"
    elif cod_depto == "9":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS TESORERIA"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_uma(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)

        nombre_archivo = "ingreso_depto_diario_tesoreria.xlsx"

    else:
        return None

    def reporte_excel(datos): return IngresosDeptosDiarioReport(
        datos, vista.datos_muni, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin, depto=cod_depto, tipo_impuesto=tipo_impuesto
    )
    vista.cerrar_modal()
    try:
        await ejecutar_reporte(
            vista,
            e,
            nombre_archivo,
            obtener_datos=lambda: fun_obtener,
            construir_reporte=reporte_excel,
            tipo="excel"
        )
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_pdf_ingreso_depto_diario(vista, e):
    fecha_ini = vista.fecha_ini
    fecha_fin = vista.fecha_fin
    cod_depto = vista.cod_depto.current.value
    tipo_impuesto = vista.tipo_impuesto.current.value
    vista.cerrar_modal()
    if cod_depto == "1":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE CATASTRO"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_catastro(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_diario_catastro.pdf"
    elif cod_depto == "2":
        if tipo_impuesto == "0":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - OTRAS TASAS"
            fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_tributaria_otras_tasas(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)
            nombre_archivo = "ingreso_depto_diario_tributaria_ot.pdf"

        elif tipo_impuesto == "1":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - BIENES INMUEBLES"
            fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_tributaria_inmuebles(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)
            nombre_archivo = "ingreso_depto_diario_tributaria_bi.pdf"

        elif tipo_impuesto == "2,3":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - INDUSTRIA, COMERCIO Y SERVICIO"
            fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_tributaria_comercio(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)
            nombre_archivo = "ingreso_depto_diario_tributaria_ics.pdf"
        elif tipo_impuesto == "4":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - IMPUESTO PERSONAL"
            fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_tributaria_personal(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)
            nombre_archivo = "ingreso_depto_diario_tributaria_ip.pdf"
        elif tipo_impuesto == "8":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - ABONOS A FACTURAS"
            fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_tributaria_abonos(
                fecha_fin=fecha_fin, fecha_ini=fecha_ini)
            nombre_archivo = "ingreso_depto_diario_tributaria_ab.pdf"

        else:
            return
    elif cod_depto == "3":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS A LA UNIDAD MUNICIPAL AMBIENTAL - UMA"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_uma(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_diario_uma.pdf"
    elif cod_depto == "4":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DE LA DIRECCION DE JUSTICIA MUNICIPAL"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_justicia(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_diario_justicia.pdf"
    elif cod_depto == "6":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO SECRETARIA MUNICIPAL"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_secretaria(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_diario_secretaria.pdf"
    elif cod_depto == "7":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DE PROCAMUT"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_procamut(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_diario_procamut.pdf"
    elif cod_depto == "8":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS UNIDAD DE DESARROLLO URBANO"
        fun_obtener = vista.ingresos_deptos_diario.ingresos_diarios_desarrollo_urbano(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini)
        nombre_archivo = "ingreso_depto_diario_desarrollo_urbano.pdf"

    else:
        return
    try:
        await ejecutar_reporte(
            vista,
            e,
            nombre_archivo,
            obtener_datos=lambda: fun_obtener,
            construir_reporte=lambda datos: RptIngresosDeptoDiarioReport(
                datos, vista.datos_muni,  vista.administracion, titulo_rpt, fecha_ini=fecha_ini, fecha_fin=fecha_fin, depto=cod_depto, tipo_fact=tipo_impuesto
            ),
            tipo="pdf"
        )
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_pdf_ingreso_depto_mensual(vista, e):
    anio = vista.anio.current.value

    cod_depto = vista.cod_depto.current.value
    tipo_impuesto = vista.tipo_impuesto.current.value
    vista.cerrar_modal()
    if cod_depto == "1":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE CATASTRO"
        fun_obtener = vista.ingresos_deptos_mensual.ingresos_mensual_catastro(
            anio=anio)
        nombre_archivo = "ingreso_depto_mensual_catastro.pdf"
    elif cod_depto == "2":
        if tipo_impuesto == "0":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - OTRAS TASAS"
            fun_obtener = vista.ingresos_deptos_mensual.ingresos_mensual_tributaria_otras_tasas(
                anio=anio)
            nombre_archivo = "ingreso_depto_mensual_tributaria_ot.pdf"

        elif tipo_impuesto == "1":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - BIENES INMUEBLES"
            fun_obtener = vista.ingresos_deptos_mensual.ingresos_mensual_tributaria_inmuebles(
                anio=anio)
            nombre_archivo = "ingreso_depto_mensual_tributaria_bi.pdf"

        elif tipo_impuesto == "2,3":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - INDUSTRIA, COMERCIO Y SERVICIO"
            fun_obtener = vista.ingresos_deptos_mensual.ingresos_mensual_tributaria_comercio(
                anio=anio)
            nombre_archivo = "ingreso_depto_mensual_tributaria_ics.pdf"
        elif tipo_impuesto == "4":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - IMPUESTO PERSONAL"
            fun_obtener = vista.ingresos_deptos_mensual.ingresos_mensual_tributaria_personal(
                anio=anio)
            nombre_archivo = "ingreso_depto_mensual_tributaria_ip.pdf"
        elif tipo_impuesto == "8":
            titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO DE ADMINISTRACION TRIBUTARIA - ABONOS A FACTURAS"
            fun_obtener = vista.ingresos_deptos_mensual.ingresos_mensual_tributaria_abonos(
                anio=anio)
            nombre_archivo = "ingreso_depto_mensual_tributaria_ip.pdf"

        else:
            return
    elif cod_depto == "3":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS A LA UNIDAD MUNICIPAL AMBIENTAL - UMA"
        fun_obtener = vista.ingresos_deptos_mensual.ingresos_mensual_uma(
            anio=anio)
        nombre_archivo = "ingreso_depto_mensual_uma.pdf"
    elif cod_depto == "4":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DE LA DIRECCION DE JUSTICIA MUNICIPAL"
        fun_obtener = vista.ingresos_deptos_mensual.ingresos_mensual_justicia(
            anio=anio)
        nombre_archivo = "ingreso_depto_mensual_justicia.pdf"
    elif cod_depto == "6":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DEL DEPARTAMENTO SECRETARIA MUNICIPAL"
        fun_obtener = vista.ingresos_deptos_mensual.ingresos_mensual_secretaria(
            anio=anio)
        nombre_archivo = "ingreso_depto_mensual_secretaria.pdf"
    elif cod_depto == "7":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS DE PROCAMUT"
        fun_obtener = vista.ingresos_deptos_mensual.ingresos_mensual_procamut(
            anio=anio)
        nombre_archivo = "ingreso_depto_mensual_procamut.pdf"
    elif cod_depto == "8":
        titulo_rpt = "REPORTE DIARIO DE INGRESOS UNIDAD DE DESARROLLO URBANO"
        fun_obtener = vista.ingresos_deptos_mensual.ingresos_mensual_desarrollo_urbano(
            anio=anio)
        nombre_archivo = "ingreso_depto_mensual_desarrollo_urbano.pdf"

    else:
        snack_error_reporte(vista.page, "Parametros no Validos")
        return
    try:
        await ejecutar_reporte(
            vista,
            e,
            nombre_archivo,
            obtener_datos=lambda: fun_obtener,
            construir_reporte=lambda datos: RptIngresosDeptoMensualReport(
                datos, vista.datos_muni,  vista.administracion, titulo_rpt,  depto=cod_depto, tipo_fact=tipo_impuesto
            ),
            tipo="pdf"
        )
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_pdf_bomberos(vista, e):
    fecha_ini = vista.fecha_ini
    fecha_fin = vista.fecha_fin
    titulo_rpt = "REPORTE INGRESOS SERVICIO DE BOMBEROS"
    tipo_cta = vista.datos_system["TpoCuenta"]

    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "reporte_ingreso_bomberos.pdf",
        obtener_datos=lambda: vista.ingresos_bombero.obtener_pagos_bomberos(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini, tipo_cta=tipo_cta),
        construir_reporte=lambda datos: RptIngresosDeptoDetalladoReport(
            datos, vista.datos_muni, vista.administracion, titulo_rpt, fecha_ini, fecha_fin, depto="BOMBEROS", tipo_cta=tipo_cta
        ),
        tipo="pdf"
    )


async def generar_reporte_excel_bomberos(vista, e):
    fecha_ini = vista.fecha_ini
    fecha_fin = vista.fecha_fin
    titulo_rpt = "REPORTE INGRESOS SERVICIO DE BOMBEROS"
    tipo_cta = vista.datos_system["TpoCuenta"]
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "reporte_ingreso_bomberos.xlsx",
        obtener_datos=lambda: vista.ingresos_bombero.obtener_pagos_bomberos(
            fecha_fin=fecha_fin, fecha_ini=fecha_ini, tipo_cta=tipo_cta),
        construir_reporte=lambda datos: PagosBomberoReport(
            datos, vista.datos_muni,  titulo_rpt, fecha_ini, fecha_fin, tipo_cta
        ),
        tipo="excel"
    )
