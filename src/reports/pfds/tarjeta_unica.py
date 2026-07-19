
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, LEGAL, legal
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from src.reports.tablas.abonados_por_servicio import tabla_abonados_servicio
from src.reports.utils.firmas_pdf import tabla_frima_pdf_unica
from src.reports.utils.footer_pdf import otras_paginas, primera_pagina
from src.reports.utils.periodo_impresion_pdf import periodo_impresion_pdf, dia_impresion_pdf
from src.reports.utils.logo_mun_pdf import logo_muni_imagen
from src.reports.utils.tabla_titulo_pfd import titulo_horizontal, titulo_paragrap_pdf


class TarjetaUnicaReport:
    def __init__(self, datos, municipio, municipio_admin, titulo_reporte):
        self.datos = datos
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.administracion = municipio_admin


    def generar_pdf(self, ruta_salida="rpt_ingresos_depto_detatllado.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(legal), leftMargin=40,
                                rightMargin=40,
                                topMargin=20,
                                bottomMargin=20)
        elementos = []
        estilos = getSampleStyleSheet()
        ruta_base = r"C:\Program Files (x86)\SAFT\LogoMun"
        logo_mun = logo_muni_imagen(ruta_base)
        titulo = titulo_paragrap_pdf(
            self.municipio, self.titulo, estilos["Title"])

        tabla_titulo = titulo_horizontal(titulo, logo_mun, None)
        fecha = dia_impresion_pdf(estilos["Normal"])
        elementos.append(tabla_titulo)
        elementos.append(Spacer(1, 12))
        elementos.append(fecha)
        elementos.append(Spacer(1, 5))

        elementos.append(Spacer(1, 5))
        elementos.append(Spacer(1, 24))
        # CATASTRO
        
      
 
        tabla_firma = tabla_frima_pdf_unica(
            self.administracion["Tributaria"], "Jefe Administración Servicios Publicos", None)
        # TABLA ENCABEZADO
        
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
