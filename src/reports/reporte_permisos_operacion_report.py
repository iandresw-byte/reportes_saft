from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from src.ui.components.ui_style_table import fila_style, table_style, columa_style


class RptPermisoOperacionReport:
    def __init__(self, datos, municipio, titulo_reporte, nombre_aldea=None, nombre_barrio=None, fecha_ini=None, fecha_fin=None, tipo_po=None):
        self.datos = datos
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.nombre_aldea = nombre_aldea,
        self.nombre_barrio = nombre_barrio,
        self.fecha_ini = fecha_ini,
        self.fecha_fin = fecha_fin
        self.tipo_po = tipo_po

    def generar_pdf(self, ruta_salida="rpt_permiso_operacion.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(letter), leftMargin=40,
                                rightMargin=40,
                                topMargin=20,
                                bottomMargin=20)
        elementos = []
        estilos = getSampleStyleSheet()

        titulo = Paragraph(
            f"<b>REPORTE DE {self.titulo} </b><br/>{self.municipio['NombreMuni']} - {self.municipio['NombreDepto']}",
            estilos["Title"],
        )
        fecha = Paragraph(
            f"<b>Fecha de generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            estilos["Normal"],
        )
        aldea = Paragraph(
            f"<b>Aldea:</b> {self.nombre_aldea[0]}",
            estilos["Normal"],
        )
        barrio = Paragraph(
            f"<b>Barrio/Colonia/Caserio:</b> {self.nombre_barrio[0]}",
            estilos["Normal"],
        )

        if (isinstance(self.fecha_ini, tuple) and (len(self.fecha_ini) > 0)):
            self.fecha_ini = self.fecha_ini[0]

        if self.fecha_fin is not None and self.fecha_ini is not None:
            fecha_inicio = datetime.strptime(self.fecha_ini, "%Y%m%d")
            fecha_inicio = fecha_inicio.strftime("%d/%m/%Y")

            fecha_final = datetime.strptime(self.fecha_fin, "%Y%m%d")
            fecha_final = fecha_final.strftime("%d/%m/%Y")
        else:
            fecha_inicio = f"No Definido"
            fecha_final = f"No Definido"

        periodo_impresion = Paragraph(
            f"<b>{len(self.datos)}</b> Permisos emitidos desde {fecha_inicio} hasta {fecha_final}:",
            estilos["Normal"],
        )
        if self.tipo_po == "%":
            self.tipo_po = "Apertura-Renovacion"
        tipo_po_fila = Paragraph(
            f"<b>Tipo Solicitud</b> {self.tipo_po}",
            estilos["Normal"],
        )

        elementos.append(titulo)
        elementos.append(Spacer(1, 12))
        elementos.append(fecha)
        elementos.append(Spacer(1, 5))
        elementos.append(aldea)
        elementos.append(Spacer(1, 5))
        elementos.append(barrio)
        elementos.append(Spacer(1, 5))
        elementos.append(periodo_impresion)
        elementos.append(Spacer(1, 5))
        elementos.append(tipo_po_fila)
        elementos.append(Spacer(1, 24))
        estilo_encabezado = columa_style()
        estilo_fila = fila_style()
        estilo_tabla = table_style()
        encabezados = [
            Paragraph("Identidad", estilo_encabezado),
            Paragraph("Nombre Establecimeinto", estilo_encabezado),
            Paragraph("Fecha", estilo_encabezado),
            Paragraph("Actividad Economica", estilo_encabezado),
            Paragraph("Tipo", estilo_encabezado),
            Paragraph("No. Permiso", estilo_encabezado),
            Paragraph("No. Recibo", estilo_encabezado),
            Paragraph("Valor Pagado", estilo_encabezado),
            Paragraph("Periodo", estilo_encabezado),
        ]
        filas = [encabezados]
        total = 0
        for item in self.datos:
            dni = (item["Identidad"]) if item["Identidad"] else ''
            nombre_establecimeinto = (
                item["Negocio"]) if item["Negocio"] else ''
            propetario = (item["Propietario"]
                          ) if item["Propietario"] else ''
            fecha = (item["Fecha"]) if item["Fecha"] else ''
            actividad = (item["Actividad"]) if item["Actividad"] else ''
            tipo = (item["Observacion"]) if item["Observacion"] else ''
            no_permiso = (item["NoPermiso"]) if item["NoPermiso"] else 0
            valor_pagado = (item["ValorUnitReciboDet"]
                            ) if item["ValorUnitReciboDet"] else 0
            num_recibo = (item["NumRecibo"]
                          ) if item["NumRecibo"] else 0
            aldea = (item["NombreAldea"]) if item["NombreAldea"] else ''
            barrio = (item["NombreBarrio"]) if item["NombreBarrio"] else ''
            periodo = (item["Periodo"]) if item["Periodo"] else ''
            total += valor_pagado
            filas.append([
                Paragraph(dni, estilo_fila),
                Paragraph(nombre_establecimeinto, estilo_fila),
                Paragraph(fecha, estilo_fila),
                Paragraph(actividad, estilo_fila),
                Paragraph(tipo, estilo_fila),
                Paragraph(f"{no_permiso}", estilo_fila),
                Paragraph(f"{num_recibo}", estilo_fila),
                Paragraph(f"{valor_pagado:,.2f}", estilo_fila),
                Paragraph(f"{periodo}", estilo_fila)
            ])
        filas.append([Paragraph("", estilo_fila),
                      Paragraph("", estilo_fila),
                      Paragraph("", estilo_fila),
                      Paragraph("", estilo_fila),
                      Paragraph("", estilo_fila),
                      Paragraph("TOTAL", estilo_fila),
                      Paragraph("", estilo_fila),
                      Paragraph(f"{total:,.2f}", estilo_fila),
                      Paragraph("", estilo_fila)])
        tabla = Table(filas, colWidths=[
                      75, 175, 55, 175, 65, 45, 50, 50, 45])
        tabla.setStyle(estilo_tabla)
        elementos.append(tabla)
        elementos.append(Spacer(1, 20))

        footer = Paragraph(
            "<b>Generado por el sistema SAFT</b>",
            estilos["Normal"],
        )
        elementos.append(footer)

        doc.build(elementos)
