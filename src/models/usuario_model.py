class Usuario:

    def __init__(
        self,
        username: str,
        UsuarioNombre: str,
        Identidad: str,
        ModuloCod: dict,
        Mnu: dict
    ):

        self.username = username
        self.nombre = UsuarioNombre
        self.identidad = Identidad
        self.modulos = ModuloCod
        self.permisos = Mnu

    def tiene_modulo(self, modulo: str) -> bool:
        return modulo in self.modulos

    def validar_permiso(self, modulo: str, menu: str, accion: str = "acceso") -> bool:

        try:
            return self.permisos[menu][accion]
        except KeyError:
            return False
