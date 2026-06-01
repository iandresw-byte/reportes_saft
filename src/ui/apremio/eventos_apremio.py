
from src.reports.apremio_report import ApremioReport
from src.ui.reports.utils_reportes import (
    ejecutar_reporte)


async def generar_primer_requerimiento(vista, e,):
    tipo_impuesto = vista.tipo_impuesto.current.value
    tipo_persona = vista.tipo_persona.current.value
    cod_aldea = vista.cod_aldea.current.value
    cod_barrio = vista.cod_barrio.current.value
    mora_mayor = vista.mora_mayor.current.value
    fecha_minima = vista.fecha_minima
    num_requerimientos = int(vista.num_avisos.current.value)
    await ejecutar_reporte(
        vista,
        e,
        "apremio_1er.pdf",
        obtener_datos=lambda: vista.apremio.obtener_mora_gob(
            tipo_impuesto, tipo_persona, cod_aldea, cod_barrio, 1, num_requerimientos, mora_mayor, fecha_minima),
        construir_reporte=lambda datos: ApremioReport(
            datos, vista.datos_muni, "1er REQUERIMIENTO DE PAGO"
        ),
        tipo="pdf"
    )


async def generar_primer_requerimiento_individual(vista, e,):

    await ejecutar_reporte(
        vista,
        e,
        "apremio_1er.pdf",
        obtener_datos=lambda: vista.apremio.iniar_proceso_individual(
            vista.data_contribuyente, vista.tipo_doc, vista.identidad),

        construir_reporte=lambda datos: ApremioReport(
            datos, vista.datos_muni, "1er REQUERIMIENTO DE PAGO"
        ),
        tipo="pdf"
    )


async def generar_segundo_requerimiento(vista, e,):
    tipo_impuesto = vista.tipo_impuesto.current.value
    tipo_persona = vista.tipo_persona.current.value
    cod_aldea = vista.cod_aldea.current.value
    cod_barrio = vista.cod_barrio.current.value
    await ejecutar_reporte(
        vista,
        e,
        "apremio_2do.pdf",
        obtener_datos=lambda: vista.apremio.obtener_mora_gob(
            tipo_impuesto, tipo_persona, cod_aldea, cod_barrio, 2),
        construir_reporte=lambda datos: ApremioReport(
            datos, vista.datos_muni, "2do REQUERIMIENTO DE PAGO"
        ),
        tipo="pdf"
    )


async def generar_certificacion(vista, e,):
    tipo_impuesto = vista.tipo_impuesto.current.value
    tipo_persona = vista.tipo_persona.current.value
    cod_aldea = vista.cod_aldea.current.value
    cod_barrio = vista.cod_barrio.current.value
    await ejecutar_reporte(
        vista,
        e,
        "apremio_cerificacion.pdf",
        obtener_datos=lambda: vista.apremio.obtener_mora_gob(
            tipo_impuesto, tipo_persona, cod_aldea, cod_barrio, 3),
        construir_reporte=lambda datos: ApremioReport(
            datos, vista.datos_muni, "CERTIFICACION DE FALTA DE PAGO"
        ),
        tipo="pdf"
    )


async def reiniciar_primer_requerimiento(vista, fila, e,):

    await ejecutar_reporte(
        vista,
        e,
        "apremio.pdf",
        obtener_datos=lambda: vista.apremio.reinicar_proceso(fila),
        construir_reporte=lambda datos: ApremioReport(
            datos, vista.datos_muni, "IMPUESTOS, TASAS Y SERVICIOS MUNICIPALES EN MORA"
        ),
        tipo="pdf"
    )


def obtener_contriuyente(vista):
    dni = vista.identidad.current.value
    data = vista.contribuente.obtener_datos_contribuyente(identidad=dni)
    data_1 = vista.contribuente.obtener_datos_contribuyente_proceso(
        identidad=dni)

    return data


def obtener_contriuyente_proceso(vista):
    dni = vista.identidad.current.value
    data = vista.contribuente.obtener_datos_contribuyente_proceso(
        identidad=dni)

    return data
