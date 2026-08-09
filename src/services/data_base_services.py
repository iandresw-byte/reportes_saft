
from src.repositories.data_base_repository import DataBaseRepository


class DataBaseService:
    def __init__(self, conexion):
        self.repository = DataBaseRepository(conexion)

    def alterar_parametro_cont(self):
        return self.repository.parametroCont()

    def alterar_apremio(self):
        return self.repository.modifiaciones_apremio()

    def alterar_login(self):
        return self.repository.actualizar_login()

    def create_vistas(self):
        return self.repository.crear_vistas_powerBI()