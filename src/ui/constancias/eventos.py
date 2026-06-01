# ui/reportes/eventos_reportes.py

from src.reports.licencia_ambiental_tocoa import LicenciaAmbientalTocoaReport

from src.ui.reports.utils_reportes import (
    ejecutar_reporte, snack_error_reporte
)


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


async def cargar_data_licencia_uma_ics(vista, e):
    num_recibo = vista.num_recibo.current.value
    titulo_rpt = "LICENCIA AMBIENTAL MUNCIPAL"
    if not num_recibo:
        snack_error_reporte(
            vista.page, f"Numero de recibo no valido! Recibo: {num_recibo}")
        return

    vista.cerrar_modal()

    await ejecutar_reporte(
        vista,
        e,
        "licencia_uma_ics.pdf",
        obtener_datos=lambda: vista.constancias.obtener_licencia_uma_ics(
            num_recibo),
        construir_reporte=lambda datos: LicenciaAmbientalTocoaReport(
            datos, vista.datos_muni, titulo_rpt, municipio_admin=vista.administracion
        ),
        tipo="pdf"
    )
