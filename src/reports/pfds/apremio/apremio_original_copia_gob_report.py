from pathlib import Path
import sys
import qrcode
import os
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    FrameBreak,
    Image,
    Paragraph,
    Spacer,
    PageBreak,
)
import time
from reportlab.lib import colors
from reportlab.platypus import HRFlowable
from reportlab.platypus import BaseDocTemplate
from reportlab.platypus import Frame
from reportlab.platypus import PageTemplate
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from datetime import datetime
from io import BytesIO
from src.reports.utils.firmas_pdf import firma_apremio_dos, firma_apremio_tres
from src.reports.pfds.apremio.crea_aviso import crear_aviso
from src.reports.tablas.tabla_aviso_cobro import tabla_aviso_mora_media_carta
from src.reports.utils.logo_mun_pdf import logo_muni_imagen_media_carta
from src.reports.utils.tabla_titulo_pfd import titulo_mudia_carta
from src.ui.components.ui_style_table import estilos_parrafo
from src.ui.components.ui_style_pdf import getSampleStyleSheet as estilos_mod

from src.utils.config_manager import Config
NUM_FIRMAS = Config.obtener("APREMIO", "NumFirmas")
FIRMAS_1 = Config.obtener("APREMIO", "firma_1")
FIRMAS_2 = Config.obtener("APREMIO", "firma_2")
CARGO_1 = Config.obtener("APREMIO", "cargo_1")
CARGO_2 = Config.obtener("APREMIO", "cargo_2")

class ApremioOriginalCopiaGobReport:
    def __init__(self, lista_datos, municipio,administracion, titulo_reporte, aviso = False):
        self.lista_datos = lista_datos
        self.municipio = municipio
        self.admin = administracion
        self.titulo = titulo_reporte
        self.num_requerimiento = "1er"
        self.margen = 0.4* cm
        self.es_aviso = aviso

    def dibujar_linea(self, canvas, doc):
        """
        Dibuja la línea divisoria exactamente
        en la mitad de la hoja carta.
        """
        ancho, alto = letter
        y = alto / 2
        canvas.saveState()
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(1)
        canvas.line(
            doc.leftMargin,
            y,
            ancho - doc.rightMargin,
            y,
        )
        canvas.restoreState()
    

    def generar_pdf(self, ruta_salida):
        doc = BaseDocTemplate(
            ruta_salida,
            pagesize=letter,
            leftMargin=self.margen,
            rightMargin=self.margen,
            topMargin=self.margen,
            bottomMargin=self.margen
        )
        ancho, alto = letter
        alto_util = alto - doc.topMargin - doc.bottomMargin
        alto_frame = (alto_util / 2) - 8

        frame_superior = Frame(
            x1=doc.leftMargin,
            y1=alto / 2 + 4,
            width=ancho - doc.leftMargin - doc.rightMargin,
            height=alto_frame,
            id="superior",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            showBoundary=0,
        )

        frame_inferior = Frame(
            x1=doc.leftMargin,
            y1=doc.bottomMargin,
            width=ancho - doc.leftMargin - doc.rightMargin,
            height=alto_frame,
            id="inferior",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            showBoundary=0,
        )


        template = PageTemplate(
            id="OriginalCopia",
            frames=[
                frame_superior,
                frame_inferior,
            ],
            onPage=self.dibujar_linea,
        )

        doc.addPageTemplates([template])
        elementos = []
        estilos = estilos_mod()
        ruta_base = r"C:\Program Files (x86)\SAFT\LogoMun"
        logo_mun = logo_muni_imagen_media_carta(ruta_base)

        if getattr(sys, 'frozen', False):
            BASE_DIR = Path(sys.executable).parent
        else:
            BASE_DIR = r"C:\Users\iAndresw\RepositorioLocal\reportes_saft"
        firma_admin_1 = ''
        firma_admin_2 = ''
        if self.municipio["CodMuni"] == "1807":
            DIR_FIRMA= os.path.join(BASE_DIR,  "assets", "images","firma_tributaria.png")
            DIR_FIRMA_2= os.path.join(BASE_DIR,  "assets", "images","firma_alcalde.png")
            LOGO_MUN= os.path.join(BASE_DIR, "assets", "images","logo_olanchito.png")
            print(LOGO_MUN)
            
            if DIR_FIRMA:
                firma_admin_1 = Image(DIR_FIRMA, width=3*cm, height=2*cm)
            else:
                firma_admin_1 = None
                
            if DIR_FIRMA_2:
                firma_admin_2 = Image(DIR_FIRMA_2, width=3*cm, height=2*cm)
            else:
                firma_admin_2 = None
            logo_mun = Image(LOGO_MUN, width=1.20*cm, height=1.20*cm)
            
        estilo_personal = estilos_parrafo()
        if not self.es_aviso:
            texto_parrafo = f"""Por este medio se le hace el {self.num_requerimiento} requerimiento de pago de los impuestos y servicios adeudados a esta municipalidad, a fin de que en el término de 30 días calendario, proceda a efectuar el pago del valor que se detalla a continuación"""
        else:
            texto_parrafo = f"""Por este medio se le hace el aviso de pago de los impuestos y servicios adeudados a esta municipalidad, a fin de que en el término de 30 días calendario, proceda a efectuar el pago del valor que se detalla a continuación"""
        #texto_pie = f"""En caso de no atender este requerimiento en el plazo indicado, se procederá con el procedimiento administrativo correspondiente."""
        texto_nota = """ Intereses y recargos calculados hasta la fecha de este documento. Los valores indicados en este documento son referenciales y pueden variar al momento del pago."""
        texto_fecha = f"Emitido a los {datetime.now().day} días del mes de {datetime.now().strftime('%B')} del año {datetime.now().year}"
        paragrap_texto_parrafo = Paragraph(texto_parrafo, estilos["Normal"])
        #paragrap_texto_pie = Paragraph(texto_pie, estilos["Normal"])
        paragrap_texto_nota = Paragraph(texto_nota, estilos["Normal"])
        paragrap_texto_fecha = Paragraph(texto_fecha, estilos["Normal"])


        cc_original = Paragraph(f"Original: Contribuyente", estilos["Normal_grey_bold"])
        cc_copia = Paragraph(f"Copia: Archivo", estilos["Normal_grey_bold"])

        muni_titulo = Paragraph( f"{self.municipio['NombreMuni']}", estilo_personal["TituloMuniMedia"],)
        titulo = Paragraph(f"<b>{self.titulo}</b><br/>", estilos["Title"]  )
        if NUM_FIRMAS == '1':
            tabla_firma = firma_apremio_tres(
                self.admin[FIRMAS_1],
                CARGO_1,
                self.admin[FIRMAS_2],
                CARGO_2,
                firma_admin_1,
                firma_admin_2
                )
        else:
            tabla_firma = firma_apremio_dos(self.admin[FIRMAS_1],CARGO_1,firma_admin_1)
        tabla_titulo = titulo_mudia_carta(titulo, muni_titulo, logo_mun, None)
        tiempo_aviso = 0
        tiempo_mora = 0
          
        for index, contribuyente in enumerate(self.lista_datos):
            # contribuyente_qr = { 
            #      "periodo":   contribuyente['periodo'],
            #      "nombre":   contribuyente['nombre'],
            #      "dni":   contribuyente['dni'],
            #      "direccion":   contribuyente['direccion'],
            #      "clave_catastro":   contribuyente['clave_catastro'],
            #      "num_documeto":   contribuyente['num_documeto']}
            # qr_img = qrcode.make(contribuyente_qr)
            # buffer = BytesIO()
            # qr_img.save(buffer, format="PNG")
            # buffer.seek(0)
            # qr_flowable = Image(buffer, width=1.20*cm, height=1.20*cm)
            inicio = time.perf_counter()
            encabezado = crear_aviso(self, contribuyente, "ORIGINAL")
            tiempo_aviso += time.perf_counter() - inicio
            inicio = time.perf_counter()
            tabla_duo = tabla_aviso_mora_media_carta(contribuyente["mora"])
            tiempo_mora += time.perf_counter() - inicio
            elementos.append(tabla_titulo)
            elementos.append(Spacer(1, 3))
            elementos.extend(encabezado)
            elementos.append(Spacer(1, 1))
            elementos.append(paragrap_texto_parrafo)
            elementos.append(Spacer(1, 1))
            elementos.append(tabla_duo)
            elementos.append(Spacer(1, 1))
            #elementos.append(paragrap_texto_pie)
            elementos.append(paragrap_texto_nota)
            elementos.append(paragrap_texto_fecha)
            elementos.append(Spacer(1, 16))
            elementos.append(tabla_firma)
            #elementos.append(cc_original)
            elementos.append(FrameBreak())
            elementos.append(tabla_titulo)
            elementos.append(Spacer(1, 3))
            elementos.extend(encabezado)
            elementos.append(Spacer(1, 1))
            elementos.append(paragrap_texto_parrafo)
            elementos.append(Spacer(1, 1))
            elementos.append(tabla_duo)
            elementos.append(Spacer(1, 2))
            #elementos.append(paragrap_texto_pie)
            elementos.append(paragrap_texto_nota)
            elementos.append(paragrap_texto_fecha)
            elementos.append(Spacer(1, 16))
            elementos.append(tabla_firma)
            #elementos.append(cc_copia)
            if index < len(self.lista_datos) - 1:
                elementos.append(PageBreak())
        print(f"Aviso:    {tiempo_aviso:.2f} segundos")
        print(f"Mora:     {tiempo_mora:.2f} segundos")
        doc.build(elementos)
