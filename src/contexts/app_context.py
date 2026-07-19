import logging
from src.models.municipio_admin import Administracion, Municipio
from src.services.parametro_service import ParametroService
from src.database.conexion import ConexionBD
from src.models.usuario_model import Usuario
from src.services.usuario_services import UsuarioService
from src.utils.logger_config import configurar_logger
from src.utils.config_manager import Config

class AppContext:
    def __init__(self):
        self._conexion_saft = None

        self._conexion_bitacora = None
        self._auth_service = None
        self._administracion_service = None
        self.municipio: str = ""
        self.departamento: str = ""
        self.datos_muni = None
        self.datos_admin = None
        self.datos_system = None
        self.usuario_actual: Usuario = None  # type: ignore
        self.administracion: str = None  # type: ignore
        self.cod_muni = None
        self.tamanio_documento: str = ""
        self.logger = configurar_logger(
            nombre_app="saft_app_bd",
            nivel=logging.INFO
        )

    def init_saft(self):
        self.tamanio_documento = Config.obtener("APREMIO", "tipo_documento")
        if not self._conexion_saft:
            self._conexion_saft = ConexionBD('SAFT', self.logger)
            self._auth_service = UsuarioService( self._conexion_saft)
            self._administracion_service = ParametroService(
                self._conexion_saft)

    def init_bitacora(self):
        if not self._conexion_bitacora:
            self._conexion_bitacora = ConexionBD('SAFTBIT', self.logger)

    def init_services(self):
        self._conexion = ConexionBD('SAFT', self.logger)
        self._auth_service = UsuarioService(self._conexion )
        self._administracion_service = ParametroService(self._conexion_saft)

    @property
    def conexion_saft(self):
        return self._conexion_saft

    @property
    def conexion_bitacora(self):
        return self._conexion_bitacora

    @property
    def auth_service(self):
        return self._auth_service

    @property
    def administracion_service(self):
        return self._administracion_service

    

