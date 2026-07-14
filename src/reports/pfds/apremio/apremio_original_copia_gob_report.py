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
from src.ui.components.ui_style_table import estilos_parrafo
from src.ui.components.ui_style_pdf import getSampleStyleSheet as estilos_mod


class ApremioOriginalCopiaGobReport:
    def __init__(self, lista_datos, municipio, titulo_reporte):
        self.lista_datos = lista_datos
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.num_requerimiento = "1er"
        self.margen = 0.4* cm

    def generar_pdf(self, ruta_salida):
        doc = SimpleDocTemplate(ruta_salida, pagesize=letter,
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
            BASE_DIR = Path(__file__).resolve().parent.parent.parent



        if os.path.exists(ruta_base + ".png"):
            ASSETS_DIR = ruta_base + ".png"
        elif os.path.exists(ruta_base + ".jpeg"):
            ASSETS_DIR = ruta_base + ".jpeg"
        elif os.path.exists(ruta_base + ".jpg"):
            ASSETS_DIR = ruta_base + ".jpg"
        else:
            ASSETS_DIR = None
        
        

        if ASSETS_DIR:
            logo_mun = Image(ASSETS_DIR, width=1.20*cm, height=1.20*cm)
        else:
            logo_mun = None
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
        texto_parrafo = f"""
                            Por este medio se le hace el {self.num_requerimiento} requerimiento de pago de los impuestos y servicios adeudados a esta municipalidad, a fin de que en el término de 30 días calendario, proceda a efectuar el pago del valor que se detalla a continuación
                            """
        texto_pie = f"""
                            En caso de no atender este requerimiento en el plazo indicado, se procederá con el procedimiento administrativo correspondiente.
                            """
        texto_nota = """ Intereses y recargos calculados hasta la fecha de este documento. Los valores indicados en este documento son referenciales y pueden variar al momento del pago."""
        texto_fecha = f"Emitido a los {datetime.now().day} días del mes de {datetime.now().strftime('%B')} del año {datetime.now().year}"
        for index, contribuyente in enumerate(self.lista_datos):

            qr_img = qrcode.make(contribuyente)
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            buffer.seek(0)

            # crea Flowable Image para ReportLab
            qr_flowable = Image(buffer, width=1.20*cm, height=1.20*cm)
            muni_titulo = Paragraph( f"{self.municipio['NombreMuni']}", estilo_personal["TituloMuniMedia"],)
            
            titulo = Paragraph(f"<b>{self.titulo}</b><br/>", estilos["Title"]  )


            tabla_titulo = Table(
                    [
                        [logo_mun, muni_titulo, qr_flowable],
                        ["", titulo, ""]
                    ],
                    colWidths=[100, 300, 100]
                )
            tabla_titulo.setStyle(TableStyle([
                ("SPAN", (0, 0), (0, 1)),
                ("SPAN", (2, 0), (2, 1)),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
               # ("LINEBELOW", (0, 1), (2, 1), 1, colors.black),
            ]))



            periodo_fila = Paragraph(f"<b>Periodo:</b> {contribuyente['periodo']}", estilos["Normal"],  )
            contribuyente_fila = Paragraph( f"<b>Contribuyente:</b> {contribuyente['nombre']}",  estilos["Normal"],)
            dni_fila = Paragraph( f"<b>DNI:</b> {contribuyente['dni']}", estilos["Normal"], )
            
            
            
            direccion_fila = Paragraph(
                f"<b>Dirección:</b> {contribuyente['direccion']}<br/>",
                estilos["Normal"],
            )
            clave_cata_fila = Paragraph(
                f"<b>Claves Catastrales:</b> {contribuyente['clave_catastro']}<br/>",
                estilos["Normal"],
            )
            num_requerimiento = Paragraph(
                f"<b>Aviso No.</b> {contribuyente['num_documeto']}<br/>",
                estilos["Normal"],
            )
     
            fila = [contribuyente_fila, dni_fila,periodo_fila,  num_requerimiento]

            tabla_datos_generales = Table(
                [fila],
                colWidths=[250, 90, 140,110],  # ajusta según tus márgenes
            )
            tabla_datos_generales.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "RIGHT"),
    
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                # Fondo gris para valores
                ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
            ]))
            fila = [direccion_fila,  clave_cata_fila]

            tabla_ubicacion = Table(
                [fila],
                colWidths=[290,300],  # ajusta según tus márgenes
            )
            tabla_ubicacion.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "RIGHT"),
       
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                # Fondo gris para valores
                ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
            ]))
            

            filas = [["Cuenta", "Descripción", "Monto (L)"]]
            total = 0

            for item in contribuyente["mora"]:
                monto = item["valor"] or 0
                filas.append(  [item["cta_ingreso"], item["nombre"], f"{monto:,.2f}"])
                total += monto

            filas.append(["", "TOTAL", f"{total:,.2f}"])

            tabla = Table(filas, colWidths=[90, 300, 100])
            tabla.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (2, 1), (2, -1), "RIGHT"),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))

            valores_firma = [
                Paragraph("", estilo_personal["firma_apremio"]),
                Paragraph("", estilo_personal["firma_apremio"]),
                Paragraph("Administración Tributaria", estilo_personal["firma_apremio"]),
                Paragraph("", estilo_personal["firma_apremio"]),
                Paragraph("", estilo_personal["firma_apremio"]),
            ]

            image_firma = [
                Paragraph("", estilo_personal["firma_apremio"]),
                Paragraph("", estilo_personal["firma_apremio"]),
                firma_admin,
                Paragraph("", estilo_personal["firma_apremio"]),
                Paragraph("", estilo_personal["firma_apremio"]),
            ]

            tabla_firma = Table(
                [image_firma,valores_firma],
                colWidths=[50, 50, 200, 50, 50],
            )

            tabla_firma.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LINEABOVE", (2, 1), (2, 1), 1, colors.black),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]))

      
            elementos.append(tabla_titulo)
            elementos.append(Spacer(1, 9))
            elementos.append(tabla_datos_generales)
            elementos.append(tabla_ubicacion)
            #elementos.append(periodo_fila)
            elementos.append(Spacer(1, 4))
            elementos.append(Paragraph(texto_parrafo, estilos["Normal"]))
            elementos.append(Spacer(1, 4))
            elementos.append(tabla)
            elementos.append(Spacer(1, 4))
            elementos.append(Paragraph(texto_pie, estilos["Normal"]))
            elementos.append(Paragraph(texto_nota, estilos["Normal"]))
            elementos.append(Paragraph(texto_fecha, estilos["Normal"]))
            elementos.append(tabla_firma)
            elementos.append(Spacer(1, 4))
            elementos.append(HRFlowable(
                width="100%",
                thickness=1,
                color=colors.black,
                spaceBefore=4,
                spaceAfter=4
            ))
            elementos.append(Spacer(1, 4))

            elementos.append(tabla_titulo)
            elementos.append(Spacer(1, 4))
            elementos.append(tabla_datos_generales)
            elementos.append(tabla_ubicacion)
            #elementos.append(periodo_fila)
            elementos.append(Spacer(1, 4))
            elementos.append(Paragraph(texto_parrafo, estilos["Normal"]))
            elementos.append(Spacer(1, 4))
            elementos.append(tabla)
            elementos.append(Spacer(1, 4))
            elementos.append(Paragraph(texto_pie, estilos["Normal"]))
            elementos.append(Paragraph(texto_nota, estilos["Normal"]))
            elementos.append(Paragraph(texto_fecha, estilos["Normal"]))
            elementos.append(tabla_firma)


            # 🚨 Salto de página entre contribuyentes
            if index < len(self.lista_datos) - 1:
                elementos.append(PageBreak())

        doc.build(elementos)
