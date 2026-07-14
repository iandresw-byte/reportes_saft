import qrcode
import os
from reportlab.platypus import SimpleDocTemplate, Table, Image, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from datetime import datetime
from io import BytesIO
from src.ui.components.ui_style_table import estilos_parrafo


class ApremioCartaSAMIReport:
    def __init__(self, lista_datos, municipio, titulo_reporte):
        self.lista_datos = lista_datos
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.num_requerimiento = "1er"
        self.margen = 0.70* cm

    def generar_pdf(self, ruta_salida):
        doc = SimpleDocTemplate(ruta_salida, pagesize=letter,
                                leftMargin=self.margen,
                                rightMargin=self.margen,
                                topMargin=self.margen,
                                bottomMargin=self.margen)
        elementos = []
        estilos = getSampleStyleSheet()
        ruta_base = r"C:\Program Files (x86)\SAFT\LogoMun"

        if os.path.exists(ruta_base + ".png"):
            ASSETS_DIR = ruta_base + ".png"
        elif os.path.exists(ruta_base + ".jpeg"):
            ASSETS_DIR = ruta_base + ".jpeg"
        elif os.path.exists(ruta_base + ".jpg"):
            ASSETS_DIR = ruta_base + ".jpg"
        else:
            ASSETS_DIR = None

        if ASSETS_DIR:
            logo_mun = Image(ASSETS_DIR, width=2.84*cm, height=2.52*cm)
        else:
            logo_mun = None

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
            qr_flowable = Image(buffer, width=60, height=60)
            muni_titulo = Paragraph(
                f"{self.municipio['NombreMuni']}", estilo_personal["TituloMuni"],)
            elementos.append(muni_titulo)
            titulo = Paragraph(
                f"<b>{self.titulo}</b><br/>",
                estilos["Title"]
            )

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

            periodo_fila = Paragraph( f"<b>Periodo:</b> {contribuyente['periodo']}", estilos["Normal"], )
            contribuyente_fila = Paragraph( f"<b>Contribuyente:</b> {contribuyente['nombre']}<br/>", estilos["Normal"],)
            dni_fila = Paragraph( f"<b>DNI:</b> {contribuyente['dni']}<br/>", estilos["Normal"], )
            direccion_fila = Paragraph( f"<b>Dirección:</b> {contribuyente['direccion']}<br/>", estilos["Normal"],)
            clave_cata_fila = Paragraph( f"<b>Claves Catastrales:</b> {contribuyente['clave_catastro']}<br/>",  estilos["Normal"], )
            num_requerimiento = Paragraph( f"<b>Requerimiento No.</b> {contribuyente['num_documeto']}<br/>",estilos["Normal"], )
            fila = [periodo_fila, num_requerimiento]
            tabla_periodo_num = Table(
                [fila],
                colWidths=[300, 270],  # ajusta según tus márgenes
            )
            fila = [contribuyente_fila, dni_fila]
            tabla_nombre_dni = Table(
                [fila],
                colWidths=[300, 270],  # ajusta según tus márgenes
            )
            fila = [ clave_cata_fila]
            tabla_cata = Table(
                [fila],
                colWidths=[570],  # ajusta según tus márgenes
            )
            fila = [direccion_fila ]
            tabla_ubicacion = Table(
                [fila],
                colWidths=[570],  # ajusta según tus márgenes
            )

            elementos.append(tabla_nombre_dni)
            elementos.append(tabla_periodo_num)
            elementos.append(tabla_ubicacion)
            elementos.append(tabla_cata)
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

            valores_firma = [
                Paragraph("", estilo_personal["firma_apremio"]),
                Paragraph("Administración Tributaria", estilo_personal["firma_apremio"]),
                Paragraph("", estilo_personal["firma_apremio"]),
                Paragraph("Firma Recibido Contribuyente", estilo_personal["firma_apremio"]),
                Paragraph("", estilo_personal["firma_apremio"]),
            ]

            tabla_firma = Table(
                [valores_firma],
                colWidths=[50, 200, 50, 200, 50],
            )

            tabla_firma.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LINEABOVE", (1, 0), (1, 0), 1, colors.black),
                ("LINEABOVE", (3, 0), (3, 0), 1, colors.black),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]))
            elementos.append(tabla)

            elementos.append(Spacer(1, 5))
            elementos.append(Paragraph(texto_pie, estilos["Normal"]))
            elementos.append(Spacer(1, 5))
            elementos.append(Paragraph(texto_nota, estilos["Normal"]))
            elementos.append(Spacer(1, 5))
            elementos.append(Paragraph(texto_fecha, estilos["Normal"]))
            elementos.append(Spacer(1, 30))
            elementos.append(tabla_firma)

            # 🚨 Salto de página entre contribuyentes
            if index < len(self.lista_datos) - 1:
                elementos.append(PageBreak())

        doc.build(elementos)
