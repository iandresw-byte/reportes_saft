class TrancicionBIRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_bi_urbano(self):
        query = """
                SELECT COUNT(CatClv) AS Total
                FROM FC_01
                WHERE (Ubicacion = 0)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_bi_rural(self):
        query = """
                SELECT COUNT(CatClv) AS Total
                FROM FC_01
                WHERE (Ubicacion = 1)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_bi_urbano_activos(self, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT COUNT(DISTINCT F_01.ClaveCatastro) AS Total
            FROM F_01 INNER JOIN
            FC_01 ON F_01.ClaveCatastro = FC_01.CatClv
            WHERE (FC_01.Ubicacion = 0) AND (F_01.AvPgEstado = 2) AND (F_01.AvPgTipoImpuesto = 1)
            AND (year(F_01.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_bi_rural_activos(self, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT COUNT(DISTINCT F_01.ClaveCatastro) AS Total
            FROM F_01 INNER JOIN
            FC_01 ON F_01.ClaveCatastro = FC_01.CatClv
            WHERE (FC_01.Ubicacion = 1) AND (F_01.AvPgEstado = 2) AND (F_01.AvPgTipoImpuesto = 1)
            AND (year(F_01.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
    # detalles tecnificado declaracion

    def obtener_tec_anio_inicio(self, ubicacion: int, anio_inicio_periodo: str):
        query = """
                SELECT COUNT(DISTINCT FC_01.CatClv) AS Total
                FROM  FC_01 INNER JOIN
                F_FichaUrb ON FC_01.CatClv = F_FichaUrb.ClaveCatastro
                WHERE (FC_01.Ubicacion = ?) AND  (F_FichaUrb.FechaAvaluo < ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion, anio_inicio_periodo))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_tec_anio_fin(self, ubicacion: int):
        query = """
                SELECT COUNT(DISTINCT FC_01.CatClv) AS Total
                FROM  FC_01 INNER JOIN
                F_FichaUrb ON FC_01.CatClv = F_FichaUrb.ClaveCatastro
                WHERE (FC_01.Ubicacion = ?) 
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_dec_anio_inicio(self, ubicacion: int, anio_inicio_periodo: str):
        query = """
                SELECT COUNT(DISTINCT FC_01.CatClv) AS Total
                FROM  FC_01 INNER JOIN
                DeclaraBI ON FC_01.CatClv = DeclaraBI.ClaveCatastro
                WHERE (FC_01.Ubicacion = ?) AND ( DeclaraBI.FechaDeclaraBI < ?) AND (FC_01.CatClv NOT IN
                             (SELECT        ClaveCatastro
                               FROM            F_FichaUrb))
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion, anio_inicio_periodo))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_dec_anio_fin(self, ubicacion: int):
        query = """
SELECT COUNT(DISTINCT FC_01.CatClv) AS Total
FROM  FC_01 INNER JOIN
DeclaraBI ON FC_01.CatClv = DeclaraBI.ClaveCatastro
WHERE (FC_01.Ubicacion = ?) AND (FC_01.CatClv NOT IN
                             (SELECT        ClaveCatastro
                               FROM            F_FichaUrb))
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion, ))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
    # DETALLE PROPEIADES

    def obtener_bi_urbano_detalle(self):
        query = """
                SELECT FC_01.CatClv, FC_01.DNI, FC_01.Direccion, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
                FROM FC_01 INNER JOIN
                FC_03 ON FC_01.DNI = FC_03.DNI
                WHERE (FC_01.Ubicacion = 0)
                GROUP BY FC_01.CatClv, FC_01.DNI, FC_01.Direccion, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
                """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_bi_rural_detalle(self):
        query = """
                SELECT FC_01.CatClv, FC_01.DNI, FC_01.Direccion, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
                FROM FC_01 INNER JOIN
                FC_03 ON FC_01.DNI = FC_03.DNI
                WHERE (FC_01.Ubicacion = 1)
                GROUP BY FC_01.CatClv, FC_01.DNI, FC_01.Direccion, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
                """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_bi_urbano_activos_detalle(self, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT FC_01.CatClv, FC_03.DNI, FC_01.Direccion, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
            FROM FC_01 INNER JOIN
            F_01 ON F_01.ClaveCatastro = FC_01.CatClv INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI AND F_01.DNI = FC_03.DNI
            WHERE (FC_01.Ubicacion = 0) AND (F_01.AvPgEstado = 2) AND (F_01.AvPgTipoImpuesto = 1) AND (year(F_01.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (anio))
            row = cur.fetchone()
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_bi_rural_activos_detalle(self, anio: str):
        anio = str(anio)[:4]
        query = """
            SELECT FC_01.CatClv, F_01.DNI, FC_01.Direccion, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido
            FROM FC_01 INNER JOIN
            F_01 ON F_01.ClaveCatastro = FC_01.CatClv INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI AND F_01.DNI = FC_03.DNI
            WHERE (FC_01.Ubicacion = 1) AND (F_01.AvPgEstado = 2) AND (F_01.AvPgTipoImpuesto = 1) AND (year(F_01.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (anio))

            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
    # DETALLE CATASTRO TECNIFICADO

    def obtener_tec_anio_inicio_detalle(self, ubicacion: int, anio_inicio_periodo: str):
        query = """
                SELECT  FC_01.CatClv, FC_01.Direccion, FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, F_FichaUrb.FechaAvaluo
                FROM FC_01 INNER JOIN
                F_FichaUrb ON FC_01.CatClv = F_FichaUrb.ClaveCatastro INNER JOIN
                FC_03 ON FC_01.DNI = FC_03.DNI
                WHERE (FC_01.Ubicacion = ?) AND (F_FichaUrb.FechaAvaluo < ?)
                GROUP BY FC_01.CatClv, FC_01.Direccion, FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, F_FichaUrb.FechaAvaluo
                ORDER BY F_FichaUrb.FechaAvaluo
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion, anio_inicio_periodo))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_tec_anio_fin_detalle(self, ubicacion: int):
        query = """
                SELECT  FC_01.CatClv, FC_01.Direccion, FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, F_FichaUrb.FechaAvaluo
                FROM FC_01 INNER JOIN
                F_FichaUrb ON FC_01.CatClv = F_FichaUrb.ClaveCatastro INNER JOIN
                FC_03 ON FC_01.DNI = FC_03.DNI
                WHERE (FC_01.Ubicacion = ?) 
                GROUP BY FC_01.CatClv, FC_01.Direccion, FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, F_FichaUrb.FechaAvaluo
                ORDER BY F_FichaUrb.FechaAvaluo
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    # DETALLE CATASTRO DECLARADO

    def obtener_dec_anio_inicio_detalle(self, ubicacion: int, anio_inicio_periodo: str):
        query = """
                SELECT  FC_01.CatClv, FC_01.Direccion, FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, 
                DeclaraBI.FechaOperacionBI
                FROM FC_01 INNER JOIN
                DeclaraBI ON FC_01.CatClv = DeclaraBI.ClaveCatastro INNER JOIN
                FC_03 ON FC_01.DNI = FC_03.DNI
                WHERE (FC_01.Ubicacion = ?) AND (DeclaraBI.FechaDeclaraBI< ?) AND (FC_01.CatClv NOT IN
                (SELECT  ClaveCatastro FROM F_FichaUrb))
                GROUP BY FC_01.CatClv, FC_01.Direccion, FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, DeclaraBI.FechaOperacionBI, 
                DeclaraBI.FechaDeclaraBI
                ORDER BY DeclaraBI.FechaDeclaraBI
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion, anio_inicio_periodo))

            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_dec_anio_fin_detalle(self, ubicacion: int):
        query = """
                SELECT   FC_01.CatClv, FC_01.Direccion, FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, 
                DeclaraBI.FechaOperacionBI
                FROM FC_01 INNER JOIN
                DeclaraBI ON FC_01.CatClv = DeclaraBI.ClaveCatastro INNER JOIN
                FC_03 ON FC_01.DNI = FC_03.DNI
                WHERE (FC_01.Ubicacion = ?)  AND (FC_01.CatClv NOT IN
                (SELECT  ClaveCatastro FROM F_FichaUrb))
                GROUP BY FC_01.CatClv, FC_01.Direccion, FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, DeclaraBI.FechaOperacionBI, 
                DeclaraBI.FechaDeclaraBI
                ORDER BY DeclaraBI.FechaDeclaraBI
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
