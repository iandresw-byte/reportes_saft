class AbonadosRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_mora_por_abonado_servicio(self, cta_cuenta, cta_recuperacion, cta_interes, cta_recargo):
        query = """
                SELECT        
                F_01.DNI, FC_03.Pnombre , FC_03.SNombre , FC_03.PApellido , FC_03.SApellido, 
                FC_04.ASPE_Seq AS CodAbonado, 
                FC_04.NoCuenta AS CuentaAbonado, 
                FC_05.CtaIngreso, 
                CuentaIngreso_A.NombreCtaIngreso, 
                CAST(MONTH(MIN(f_01.fechavenceavpg)) AS int) AS mes_inicial,
                CAST(YEAR(MIN(f_01.fechavenceavpg)) AS int) AS anio_inicial,
                CAST(MONTH(MAX(f_01.fechavenceavpg)) AS int) AS mes_final,
                CAST(YEAR(MAX(f_01.fechavenceavpg)) AS int) AS anio_final,
                CAST(SUM(CASE WHEN f_02.CtaIngreso LIKE ? THEN f_02.valorunitavpgdet ELSE 0 END) AS FLOAT) AS servicio,
                CAST(SUM(CASE WHEN f_02.CtaIngreso LIKE ? THEN f_02.valorunitavpgdet ELSE 0 END) AS FLOAT) AS recuperacion,
                CAST(SUM(CASE WHEN f_02.CtaIngreso LIKE ? THEN f_02.valorunitavpgdet ELSE 0 END) AS FLOAT) AS interes,
                CAST(SUM(CASE WHEN f_02.CtaIngreso LIKE ? THEN f_02.valorunitavpgdet ELSE 0 END) AS FLOAT) AS recargo
                FROM            F_01 INNER JOIN
                F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                CuentaIngreso_A ON YEAR(F_01.FechaVenceAvPg) = CuentaIngreso_A.Anio INNER JOIN
                FC_04 ON F_01.CodDeclara = FC_04.ASPE_Seq INNER JOIN
                FC_03 ON F_01.DNI = FC_03.DNI AND FC_04.Identidad = FC_03.DNI INNER JOIN
                FC_05 ON FC_04.ASPE_Seq = FC_05.ASPE_Seq AND CuentaIngreso_A.CtaIngreso = FC_05.CtaIngreso
                WHERE        (F_01.AvPgEstado = 1) AND (FC_05.CtaIngreso = ?) and  FC_04.ASPE_Estado = 0
                GROUP BY F_01.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_04.ASPE_Seq, 
                FC_04.NoCuenta, FC_05.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_cuenta, cta_recuperacion, cta_interes, cta_recargo, cta_cuenta,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]