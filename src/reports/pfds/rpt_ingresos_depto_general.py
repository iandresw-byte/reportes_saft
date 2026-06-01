
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from src.reports.tablas.ingresos_depto_general import tabla_ingresos_generales_depto
from src.reports.utils.firmas_pdf import tabla_frima_pdf_unica
from src.reports.utils.footer_pdf import otras_paginas, primera_pagina
from src.reports.utils.periodo_impresion_pdf import periodo_impresion_pdf, dia_impresion_pdf
from src.reports.utils.logo_mun_pdf import logo_muni_imagen
from src.reports.utils.tabla_titulo_pfd import titulo_vertical, titulo_paragrap_pdf


class RptIngresosDeptoGeneralReport:
    def __init__(self, datos, municipio, municipio_admin, titulo_reporte, nombre_aldea=None, nombre_barrio=None, fecha_ini=None, fecha_fin=None, depto=None, tipo_fact=None):
        self.datos = datos
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.administracion = municipio_admin
        self.depto = depto
        self.nombre_aldea = nombre_aldea,
        self.nombre_barrio = nombre_barrio,
        self.fecha_ini = fecha_ini,
        self.fecha_fin = fecha_fin
        self.tipo_factura = tipo_fact

    def generar_pdf(self, ruta_salida="rpt_ingresos_depto.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=letter, leftMargin=40,
                                rightMargin=40,
                                topMargin=20,
                                bottomMargin=20)
        elementos = []
        estilos = getSampleStyleSheet()
        ruta_base = r"C:\Program Files (x86)\SAFT\LogoMun"
        logo_mun = logo_muni_imagen(ruta_base)

        titulo = titulo_paragrap_pdf(
            self.municipio, self.titulo, estilos["Title"])

        tabla_titulo = titulo_vertical(titulo, logo_mun, None)
        fecha = dia_impresion_pdf(estilos["Normal"])
        elementos.append(tabla_titulo)
        elementos.append(Spacer(1, 12))
        elementos.append(fecha)

        elementos.append(Spacer(1, 5))
        elementos.append(Spacer(1, 24))

        tabla = tabla_ingresos_generales_depto(self.datos)
        elementos.append(tabla)
        tabla_firma = tabla_frima_pdf_unica(
            self.administracion["Tesorero"], "Jefe Tesoreria", None)

        elementos.append(Spacer(1, 100))
        elementos.append(tabla_firma)
        elementos.append(Spacer(1, 20))

        doc.build(
            elementos,
            onFirstPage=primera_pagina,
            onLaterPages=lambda canvas, doc: otras_paginas(
                canvas,
                doc,
                self.municipio,
                self.titulo
            )
        )
