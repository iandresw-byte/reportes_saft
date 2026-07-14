
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from src.reports.tablas.establecimientos_x_actividad import tabla_establecimietos_x_actividad_pdf
from src.reports.utils.firmas_pdf import tabla_frima_pdf_unica
from src.reports.utils.footer_pdf import otras_paginas, primera_pagina
from src.reports.utils.periodo_impresion_pdf import periodo_impresion_pdf, dia_impresion_pdf
from src.reports.utils.logo_mun_pdf import logo_muni_imagen
from src.reports.utils.tabla_titulo_pfd import titulo_horizontal, titulo_paragrap_pdf


class RptEstablecimientosActividadReport:
    def __init__(self, datos, municipio, municipio_admin, titulo_reporte, nombre_aldea=None, nombre_barrio=None, fecha_ini=None, fecha_fin=None, depto=None, tipo_fact=None, tipo_cta=0):
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
        self.tipo_cta = tipo_cta

    def generar_pdf(self, ruta_salida="rpt_ingresos_depto_detatllado.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(letter), leftMargin=40,
                                rightMargin=40,
                                topMargin=10,
                                bottomMargin=10)
        elementos = []
        estilos = getSampleStyleSheet()
        ruta_base = r"C:\Program Files (x86)\SAFT\LogoMun"
        logo_mun = logo_muni_imagen(ruta_base)
        titulo = titulo_paragrap_pdf(
            self.municipio, self.titulo, estilos["Title"])
        periodo_impresion = periodo_impresion_pdf(
            self.fecha_ini, self.fecha_fin, len(self.datos), estilos["Normal"])
        tabla_titulo = titulo_horizontal(titulo, logo_mun, None)
        fecha = dia_impresion_pdf(estilos["Normal"])
        elementos.append(tabla_titulo)
        elementos.append(Spacer(1, 12))
        elementos.append(fecha)
        elementos.append(Spacer(1, 5))
        elementos.append(periodo_impresion)
        elementos.append(Spacer(1, 5))
      
        # CATASTRO
        
        tabla = tabla_establecimietos_x_actividad_pdf(
            self.datos)
        elementos.append(tabla)
        tabla_firma = tabla_frima_pdf_unica(
            self.administracion["Tributaria"], "Jefe Administración Tributaria", None)
        # TABLA ENCABEZADO
        
        elementos.append(Spacer(1, 60))
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
