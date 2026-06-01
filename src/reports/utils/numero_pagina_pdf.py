

def agregar_numero_pagina(canvas, doc):
    pagina = canvas.getPageNumber()
    texto = f"Página {pagina}"

    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        doc.pagesize[0] - 40,  # derecha
        20,                    # abajo
        texto
    )
    canvas.restoreState()
