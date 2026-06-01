
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from src.reports.tablas.ingresos_detallados_justicia_municipal import tabla_ingreso_diario_justicia
from src.reports.tablas.ingresos_detallados_procamut import tabla_ingreso_diario_procamut
from src.reports.tablas.ingresosd_detallados_desarrollo_urbano import tabla_ingreso_diario_desarrollo_urbano
from src.reports.tablas.ingresos_detallados_admin_triburaria_os import tabla_ingreso_diario_admin_tributaria_os
from src.reports.tablas.ingresos_detallados_admin_triburaria_ip import tabla_ingreso_diario_admin_tributaria_ip
from src.reports.tablas.ingresos_detallados_admin_triburaria_bi import tabla_ingreso_diario_admin_tributaria_bi
from src.reports.tablas.ingresos_detallados_admin_tributaria_ics import tabla_ingreso_diario_admin_tributaria_ics
from src.reports.tablas.ingresos_detallados_catastro import tabla_ingreso_diario_catastro
from src.reports.tablas.ingresos_detallados_secretaria import tabla_ingreso_diario_scretaria
from src.reports.utils.firmas_pdf import tabla_frima_pdf_unica
from src.reports.utils.footer_pdf import otras_paginas, primera_pagina
from src.reports.utils.periodo_impresion_pdf import dia_impresion_pdf, periodo_impresion_pdf_diario
from src.reports.utils.logo_mun_pdf import logo_muni_imagen
from src.reports.utils.tabla_ingresos_uma import tabla_ingreso_diario_uma
from src.reports.utils.tabla_titulo_pfd import titulo_horizontal, titulo_paragrap_pdf


class RptIngresosDeptoDiarioReport:
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

    def generar_pdf(self, ruta_salida="rpt_ingresos_depto_detatllado.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(letter), leftMargin=40,
                                rightMargin=40,
                                topMargin=20,
                                bottomMargin=20)
        elementos = []
        estilos = getSampleStyleSheet()
        ruta_base = r"C:\Program Files (x86)\SAFT\LogoMun"
        logo_mun = logo_muni_imagen(ruta_base)

        titulo = titulo_paragrap_pdf(
            self.municipio, self.titulo, estilos["Title"])
        periodo_impresion = periodo_impresion_pdf_diario(
            self.fecha_ini, self.fecha_fin, len(self.datos), estilos["Normal"])
        tabla_titulo = titulo_horizontal(titulo, logo_mun, None)
        fecha = dia_impresion_pdf(estilos["Normal"])
        elementos.append(tabla_titulo)
        elementos.append(Spacer(1, 12))
        elementos.append(fecha)
        elementos.append(Spacer(1, 5))
        elementos.append(periodo_impresion)
        elementos.append(Spacer(1, 5))
        elementos.append(Spacer(1, 24))
        # CATASTRO
        if self.depto == "1":
            tabla = tabla_ingreso_diario_catastro(self.datos)
            elementos.append(tabla)
            tabla_firma = tabla_frima_pdf_unica(
                self.administracion["Catastro"], "Jefe del Departamento de Catastro", None)
        # ADMINISTRACION TRIBUTARIA
        elif self.depto == "2":
            if self.tipo_factura == "0":
                tabla = tabla_ingreso_diario_admin_tributaria_os(self.datos)
                elementos.append(tabla)
                tabla_firma = tabla_frima_pdf_unica(
                    self.administracion["Tributaria"], "Jefe del Departamento de Administracion Tributaria", None)
            elif self.tipo_factura == "1":
                tabla = tabla_ingreso_diario_admin_tributaria_bi(self.datos)
                elementos.append(tabla)
                tabla_firma = tabla_frima_pdf_unica(
                    self.administracion["Tributaria"], "Jefe del Departamento de Administracion Tributaria", None)
            elif self.tipo_factura == "2,3":
                tabla = tabla_ingreso_diario_admin_tributaria_ics(
                    self.datos)
                elementos.append(tabla)
                tabla_firma = tabla_frima_pdf_unica(
                    self.administracion["Tributaria"], "Jefe del Departamento de Administracion Tributaria", None)
            elif self.tipo_factura == "4":
                tabla = tabla_ingreso_diario_admin_tributaria_ip(
                    self.datos)
                elementos.append(tabla)
                tabla_firma = tabla_frima_pdf_unica(
                    self.administracion["Tributaria"], "Jefe del Departamento de Administracion Tributaria", None)
            else:
                return
        # UNIDAD AMBIENTAL
        elif self.depto == "3":
            tabla = tabla_ingreso_diario_uma(self.datos)
            elementos.append(tabla)
            tabla_firma = tabla_frima_pdf_unica(
                self.administracion["Ambiental"], "Jefe de la Unidad Ambiental Municipal", None)
        # DIRECCION DE JUSTICIA MUNICIPAL
        elif self.depto == "4":
            tabla = tabla_ingreso_diario_justicia(self.datos)
            elementos.append(tabla)
            tabla_firma = tabla_frima_pdf_unica(
                self.administracion["Justicia"], "Jefe de la Unidad de Direcion de Justicias Municipal", None)
        # SECRETARIA
        elif self.depto == "6":
            tabla = tabla_ingreso_diario_scretaria(self.datos)
            elementos.append(tabla)
            tabla_firma = tabla_frima_pdf_unica(
                self.administracion["Secretaria"], "Jefe del Departamento de Secretaria Municipal", None)
        # PROCAMUT
        elif self.depto == "7":
            tabla = tabla_ingreso_diario_procamut(self.datos)
            elementos.append(tabla)
            tabla_firma = tabla_frima_pdf_unica(
                self.administracion["Justicia"], "Jefe de la Unidad de Direcion de Justicias Municipal", None)
        # DESARROLLO URBANO
        elif self.depto == "8":
            tabla = tabla_ingreso_diario_desarrollo_urbano(self.datos)
            elementos.append(tabla)
            tabla_firma = tabla_frima_pdf_unica(
                self.administracion["DesarrolloUrbano"], "Jefe Unidad de Desarrollo Urbano", None)

        else:
            return None
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
