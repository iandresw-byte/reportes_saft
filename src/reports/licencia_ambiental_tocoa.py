from datetime import date, datetime
import os
import locale
import json
from pathlib import Path
import sys
import qrcode
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.fonts import addMapping
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable, Image
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from src.reports.tablas.tabla_licencia import tabla_licencia_ambienntal
from src.reports.utils.cargar_imagenes import cargar_iconos_licencia
from src.models.tra_liceambiental import Tra_LiceAmbie
from src.reports.utils.firmas_pdf import tabla_frima_pdf_unica
from src.ui.components.ui_style_table import estilos_licencia_uma, table_fecha_lateral, table_per_ope, estilos_parrafo, table_per_ope_2


for loc in ["es_ES", "Spanish", "es-ES", "es_HN", "es_ES.UTF-8"]:
    try:
        locale.setlocale(locale.LC_TIME, loc)
        break
    except locale.Error:
        pass


def add_background(canvas, doc, image_path):
    # Dimensiones de media carta en puntos (pulgadas * 72)
    width, height = letter  # Página completa letter
    half_height = height / 2  # Media carta, horizontalmente en vertical
    canvas.drawImage(
        image_path,
        0, 0,  # origen en la parte superior
        width=width,
        height=height,
        preserveAspectRatio=True,
        mask='auto'
    )


# ==== Registrar fuentes Malgun desde carpeta local ====
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

# sube un nivel desde reports/
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

# Rutas de fuentes
font_SourceSansPro_regular = os.path.join(
    FONTS_DIR, "source-sans-pro.regular.ttf")
font_SourceSansPro_bold = os.path.join(FONTS_DIR, "source-sans-pro.bold.ttf")
font_regular = os.path.join(FONTS_DIR, "malgun.ttf")
font_bold = os.path.join(FONTS_DIR, "malgunbd.ttf")
font_GOTHICB = os.path.join(FONTS_DIR, "GOTHICB.TTF")
font_GOTHICB0 = os.path.join(FONTS_DIR, "GOTHICB0.TTF")
font_Jhenghei = os.path.join(FONTS_DIR, "Jhenghei.ttf")
font_Century_Gothic = os.path.join(FONTS_DIR, "Century-Gothic.ttf")

# Registrar fuentes si existen
if os.path.exists(font_regular) and os.path.exists(font_bold):
    pdfmetrics.registerFont(
        TTFont('SourceSansPro', font_SourceSansPro_regular))
    pdfmetrics.registerFont(
        TTFont('SourceSansPro-Bold', font_SourceSansPro_bold))
    pdfmetrics.registerFont(TTFont('Malgun', font_regular))
    pdfmetrics.registerFont(TTFont('Malgun-Bold', font_bold))
    pdfmetrics.registerFont(TTFont('GOTHICB0', font_GOTHICB0))
    pdfmetrics.registerFont(TTFont('GOTHICB', font_GOTHICB))
    pdfmetrics.registerFont(TTFont('Jhenghei', font_Jhenghei))
    pdfmetrics.registerFont(TTFont('Century-Gothic', font_Jhenghei))
    addMapping('Malgun', 0, 0, 'Malgun')
    addMapping('Malgun', 1, 0, 'Malgun-Bold')
    addMapping('GOTHICB0', 0, 0, 'GOTHICB0')
    addMapping('GOTHICB', 1, 0, 'GOTHICB')
    addMapping('Jhenghei', 0, 0, 'Jhenghei')
    addMapping('Century-Gothic', 1, 0, 'Century-Gothic')


class LicenciaAmbientalTocoaReport:
    def __init__(self, datos, municipio, titulo_reporte, firma_justicia=False, municipio_admin=None):
        self.datos = datos[0]
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.administracion = municipio_admin
        self.justicia_firma = firma_justicia

    def generar_pdf(self, ruta_salida="mora_bi_report.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=letter,
                                leftMargin=40,
                                rightMargin=40,
                                topMargin=20,
                                bottomMargin=20)
        elementos = []
        permiso_datos = json.dumps({
            "num_recibo": self.datos["num_recibo"],
            "propietario": self.datos["propietario"],
            "fecha_solicitud": str(self.datos["fecha_solicitud"]),
            "dni": self.datos["dni"],
            "establecimiento": self.datos["establecimiento"],
            "fecha_vence": str(self.datos["fecha_vence"])
        }, ensure_ascii=False)

        estilos = estilos_parrafo()
        estilos_uma = estilos_licencia_uma()

        municipalidad = Paragraph(
            f"{self.municipio['NombreMuni'].upper()}", estilos_uma["TituloMuni"],)
        departamento = Paragraph(
            f"DEPARTAMENTO DE {self.municipio['NombreDepto']}", estilos_uma["TituloDepto"],)
        telefono = Paragraph(
            f"TEL: {self.municipio['Telefono']}", estilos_uma["Telefono"],)
        titulo = Paragraph(f"TASA MUNICIPAL AMBIENTAL", estilos_uma["Titulo"],)

        iconos = cargar_iconos_licencia(BASE_DIR)
        tabla_data = tabla_licencia_ambienntal(self.datos, iconos)
        # tabla_data.setStyle(estilos_tabla2)
# TEXTOS
        depto = self.municipio['NombreDepto']
        ciudad = self.municipio['NombreMuni'].replace("Municipalidad de", "")
        texto1 = Paragraph(
            f"El suscrito Jefe de la Unidad Municipal Ambiental de este término municipal, por medio de la presente y en cumplimiento de la Ley General del Ambiente, HACE CONSTAR que la persona", estilos["parrafo"])
        texto2 = Paragraph(
            f"Se extiende la presente en la ciudad de {ciudad}, departamento de {depto}, debiendo colocarse en un lugar visible del establecimiento.", estilos["parrafo"])
        fecha_str = self.datos["fecha_solicitud"]

        formatos = ["%d-%m-%Y", "%Y-%m-%d"]

        fecha = None

        for formato in formatos:
            try:
                fecha = datetime.strptime(fecha_str, formato).date()
                break
            except ValueError:
                pass

        if fecha is None:
            raise ValueError(f"Formato de fecha no válido: {fecha_str}")

        ahora = fecha
        dia = ahora.day
        mes = ahora.strftime("%B")
        anio = ahora.year
        valores_fila = [
            Paragraph(f"Emitido a los", estilos["Label"],),
            Paragraph(f"{dia}", estilos_uma["Valor"],),
            Paragraph(f"dias del mes de", estilos["Label"],),
            Paragraph(f"{mes}", estilos_uma["Valor"],),
            Paragraph(f"del año", estilos["Label"],),
            Paragraph(f"{anio}", estilos_uma["Valor"],)
        ]
        tabla_fecha = Table(
            [valores_fila],
            colWidths=[90, 60, 110, 110, 60, 60],  # ajusta según tus márgenes
        )
        tabla_fecha.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            # Fondo gris para valores
            ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
        ]))
# TABLA QR
        num_permiso = Paragraph(
            f"TMA-{anio}-{self.datos["no_licencia"]}",  estilos_uma["NumPermiso"], )

        qr_img = qrcode.make(permiso_datos)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)

        # crea Flowable Image para ReportLab
        qr_flowable = Image(buffer, width=60, height=60)
        ruta_base = r"C:\Program Files (x86)\SAFT\LogoMun"

        if os.path.exists(ruta_base + ".png"):
            ASSETS_DIR = ruta_base + ".png"
        elif os.path.exists(ruta_base + ".jpeg"):
            ASSETS_DIR = ruta_base + ".jpeg"
        elif os.path.exists(ruta_base + ".jpg"):
            ASSETS_DIR = ruta_base + ".jpg"
        else:
            ASSETS_DIR = None

        logo_unidad = os.path.join(
            BASE_DIR, "assets", "images", "logo_uma.PNG")

        if ASSETS_DIR:
            logo_mun = Image(ASSETS_DIR, width=3*cm, height=2.52*cm)
        else:
            logo_mun = None

        logo_uma = Image(logo_unidad, width=2.84*cm, height=2.52*cm)

# TABLA FIRMA
        tabla_firma = tabla_frima_pdf_unica(
            self.administracion["Ambiental"], "Jefe Unidad Municipal Ambiental", None, qr_izq=qr_flowable)
        # TABLA ENCABEZADO
        valores_fila = [
            logo_mun,
            municipalidad,
            logo_uma
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
        elementos.append(departamento)
        elementos.append(telefono)
        elementos.append(titulo)
        linea = HRFlowable(width="80%", thickness=1,
                           color=colors.black, spaceBefore=10, spaceAfter=10)
        elementos.append(linea)
        elementos.append(Spacer(1, 5))
        elementos.append(texto1)
        elementos.append(tabla_data)
        elementos.append(Spacer(1, 5))
        elementos.append(texto2)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_fecha)
        elementos.append(Spacer(1, 30))
        elementos.append(tabla_firma)
        elementos.append(Spacer(1, 5))
        elementos.append(num_permiso)
        footer = Paragraph(
            f"<b>LA TIERRA ES EL HOGAR DE TODOS... CUIDEMOSLA</b>",  estilos["Label"], )
        elementos.append(footer)
        background_image = os.path.join(
            BASE_DIR, "assets", "images", "logo_tocoa.PNG")
        doc.build(elementos,
                  onFirstPage=lambda canvas, doc: add_background(
                      canvas, doc, background_image),
                  onLaterPages=lambda canvas, doc: add_background(
                      canvas, doc, background_image),
                  )
