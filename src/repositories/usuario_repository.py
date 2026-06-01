from src.models.usuario_model import Usuario


class UsuarioRepository():
    def __init__(self, conexion):
        self.conexion = conexion

    def get_usuario_por_credenciales(self, usuario, password):
        cursor = self.conexion.obtener_cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM Usuario WHERE UsuarioCod = ? AND UsuarioPass = ?", (usuario, password))
        resultado = cursor.fetchone()
        return resultado[0] > 0

    def obtener_datos_usuario(self, usuario):

        cursor = self.conexion.obtener_cursor()

        query = """
            SELECT
                u.UsuarioNombre,
                u.Identidad,
                um.ModuloCod,
                um.UMLevel,
                ua.Mnu,
                ua.Acceso,
                ua.Guarda,
                ua.Modifica,
                ua.Elimina
            FROM Usuario AS u
            INNER JOIN UsuarioModulo AS um
                ON u.UsuarioCod = um.UsuarioCod
            INNER JOIN UsuarioAcc AS ua
                ON um.UsuarioCod = ua.Usuario
                AND um.ModuloCod = ua.Modulo
            WHERE u.UsuarioCod = ?
        """

        cursor.execute(query, (usuario,))
        rows = cursor.fetchall()

        if not rows:
            return None

        columns = [c[0] for c in cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def obtener_modulos_usuario(self, usuario):

        cursor = self.conexion.obtener_cursor()

        query = """
                SELECT um.ModuloCod, um.UMLevel, u.Identidad, u.UsuarioNombre
                FROM Usuario AS u INNER JOIN
                UsuarioModulo AS um ON u.UsuarioCod = um.UsuarioCod
                WHERE (u.UsuarioCod = ?)
        """

        cursor.execute(query, (usuario,))
        rows = cursor.fetchall()

        if not rows:
            return None

        columns = [c[0] for c in cursor.description]

        return [dict(zip(columns, row)) for row in rows]
