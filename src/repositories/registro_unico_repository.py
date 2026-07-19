from src.database.consultas.tarjeta_unica import *

class RegistroUnicoRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_registro_unico_gob(self, identidad):
        query = CONSULTA_REGISTRO_UNICO_GOB
        with self.conexion.cursor() as cur:
            cur.execute(query, (identidad))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    