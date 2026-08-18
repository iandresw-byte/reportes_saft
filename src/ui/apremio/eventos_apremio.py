

from src.reports.pfds.apremio.apremio_carta_sami_report import ApremioCartaSAMIReport
from src.reports.pfds.apremio.apremio_carta_gob_report import ApremioCartaGobReport
from src.reports.pfds.apremio.apremio_media_carta_gob_report import ApremioMediaCartaGobReport
from src.reports.pfds.apremio.apremio_media_carta_sami_report import ApremioMediaCartaSAMIReport
from src.reports.pfds.apremio.apremio_original_copia_gob_report import ApremioOriginalCopiaGobReport
from src.reports.pfds.apremio.apremio_original_copia_sami_report import ApremioOriginalCopiaSAMIReport
from flet import Ref
import time




from src.ui.reports.utils_reportes import (
    ejecutar_reporte)


async def generar_aviso_cobro(vista,app,  e,):
    tipo_impuesto = vista.tipo_impuesto.current.value
    tipo_persona = vista.tipo_persona.current.value
    cod_aldea = vista.cod_aldea.current.value
    cod_barrio = vista.cod_barrio.current.value
    mora_mayor = vista.mora_mayor.current.value
    fecha_minima = vista.fecha_minima
    num_requerimientos = int(vista.num_avisos.current.value)
    tipo_cta_sami = bool(vista.datos_system["TpoCuenta"])
    from src.utils.config_manager import Config
    TIPO_REPORTE = Config.obtener("APREMIO", "tipo_documento")
    app.tamanio_documento
    titulo_reporte = "AVISO DE COBRO"
    if app.tamanio_documento == "OriginalCopiaCarta":
        if tipo_cta_sami:
            def reporte_apremio(datos): return ApremioOriginalCopiaSAMIReport(
                datos, vista.datos_muni,vista.datos_muni_admin,  titulo_reporte
            )
        else:
            def reporte_apremio(datos): return ApremioOriginalCopiaGobReport(
                datos, vista.datos_muni,vista.datos_muni_admin,  titulo_reporte, True
            )
    elif app.tamanio_documento == "MediaCarta":
        if tipo_cta_sami:
            def reporte_apremio(datos): return ApremioMediaCartaSAMIReport(
                datos, vista.datos_muni,vista.datos_muni_admin,  titulo_reporte
            )
        else:
            def reporte_apremio(datos): return ApremioMediaCartaGobReport(
                datos, vista.datos_muni, vista.datos_muni_admin,  titulo_reporte
            )
    else:
        if tipo_cta_sami:
                def reporte_apremio(datos): return ApremioCartaSAMIReport(
                datos, vista.datos_muni, vista.datos_muni_admin,titulo_reporte
            )
        else:

            def reporte_apremio(datos): return ApremioCartaGobReport(
                datos, vista.datos_muni,vista.datos_muni_admin, titulo_reporte
            )
    id = int(time.time())
    
    await ejecutar_reporte(
        vista,
        e,
        f"aviso_cobro_{id}.pdf",
        obtener_datos=lambda: vista.apremio.obtener_mora_gob(
            tipo_impuesto, tipo_persona, cod_aldea, cod_barrio, 0, num_requerimientos, mora_mayor, fecha_minima),
        construir_reporte=reporte_apremio,
        tipo="pdf"
    )


async def generar_primer_requerimiento(vista,app,  e,):
    tipo_impuesto = vista.tipo_impuesto.current.value
    tipo_persona = vista.tipo_persona.current.value
    cod_aldea = vista.cod_aldea.current.value
    cod_barrio = vista.cod_barrio.current.value
    mora_mayor = vista.mora_mayor.current.value
    fecha_minima = vista.fecha_minima
    num_requerimientos = int(vista.num_avisos.current.value)
    tipo_cta_sami = bool(vista.datos_system["TpoCuenta"])
    from src.utils.config_manager import Config
    TIPO_REPORTE = Config.obtener("APREMIO", "tipo_documento")
    app.tamanio_documento
    
    if app.tamanio_documento == "OriginalCopiaCarta":
        if tipo_cta_sami:
            def reporte_apremio(datos): return ApremioOriginalCopiaSAMIReport(
                datos, vista.datos_muni, vista.datos_muni_admin, "1er REQUERIMIENTO DE PAGO"
            )
        else:
            def reporte_apremio(datos): return ApremioOriginalCopiaGobReport(
                datos, vista.datos_muni, vista.datos_muni_admin, "1er REQUERIMIENTO DE PAGO"
            )
    elif app.tamanio_documento == "MediaCarta":
        if tipo_cta_sami:
            def reporte_apremio(datos): return ApremioMediaCartaSAMIReport(
                datos, vista.datos_muni, vista.datos_muni_admin, "1er REQUERIMIENTO DE PAGO"
            )
        else:
            def reporte_apremio(datos): return ApremioMediaCartaGobReport(
                datos, vista.datos_muni, vista.datos_muni_admin, "1er REQUERIMIENTO DE PAGO"
            )
    else:
        if tipo_cta_sami:
                def reporte_apremio(datos): return ApremioCartaSAMIReport(
                datos, vista.datos_muni,vista.datos_muni_admin, "1er REQUERIMIENTO DE PAGO"
            )
        else:

            def reporte_apremio(datos): return ApremioCartaGobReport(
                datos, vista.datos_muni,vista.datos_muni_admin, "1er REQUERIMIENTO DE PAGO"
            )
    id = int(time.time())
    await ejecutar_reporte(
        vista,
        e,
        f"apremio_1er{id}.pdf",
        obtener_datos=lambda: vista.apremio.obtener_mora_gob(
            tipo_impuesto, tipo_persona, cod_aldea, cod_barrio, 1, num_requerimientos, mora_mayor, fecha_minima),
        construir_reporte=reporte_apremio,
        tipo="pdf"
    )


async def generar_primer_requerimiento_individual(vista,app, e,):
    if isinstance(vista.identidad ,Ref):
        vista.identidad = vista.identidad.current.value
    from src.utils.config_manager import Config
    TIPO_REPORTE = Config.obtener("APREMIO", "tipo_documento")

    tipo_cta_sami = bool(vista.datos_system["TpoCuenta"])
    if app.tamanio_documento == "OriginalCopiaCarta":
        if tipo_cta_sami:
            def reporte_apremio(datos): return ApremioOriginalCopiaSAMIReport(
                datos, vista.datos_muni,vista.datos_muni_admin,  "1er REQUERIMIENTO DE PAGO"
            )
        else:
            def reporte_apremio(datos): return ApremioOriginalCopiaGobReport(
                datos, vista.datos_muni,vista.datos_muni_admin,  "1er REQUERIMIENTO DE PAGO"
            )
    elif app.tamanio_documento == "MediaCarta":
        if tipo_cta_sami:
            def reporte_apremio(datos): return ApremioMediaCartaSAMIReport(
                datos, vista.datos_muni, vista.datos_muni_admin, "1er REQUERIMIENTO DE PAGO"
            )
        else:
            def reporte_apremio(datos): return ApremioMediaCartaGobReport(
                datos, vista.datos_muni,vista.datos_muni_admin,  "1er REQUERIMIENTO DE PAGO"
            )
    else:
        if tipo_cta_sami:
                def reporte_apremio(datos): return ApremioCartaSAMIReport(
                datos, vista.datos_muni,vista.datos_muni_admin, "1er REQUERIMIENTO DE PAGO"
            )
        else:

            def reporte_apremio(datos): return ApremioCartaGobReport(
                datos, vista.datos_muni, vista.datos_muni_admin,"1er REQUERIMIENTO DE PAGO"
            )
            
    await ejecutar_reporte(
        vista,
        e,
        "apremio_1er.pdf",
        obtener_datos=lambda: vista.apremio.iniar_proceso_individual(
            vista.data_contribuyente, vista.tipo_doc, vista.identidad),
        construir_reporte=reporte_apremio,
        tipo="pdf"
    )


async def generar_segundo_requerimiento(vista,app, e,):
    tipo_impuesto = vista.tipo_impuesto.current.value
    tipo_persona = vista.tipo_persona.current.value
    cod_aldea = vista.cod_aldea.current.value
    cod_barrio = vista.cod_barrio.current.value
    from src.utils.config_manager import Config
    TIPO_REPORTE = Config.obtener("APREMIO", "tipo_documento")

    if isinstance(vista.identidad ,Ref):
        vista.identidad = vista.identidad.current.value


    tipo_cta_sami = bool(vista.datos_system["TpoCuenta"])
    if app.tamanio_documento == "OriginalCopiaCarta":
        if tipo_cta_sami:
            await ejecutar_reporte(
                    vista,
                    e,
                    "apremio_2do.pdf",
                    obtener_datos=lambda: vista.apremio.obtener_mora_gob(tipo_impuesto, tipo_persona, cod_aldea, cod_barrio, 2),
                    construir_reporte=lambda datos: ApremioOriginalCopiaSAMIReport(datos, vista.datos_muni,vista.datos_muni_admin,  "2do REQUERIMIENTO DE PAGO"),
                    tipo="pdf"
                    )
        else:
            await ejecutar_reporte(
                vista,
                e,
                "apremio_2do.pdf",
                obtener_datos=lambda: vista.apremio.obtener_mora_gob(tipo_impuesto, tipo_persona, cod_aldea, cod_barrio, 2),
                construir_reporte=lambda datos: ApremioOriginalCopiaGobReport(datos, vista.datos_muni,vista.datos_muni_admin,  "2do REQUERIMIENTO DE PAGO"),
                tipo="pdf"
                )
    elif app.tamanio_documento == "MediaCarta":
        if tipo_cta_sami:
            await ejecutar_reporte(
            vista,
            e,
            "apremio_2do.pdf",
            obtener_datos=lambda: vista.apremio.obtener_mora_gob(tipo_impuesto, tipo_persona, cod_aldea, cod_barrio, 2),
            construir_reporte=lambda datos: ApremioMediaCartaSAMIReport(datos, vista.datos_muni,vista.datos_muni_admin,  "2do REQUERIMIENTO DE PAGO"),
            tipo="pdf")
        else:
            await ejecutar_reporte(
                    vista,
                    e,
                    "apremio_2do.pdf",
                    obtener_datos=lambda: vista.apremio.obtener_mora_gob(tipo_impuesto, tipo_persona, cod_aldea, cod_barrio, 2),
                    construir_reporte=lambda datos: ApremioMediaCartaGobReport(datos, vista.datos_muni,vista.datos_muni_admin,  "2do REQUERIMIENTO DE PAGO"),
                    tipo="pdf"
                )
    else:
        if tipo_cta_sami:
               await ejecutar_reporte(
                    vista,
                    e,
                    "apremio_2do.pdf",
                    obtener_datos=lambda: vista.apremio.obtener_mora_gob(tipo_impuesto, tipo_persona, cod_aldea, cod_barrio, 2),
                    construir_reporte=lambda datos: ApremioCartaSAMIReport(datos, vista.datos_muni, vista.datos_muni_admin, "2do REQUERIMIENTO DE PAGO"),
                    tipo="pdf"
                )
        else:
            await ejecutar_reporte(
                vista,
                e,
                "apremio_2do.pdf",
                obtener_datos=lambda: vista.apremio.obtener_mora_gob(
                    tipo_impuesto, tipo_persona, cod_aldea, cod_barrio, 2),
                construir_reporte=lambda datos: ApremioCartaGobReport(
                    datos, vista.datos_muni,vista.datos_muni_admin,  "2do REQUERIMIENTO DE PAGO"
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
        construir_reporte=lambda datos: ApremioOriginalCopiaGobReport(
            datos, vista.datos_muni,vista.datos_muni_admin,  "CERTIFICACION DE FALTA DE PAGO"
        ),
        tipo="pdf"
    )


async def reiniciar_primer_requerimiento(vista, fila,app, e,):
    from src.utils.config_manager import Config
    TIPO_REPORTE = Config.obtener("APREMIO", "tipo_documento")
    tipo_cta_sami = bool(vista.datos_system["TpoCuenta"])
    if app.tamanio_documento == "OriginalCopiaCarta":
        if tipo_cta_sami:
            def reporte_apremio(datos): return ApremioOriginalCopiaSAMIReport(
                datos, vista.datos_muni,vista.datos_muni_admin,  "1er REQUERIMIENTO DE PAGO"
            )
        else:
            def reporte_apremio(datos): return ApremioOriginalCopiaGobReport(
                datos, vista.datos_muni, vista.datos_muni_admin, "1er REQUERIMIENTO DE PAGO"
            )
    elif app.tamanio_documento == "MediaCarta":
        if tipo_cta_sami:
            def reporte_apremio(datos): return ApremioMediaCartaSAMIReport(
                datos, vista.datos_muni,vista.datos_muni_admin,  "1er REQUERIMIENTO DE PAGO"
            )
        else:
            def reporte_apremio(datos): return ApremioMediaCartaGobReport(
                datos, vista.datos_muni, vista.datos_muni_admin, "1er REQUERIMIENTO DE PAGO"
            )
    else:
        if tipo_cta_sami:
                def reporte_apremio(datos): return ApremioCartaSAMIReport(
                datos, vista.datos_muni, vista.datos_muni_admin,"1er REQUERIMIENTO DE PAGO"
            )
        else:

            def reporte_apremio(datos): return ApremioCartaGobReport(
                datos, vista.datos_muni,vista.datos_muni_admin, "1er REQUERIMIENTO DE PAGO"
            )
    await ejecutar_reporte(
        vista,
        e,
        "apremio_1er.pdf",
        obtener_datos=lambda: vista.apremio.reinicar_proceso(fila),
        construir_reporte=reporte_apremio,
        tipo="pdf"
    )
    

def obtener_contriuyente(vista):
    if not isinstance(vista.identidad, str):
        dni = vista.identidad.current.value
    else:
        dni = vista.identidad
    data = vista.contribuente.obtener_datos_contribuyente(identidad=dni)
    data_1 = vista.contribuente.obtener_datos_contribuyente_proceso(
        identidad=dni)

    return data


def obtener_contriuyente_proceso(vista):
    if isinstance(vista.identidad, Ref):
        dni = vista.identidad.current.value
    else:
        dni = vista.identidad
    data = vista.contribuente.obtener_datos_contribuyente_proceso(
        identidad=dni)

    return data
