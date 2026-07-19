from pathlib import Path
import sys

import qrcode
import os
from reportlab.platypus import SimpleDocTemplate, Table, Image, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from datetime import datetime
from io import BytesIO
from src.reports.utils.firmas_pdf import tabla_frima_admin_fima_recibido
from src.reports.pfds.apremio.crea_aviso import  crear_aviso_carta
from src.reports.utils.periodo_impresion_pdf import periodo_impresion_pdf
from src.reports.utils.logo_mun_pdf import logo_muni_imagen, logo_muni_imagen_media_carta
from src.reports.utils.tabla_titulo_pfd import titulo_horizontal, titulo_paragrap_pdf
from src.ui.components.ui_style_table import estilos_parrafo



class ApremioCartaGobReport:
    def __init__(self, lista_datos, municipio, titulo_reporte):
        self.lista_datos = lista_datos
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.num_requerimiento = "1er"
        self.margen = 1 * cm

    def generar_pdf(self, ruta_salida):
        doc = SimpleDocTemplate(ruta_salida, pagesize=letter,
                                leftMargin=self.margen,
                                rightMargin=self.margen,
                                topMargin=self.margen,
                                bottomMargin=self.margen)
        elementos = []
        estilos = getSampleStyleSheet()
        ruta_base = r"C:\Program Files (x86)\SAFT\LogoMun"
        if getattr(sys, 'frozen', False):
            BASE_DIR = Path(sys.executable).parent
        else:
            BASE_DIR = r"C:\Users\iAndresw\RepositorioLocal\reportes_saft"
        
        logo_mun = logo_muni_imagen(ruta_base)
        firma_admin = ''
        if self.municipio["CodMuni"] == "1807":
            DIR_FIRMA= os.path.join(BASE_DIR,  "assets", "images","firma_tributaria.png")
            LOGO_MUN= os.path.join(BASE_DIR, "assets", "images","logo_olanchito.png")
            print(LOGO_MUN)
            
            if DIR_FIRMA:
                firma_admin = Image(DIR_FIRMA, width=3*cm, height=2*cm)
            else:
                firma_admin = None
        titulo = titulo_paragrap_pdf(
            self.municipio, self.titulo, estilos["Title"])
        
        tabla_titulo = titulo_horizontal(titulo, logo_mun, None)

        estilo_personal = estilos_parrafo()
        texto_parrafo = f"""Por este medio se le hace el {self.num_requerimiento} requerimiento de pago de los impuestos y servicios adeudados a esta municipalidad, a fin de que en el término de 30 días calendario, proceda a efectuar el pago del valor que se detalla a continuación"""
        texto_pie = f"""En caso de no atender este requerimiento en el plazo indicado, se procederá con el procedimiento administrativo correspondiente."""
        texto_nota = """ Intereses y recargos calculados hasta la fecha de este documento. Los valores indicados en este documento son referenciales y pueden variar al momento del pago."""
        texto_fecha = f"Emitido a los {datetime.now().day} días del mes de {datetime.now().strftime('%B')} del año {datetime.now().year}"
        for index, contribuyente in enumerate(self.lista_datos):
            qr_img = qrcode.make(contribuyente)
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            buffer.seek(0)

            # crea Flowable Image para ReportLab
            qr_flowable = Image(buffer, width=60, height=60)
            muni_titulo = Paragraph(f"{self.municipio['NombreMuni']}", estilo_personal["TituloMuni"],)
            elementos.append(muni_titulo)
            titulo = Paragraph(f"<b>{self.titulo}</b><br/>", estilos["Title"])

            valores_fila = [
                logo_mun,
                titulo,
                qr_flowable
            ]
            tabla_titulo = Table(
                [valores_fila],
                colWidths=[100, 300, 100],  # ajusta según tus márgenes
            )
            tabla_titulo.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                # Fondo gris para valores
                ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
            ]))
            elementos.append(tabla_titulo)
            original = crear_aviso_carta(self, contribuyente, "ORIGINAL")
            elementos.extend(original)
            elementos.append(Spacer(1, 5))
            elementos.append(Paragraph(texto_parrafo, estilos["Normal"]))
            elementos.append(Spacer(1, 5))

            filas = [["Cuenta", "Descripción", "Monto (L)"]]
            total = 0

            for item in contribuyente["mora"]:
                monto = item["valor"] or 0
                filas.append(
                    [item["cta_ingreso"], item["nombre"], f"{monto:,.2f}"])
                total += monto

            filas.append(["", "TOTAL", f"{total:,.2f}"])

            tabla = Table(filas, colWidths=[90, 300, 100])
            tabla.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (2, 1), (2, -1), "RIGHT"),
            ]))

            tabla_firma = tabla_frima_admin_fima_recibido("","Administracion Tributaria","",firma_admin)
            
            elementos.append(tabla)

            elementos.append(Spacer(1, 8))
            elementos.append(Paragraph(texto_pie, estilos["Normal"]))
            elementos.append(Spacer(1, 8))
            elementos.append(Paragraph(texto_nota, estilos["Normal"]))
            elementos.append(Spacer(1, 8))
            elementos.append(Paragraph(texto_fecha, estilos["Normal"]))
            elementos.append(Spacer(1, 25))
            elementos.append(tabla_firma)
            elementos.append(Spacer(1, 5))

            # 🚨 Salto de página entre contribuyentes
            if index < len(self.lista_datos) - 1:
                elementos.append(PageBreak())

        doc.build(elementos)
