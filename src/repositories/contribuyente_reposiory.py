from datetime import date, datetime


class ContribuyenteReposiory:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_contribuyente(self, dni: str, fecha_ahora: str):
        query = f"""
                    SELECT FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion, 
                    MIN(F_01.FechaVenceAvPg) AS mes_ini, 
                    MAX(F_01.FechaVenceAvPg) AS mes_fin, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111110' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS bi, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111111' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ip, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111112' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ic, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111113' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS com, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6)  = '111114' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ser, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111118' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS servicios, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111116' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS pecuario, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6)  = '111119' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS tasas, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112120' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS multas, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112121' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recargos, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112122' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacion, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112123' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionSp, 
                    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112126' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS intereses, 
                    CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS total,
                    Aldea.NombreAldea, 
                    TablaBarrio.NombreBarrio
                    FROM F_01 INNER JOIN
                    FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                    F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                    Aldea ON FC_03.CodAldea = Aldea.CodAldea INNER JOIN
                    TablaBarrio ON FC_03.CodBarrio = TablaBarrio.CodBarrio AND Aldea.CodAldea = TablaBarrio.CodAldea
                    WHERE (F_01.AvPgEstado = 1) AND (F_01.FechaVenceAvPg < ?) AND (FC_03.DNI LIKE ?) 
                    GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion, Aldea.NombreAldea, TablaBarrio.NombreBarrio
                """

        with self.conexion.cursor() as cur:
            cur.execute(query, fecha_ahora, dni)
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
