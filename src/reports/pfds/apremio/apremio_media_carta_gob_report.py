from pathlib import Path
import sys

import qrcode
import os
from reportlab.platypus import SimpleDocTemplate, Table, Image, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.platypus import HRFlowable

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter, HALF_LETTER, landscape
from datetime import datetime
from io import BytesIO
from src.reports.tablas.tabla_aviso_cobro import tabla_aviso_mora_media_carta
from src.reports.utils.firmas_pdf import tabla_frima_admin_fima_recibido
from src.reports.pfds.apremio.crea_aviso import crear_aviso_original
from src.reports.utils.tabla_titulo_pfd import titulo_mudia_carta
from src.reports.utils.logo_mun_pdf import logo_muni_imagen_media_carta
from src.ui.components.ui_style_table import columa_style, estilos_parrafo, fila_style, fila_style_moneda
from src.ui.components.ui_style_pdf import getSampleStyleSheet as estilos_mod


class ApremioMediaCartaGobReport:
    def __init__(self, lista_datos, municipio, titulo_reporte):
        self.lista_datos = lista_datos
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.num_requerimiento = "1er"
        self.margen = 0.4*cm

    def generar_pdf(self, ruta_salida):
        doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(HALF_LETTER),
                                leftMargin=self.margen,
                                rightMargin=self.margen,
                                topMargin=self.margen,
                                bottomMargin=self.margen)
        elementos = []
        estilos = estilos_mod()
        ruta_base = r"C:\Program Files (x86)\SAFT\LogoMun"
        if getattr(sys, 'frozen', False):
            BASE_DIR = Path(sys.executable).parent
        else:
            BASE_DIR = r"C:\Users\iAndresw\RepositorioLocal\reportes_saft"
        
        logo_mun = logo_muni_imagen_media_carta(ruta_base)
        firma_admin = ''
        if self.municipio["CodMuni"] == "1807":
            DIR_FIRMA= os.path.join(BASE_DIR,  "assets", "images","firma_tributaria.png")
            LOGO_MUN= os.path.join(BASE_DIR, "assets", "images","logo_olanchito.png")
            print(LOGO_MUN)
            
            if DIR_FIRMA:
                firma_admin = Image(DIR_FIRMA, width=2.60*cm, height=1.60*cm)
            else:
                firma_admin = None

            logo_mun = Image(LOGO_MUN, width=1.20*cm, height=1.20*cm)
        
        estilo_personal = estilos_parrafo()
        texto_parrafo = f""" Por este medio se le hace el {self.num_requerimiento} requerimiento de pago de los impuestos y servicios adeudados a esta municipalidad, a fin de que en el término de 30 días calendario, proceda a efectuar el pago del valor que se detalla a continuación"""
        texto_pie = f"""En caso de no atender este requerimiento en el plazo indicado, se procederá con el procedimiento administrativo correspondiente."""
        texto_nota = """ Intereses y recargos calculados hasta la fecha de este documento. Los valores indicados en este documento son referenciales y pueden variar al momento del pago."""
        texto_fecha = f"Emitido a los {datetime.now().day} días del mes de {datetime.now().strftime('%B')} del año {datetime.now().year}"
        
        for index, contribuyente in enumerate(self.lista_datos):
            qr_img = qrcode.make(contribuyente)
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            buffer.seek(0)
            qr_flowable = Image(buffer, width=1.20*cm, height=1.20*cm)
            muni_titulo = Paragraph( f"{self.municipio['NombreMuni']}", estilo_personal["TituloMuniMedia"],)
            titulo = Paragraph(f"<b>{self.titulo}</b><br/>", estilos["Title"]  )
            cc_original = Paragraph(f"Original: Contribuyente", estilos["Normal_grey_bold"])
            tabla_titulo = titulo_mudia_carta(titulo, muni_titulo, logo_mun, qr_flowable)
            original = crear_aviso_original(self, contribuyente, "ORIGINAL")
            tabla_duo = tabla_aviso_mora_media_carta(contribuyente["mora"])
            tabla_firma = tabla_frima_admin_fima_recibido("","Administracion Tributaria","",firma_admin)
            elementos.append(tabla_titulo)
            elementos.append(Spacer(1, 15))
            elementos.extend(original)
            elementos.append(Spacer(1, 8))
            elementos.append(Paragraph(texto_parrafo, estilos["Normal"]))
            elementos.append(Spacer(1, 4))
            elementos.append(tabla_duo)
            elementos.append(Spacer(1, 4))
            elementos.append(Paragraph(texto_pie, estilos["Normal"]))
            elementos.append(Paragraph(texto_nota, estilos["Normal"]))
            elementos.append(Paragraph(texto_fecha, estilos["Normal"]))
            elementos.append(Spacer(1, 25))
            elementos.append(tabla_firma)
            elementos.append(Spacer(1, 4))
            elementos.append(cc_original)
            if index < len(self.lista_datos) - 1:
                elementos.append(PageBreak())

        doc.build(elementos)
