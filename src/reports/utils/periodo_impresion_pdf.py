from datetime import datetime
from reportlab.platypus import Paragraph


def periodo_impresion_pdf(fecha_ini, fecha_fin, cantidad_filas: int, estilo) -> Paragraph:
    if (isinstance(fecha_ini, tuple) and (len(fecha_ini) > 0)):
        fecha_ini = fecha_ini[0]

    if fecha_fin is not None and fecha_ini is not None:
        fecha_inicio = datetime.strptime(fecha_ini, "%Y%m%d")
        fecha_inicio = fecha_inicio.strftime("%d/%m/%Y")

        fecha_final = datetime.strptime(fecha_fin, "%Y%m%d")
        fecha_final = fecha_final.strftime("%d/%m/%Y")
    else:
        fecha_inicio = f"No Definido"
        fecha_final = f"No Definido"
    if fecha_inicio == fecha_final:
        periodo_impresion = Paragraph(
            f"<b>{cantidad_filas}</b> Recibos Emitidos el dia {fecha_inicio}",
            estilo,
        )
    else:
        periodo_impresion = Paragraph(
            f"<b>{cantidad_filas}</b> Recibos Emitidos desde {fecha_inicio} hasta {fecha_final}:",
            estilo,
        )

    return periodo_impresion


def dia_impresion_pdf(estilo):
    return Paragraph(
        f"<b>Fecha de generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        estilo,
    )


def periodo_impresion_pdf_diario(fecha_ini, fecha_fin, cantidad_filas: int, estilo) -> Paragraph:
    if (isinstance(fecha_ini, tuple) and (len(fecha_ini) > 0)):
        fecha_ini = fecha_ini[0]

    if fecha_fin is not None and fecha_ini is not None:
        fecha_inicio = datetime.strptime(fecha_ini, "%Y%m%d")
        fecha_inicio = fecha_inicio.strftime("%d/%m/%Y")

        fecha_final = datetime.strptime(fecha_fin, "%Y%m%d")
        fecha_final = fecha_final.strftime("%d/%m/%Y")
    else:
        fecha_inicio = f"No Definido"
        fecha_final = f"No Definido"
    if fecha_inicio == fecha_final:
        periodo_impresion = Paragraph(
            f"Ingresos del dia {fecha_inicio}",
            estilo,
        )
    else:
        periodo_impresion = Paragraph(
            f"Ingresos desde {fecha_inicio} hasta {fecha_final}:",
            estilo,
        )

    return periodo_impresion
