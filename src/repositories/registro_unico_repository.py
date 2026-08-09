from src.database.consultas.tarjeta_unica import *

class RegistroUnicoRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_registro_unico_gob(self, identidad='%10039010340949%'):
        query = CONSULTA_REGISTRO_UNICO_GOB
        with self.conexion.cursor() as cur:
            cur.execute(query, (identidad))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_declaraciones_bienes_inmuebles(self, identidad='%10039010340949%'):
            query = CONSULTA_DECLARACIONES_BIENES_INMUBLES
            with self.conexion.cursor() as cur:
                cur.execute(query, (identidad))
                rows = cur.fetchall()
                if not rows:
                    return None
                columns = [c[0] for c in cur.description]
                return [dict(zip(columns, r)) for r in rows]

    def obtener_declaraciones_industria_comercio(self, identidad='%10039010340949%'):
                query = CONSULTA_DECLARACIONES_INDUSTRIA_COMERCIO
                with self.conexion.cursor() as cur:
                    cur.execute(query, (identidad))
                    rows = cur.fetchall()
                    if not rows:
                        return None
                    columns = [c[0] for c in cur.description]
                    return [dict(zip(columns, r)) for r in rows]

    def obtener_contribuyente(self, identidad='%10039010340949%'):
                query = CONSULTA_CONTRIBUYENTE
                with self.conexion.cursor() as cur:
                    cur.execute(query, (identidad))
                    row = cur.fetchone()
                    if not row:
                        return None
                    columns = [column[0] for column in cur.description]
                    return dict(zip(columns, row))

    def obtener_tasas(self, anio='%10039010340949%'):
                    query = CONSULTA_TASAS
                    with self.conexion.cursor() as cur:
                        cur.execute(query, (anio))
                        row = cur.fetchone()
                        if not row:
                            return None
                        columns = [column[0] for column in cur.description]
                        return dict(zip(columns, row))