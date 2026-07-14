
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from src.reports.tablas.abonados_por_servicio import tabla_abonados_servicio
from src.reports.utils.firmas_pdf import tabla_frima_pdf_unica
from src.reports.utils.footer_pdf import otras_paginas, primera_pagina
from src.reports.utils.periodo_impresion_pdf import periodo_impresion_pdf, dia_impresion_pdf
from src.reports.utils.logo_mun_pdf import logo_muni_imagen
from src.reports.utils.tabla_titulo_pfd import titulo_vertical, titulo_paragrap_pdf


class PlanDePagoReport:
    def __init__(self, municipio, municipio_admin, titulo_reporte, df_cuotas, df_facturas, df_plan, df_suma, df_esta, resultado):
    
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.administracion = municipio_admin
        self.df_cuotas = df_cuotas
        self.df_facturas = df_facturas
        self.df_plan = df_plan
        self.df_suma = df_suma
        self.df_esta = df_esta
        self.result = resultado


    def generar_pdf(self, ruta_salida="plan_pago_anulado.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=letter, leftMargin=40,
                                rightMargin=40,
                                topMargin=20,
                                bottomMargin=20)
        elementos = []
        estilos = getSampleStyleSheet()
        ruta_base = r"C:\Program Files (x86)\SAFT\LogoMun"
        logo_mun = logo_muni_imagen(ruta_base)
        titulo = titulo_paragrap_pdf(
            self.municipio, self.titulo, estilos["Title"])

        tabla_titulo = titulo_vertical(titulo, logo_mun, None)
        fecha = dia_impresion_pdf(estilos["Normal"])
        elementos.append(tabla_titulo)
        elementos.append(Spacer(1, 12))
        elementos.append(fecha)

        elementos.append(Spacer(1, 5))
        elementos.append(Spacer(1, 24))
        print(self.df_plan)
        # CATASTRO
        valores_fila = [
            Paragraph(f'Nombre: {self.df_plan.loc[0, "Nombre_Completo"]}'),
            Paragraph(f'No. Plan de Pago: {self.df_plan.loc[0, "SeqPP"]}'),
            ]
        
        valores_fila_1 = [
            Paragraph(f'DNI: {self.df_plan.loc[0, "Identidad"]}'),
            Paragraph(f'{self.df_plan.loc[0, "SeqPP"]}'),
            ]
        
        valores_fila_2 = [
            Paragraph(f'Fecha: {self.df_plan.loc[0, "FechaInicioPP"]}'),
            Paragraph(f'Estado: {self.df_plan.loc[0, "EstadoPP"]}'),
            ]
        
        valores_fila_3 = [
            Paragraph(f'Total del Plan: {self.df_plan.loc[0, "MontoPP"]}'),
            Paragraph(f'Total Pagado: {self.df_plan.loc[0, "TotalPagadoPP"]}'),
            ]
        
        valores_fila_4 = [
            Paragraph(f'✔ Cuotas pagadas: {self.df_plan.loc[0, "MontoPP"]}'),
            Paragraph(f'✖ Cuotas anuladas: {self.df_plan.loc[0, "TotalPagadoPP"]}'),
            ]
        
        valores_fila_5 = [
            Paragraph(f'✔ Mantienen: {self.result["cant_fnp_cubre"]}'),
            Paragraph(f'↺ Reactivar: {self.result["cant_fnp_no_cubre"]}'),
            ]
        valores_fila_6 = [
            Paragraph(f'➖ Factura Modificada: {self.result["num_avpg_res"]}'),
            Paragraph(f'➖ Factura Modificada: {self.result["num_avpg_res"]}'),
            ]
        
        valores_fila_7 = [
            Paragraph(f'Total anulado: {self.result["total_pp_vencido"]}'),
            Paragraph(f'Total pagado: {self.result["total_pp_pagado"]}'),
            ]

        tabla = Table(
                [valores_fila, 
                 valores_fila_1,
                 valores_fila_2,
                 valores_fila_3,
                 valores_fila_4,
                 valores_fila_5,
                 valores_fila_6,
                 valores_fila_7,
                 ],
                colWidths=[300,  200],  # ajusta según tus márgenes
            )
        
        elementos.append(tabla)
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
