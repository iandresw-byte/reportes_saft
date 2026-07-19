from src.repositories.registro_unico_repository import RegistroUnicoRepository


class RegistroUnicoService:
    def __init__(self, conexion):
        self.repository = RegistroUnicoRepository(conexion)

    def obtener_ruc(self, identidad):
        data_res = self.repository.obtener_registro_unico_gob(identidad)
        if not data_res:
            raise ValueError(
                f"Datos del contribuyente con la Identidad: {identidad}")
        return data_res


