import logging

_logger = None


def configurar_logger(nombre_app="saft_app", nivel=logging.INFO):
    global _logger

    if _logger is not None:
        return _logger

    logger = logging.getLogger(nombre_app)
    logger.setLevel(nivel)

    if not logger.handlers:
        console = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console.setFormatter(formatter)
        logger.addHandler(console)

    _logger = logger
    return logger
