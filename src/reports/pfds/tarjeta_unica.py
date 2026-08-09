
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, LEGAL, legal
import pandas as pd
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from src.reports.tablas.abonados_por_servicio import tabla_abonados_servicio
from src.reports.utils.firmas_pdf import tabla_frima_pdf_unica
from src.reports.utils.footer_pdf import otras_paginas, primera_pagina
from src.reports.utils.periodo_impresion_pdf import periodo_impresion_pdf, dia_impresion_pdf, sub_titulo
from src.reports.utils.logo_mun_pdf import logo_muni_imagen
from src.reports.utils.tabla_titulo_pfd import titulo_horizontal, titulo_paragrap_pdf


class TarjetaUnicaReport:
    def __init__(self, datos,  municipio, municipio_admin, titulo_reporte):
        self.datos = datos
        self.contribuyente = []
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.administracion = municipio_admin

    def dataframe_to_table_data(self, df: pd.DataFrame, include_index: bool = True) -> list:
        """Convierte un pivot de pandas en la lista de listas que espera Table()."""
        header = ([df.index.name or ""] if include_index else []) + [str(c) for c in df.columns]
        rows = [header]
        for idx, row in df.iterrows():
            line = ([str(idx)] if include_index else []) + [
                "" if pd.isna(v) else str(v) for v in row
            ]
            rows.append(line)
        return rows

    


    def generar_pdf(self, ruta_salida="rpt_ingresos_depto_detatllado.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(legal), leftMargin=40,
                                rightMargin=40,
                                topMargin=20,
                                bottomMargin=20)
        elementos = []
        estilos = getSampleStyleSheet()
        styles = getSampleStyleSheet()
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
        datos_fila = [
            Paragraph( f"{self.datos['nombre']} {self.datos['direccion']} - Identidad: {self.datos['dni']}",
                styles["Normal"],
            )
        ]
        #elementos.append([datos_fila])
        datos_aval_bi = self.datos["declaraciones_bi"]
        datos_aval_ics = self.datos["declaraciones_ics"]
        table_data = self.dataframe_to_table_data(datos_aval_bi)
        table_data_ics_declara = self.dataframe_to_table_data(datos_aval_ics)
        estilo_tabla = TableStyle(
                        [
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("FONTSIZE", (0, 0), (-1, -1), 7),
                            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#ecf0f1")),  # fila TOTAL
                        ]
                    )
        t = Table(table_data, repeatRows=1)
        t_1 = Table(table_data_ics_declara, repeatRows=1)
        t.setStyle(estilo_tabla)
        t_1.setStyle(estilo_tabla)
        titulo_sub_bi = sub_titulo(estilos,"AVALUOS DE BIENES INMUEBLES")
        elementos.append(titulo_sub_bi)
        elementos.append(t)
        elementos.append(Spacer(1, 5))
        titulo_sub_ics = sub_titulo(estilos,"DECLRACIONES DE BIENES INMUEBLES")
        elementos.append(titulo_sub_ics)
        elementos.append(t_1)
      
 
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
