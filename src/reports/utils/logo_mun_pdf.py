import os
from reportlab.platypus import Image
from reportlab.lib.units import cm


def logo_muni_imagen(ruta_base: str) -> Image | None:
    if os.path.exists(ruta_base + ".png"):
        ASSETS_DIR = ruta_base + ".png"
    elif os.path.exists(ruta_base + ".jpeg"):
        ASSETS_DIR = ruta_base + ".jpeg"
    elif os.path.exists(ruta_base + ".jpg"):
        ASSETS_DIR = ruta_base + ".jpg"
    else:
        ASSETS_DIR = None

    if ASSETS_DIR:
        return Image(ASSETS_DIR, width=2.84*cm, height=2.52*cm)
    else:
        return None


def logo_muni_imagen_media_carta(ruta_base: str) -> Image | None:
    if os.path.exists(ruta_base + ".png"):
        ASSETS_DIR = ruta_base + ".png"
    elif os.path.exists(ruta_base + ".jpeg"):
        ASSETS_DIR = ruta_base + ".jpeg"
    elif os.path.exists(ruta_base + ".jpg"):
        ASSETS_DIR = ruta_base + ".jpg"
    else:
        ASSETS_DIR = None

    if ASSETS_DIR:
        return Image(ASSETS_DIR, width=1.20*cm, height=1.20*cm)
    else:
        return None
