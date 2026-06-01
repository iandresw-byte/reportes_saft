

from src.repositories.usuario_repository import UsuarioRepository, Usuario
from src.utils.encriptador import ms_encrypt


class UsuarioService:
    def __init__(self, conexion):
        self.repo = UsuarioRepository(conexion)

    def login(self, usuario: str, password: str) -> bool:
        clave = ms_encrypt(password, "M1")
        datos_usuario = self.repo.get_usuario_por_credenciales(usuario, clave)
        return datos_usuario

    def obtener_datos_usuario(self, usuario) -> Usuario | None:

        accesos = self.repo.obtener_datos_usuario(usuario)
        modulos_res = self.repo.obtener_modulos_usuario(usuario)

        modulo = {}
        permisos = {}

        if modulos_res:
            nombre = modulos_res[0]["UsuarioNombre"]
            identidad = modulos_res[0]["Identidad"]
            for item in modulos_res:
                mod = item["ModuloCod"]
                modulo[mod] = {
                    "nivel": bool(item["UMLevel"]),
                }
        else:
            return None
        if accesos:
            for item in accesos:
                menu = item["Mnu"]
                permisos[menu] = {
                    "acceso": bool(item["Acceso"]),
                    "guarda": bool(item["Guarda"]),
                    "modifica": bool(item["Modifica"]),
                    "elimina": bool(item["Elimina"]),
                }

        else:
            menu = "Mnu"
            permisos["CkPo"] = {
                "acceso": bool(0),
                "guarda": bool(0),
                "modifica": bool(0),
                "elimina": bool(0),
            }
            permisos["ChkDipe"] = {
                "acceso": bool(0),
                "guarda": bool(0),
                "modifica": bool(0),
                "elimina": bool(0),
            }

        return Usuario(
            username=usuario.upper(),
            UsuarioNombre=nombre,
            Identidad=identidad,
            ModuloCod=modulo,
            Mnu=permisos,
        )
