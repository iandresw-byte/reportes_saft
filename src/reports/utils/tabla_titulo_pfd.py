from reportlab.platypus import Image
from reportlab.lib import colors
from reportlab.platypus import Table, Paragraph, TableStyle


def titulo_horizontal(titulo: Paragraph, logo_mun: Image | None, qr_image: Image | None) -> Table:
    qr = ""
    logo = ""
    if qr_image:
        qr = qr_image
    if logo_mun:
        logo = logo_mun
    valores_fila = [
        logo,
        titulo,
        qr
    ]
    tabla_titulo = Table(
        [valores_fila],
        colWidths=[100, 500, 100],  # ajusta según tus márgenes
    )

    tabla_titulo.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),  # type: ignore
    ]))

    return tabla_titulo


def titulo_vertical(titulo: Paragraph, logo_mun: Image | None, qr_image: Image | None) -> Table:
    qr = ""
    logo = ""
    if qr_image:
        qr = qr_image
    if logo_mun:
        logo = logo_mun
    valores_fila = [
        logo,
        titulo,
        qr
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
        ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),  # type: ignore
    ]))

    return tabla_titulo


def titulo_paragrap_pdf(municipio, titulo, estilo):
    return Paragraph(
        f"{municipio['NombreMuni'].strip()} - {municipio['NombreDepto'].strip()}<br/><b>{titulo}</b>",
        estilo,
    )



def titulo_mudia_carta(titulo: Paragraph, nombre_muni: Paragraph, logo_mun: Image | None, qr_image: Image | None) -> Table:
    qr = ""
    logo = ""
    if qr_image:
        qr = qr_image
    if logo_mun:
        logo = logo_mun
    valores_fila = [
        logo,
        nombre_muni,
        qr
    ]
    tabla_titulo = Table(
                    [
                        valores_fila,
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

    return tabla_titulo


