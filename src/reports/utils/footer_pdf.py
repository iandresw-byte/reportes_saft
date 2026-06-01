from datetime import datetime


def footer(canvas, doc):
    canvas.saveState()

    canvas.setFont("Helvetica", 8)
    canvas.drawString(
        40, 20, f"Generado por SAFT {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    pagina = canvas.getPageNumber()
    canvas.drawRightString(doc.pagesize[0] - 40, 20, f"Página {pagina}")

    canvas.restoreState()


def otras_paginas(canvas, doc, municipio, titulo: str):
    canvas.saveState()
    if "- UMA" in titulo:
        titulo = titulo.replace("- UMA", "").capitalize()
        titulo = titulo+" - UMA"
    # ENCABEZADO
    canvas.setFont("Helvetica", 8)
    canvas.drawString(40, doc.pagesize[1] - 20,
                      titulo)
    canvas.drawRightString(
        doc.pagesize[0] - 40,
        doc.pagesize[1] - 20,
        f"{municipio['NombreMuni'].strip()} - {municipio['NombreDepto'].strip()}"
    )
    # FOOTER
    canvas.drawString(
        40, 15, f"Generado por el Sistema Administrativo Financiero Tributario - SAFT {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    canvas.drawRightString(
        doc.pagesize[0] - 40, 15, f"Página {canvas.getPageNumber()}")

    canvas.restoreState()


def primera_pagina(canvas, doc):
    canvas.saveState()

    # Solo footer o número de página si quieres
    canvas.setFont("Helvetica", 8)
    canvas.drawString(
        40, 20, f"Generado por el Sistema Administrativo Financiero Tributario - SAFT {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    canvas.drawRightString(doc.pagesize[0] - 40, 20,
                           f"Página {canvas.getPageNumber()}")

    canvas.restoreState()
