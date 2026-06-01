from src.repositories.aldea_repository import AldeaRepository


class AldeaService:
    def __init__(self, conexion):
        self.repository = AldeaRepository(conexion)

    def obtener_aldeas(self):
        data_res = self.repository.obtener_aldeas()
        if not data_res:
            raise ValueError(
                "No se encontraron Aldeas (respuesta vacía).")
        return data_res

    def obtener_barrio(self, cod_aldea):
        data_res = self.repository.obtener_barrios(cod_aldea)
        if not data_res:
            raise ValueError("No se encontraron Barrios (respuesta vacía).")
        return data_res
