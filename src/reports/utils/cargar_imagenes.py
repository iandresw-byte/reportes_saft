import os
from reportlab.platypus import Image


def cargar_iconos_licencia(BASE_DIR):
    iconos = []
    ancho = 20
    alto = 20
    imagen = os.path.join(BASE_DIR, "assets", "images", "propietario.ico")
    iconos.append(Image(imagen, width=ancho, height=alto))
    imagen = os.path.join(BASE_DIR, "assets", "images", "dni.ico")
    iconos.append(Image(imagen, width=ancho, height=alto))
    imagen = os.path.join(BASE_DIR, "assets", "images", "establecimient.ico")
    iconos.append(Image(imagen, width=ancho, height=alto))
    imagen = os.path.join(BASE_DIR, "assets", "images", "maps.ico")
    iconos.append(Image(imagen, width=ancho, height=alto))
    imagen = os.path.join(BASE_DIR, "assets", "images", "calendar.ico")
    iconos.append(Image(imagen, width=ancho, height=alto))
    imagen = os.path.join(BASE_DIR, "assets", "images", "calendar.ico")
    iconos.append(Image(imagen, width=ancho, height=alto))
    imagen = os.path.join(BASE_DIR, "assets", "images", "recibo.ico")
    iconos.append(Image(imagen, width=ancho, height=alto))
    imagen = os.path.join(BASE_DIR, "assets", "images", "periodo.ico")
    iconos.append(Image(imagen, width=ancho, height=alto))

    return iconos
