class MoraAldeasRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def mora_vs_ingresos_general(self, tipo_impuesto='0,1,2,3,4,5,7'):

        lista_tipo = [x.strip() for x in tipo_impuesto.split(",")]

        placeholders = ",".join(["?"] * len(lista_tipo))

        query = f"""
        SELECT FC_03.CodAldea, 
        Aldea.NombreAldea, 
        CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS TotalGenerado,
        COUNT(F_02.NumAvPg) as totalFacturas,
        CAST(SUM(CASE WHEN F_01.AvPgEstado = 1 THEN 1 ELSE 0 END) AS FLOAT) AS MoraTotalFacturas, 
        CAST(SUM(CASE WHEN F_01.AvPgEstado = 1 THEN F_02.ValorUnitAvpgDet ELSE 0 END) AS FLOAT) AS MoraTotal, 
        CAST(SUM(CASE WHEN F_01.AvPgEstado = 2 THEN 1 ELSE 0 END) AS FLOAT) AS ingresosTotalFacturas, 
        CAST(SUM(CASE WHEN F_01.AvPgEstado = 2 THEN F_02.ValorUnitAvpgDet ELSE 0 END) AS FLOAT) AS Ingresos,  
        CASE WHEN CAST(SUM(F_02.ValorUnitAvpgDet) AS FLOAT) = 0 THEN 0 ELSE ROUND(CAST(SUM(CASE WHEN F_01.AvPgEstado = 1 THEN F_02.ValorUnitAvpgDet END) AS FLOAT) * 100.0 / CAST(SUM(F_02.ValorUnitAvpgDet) AS FLOAT), 2) END AS PorcentajeMora,
        CASE WHEN CAST(SUM(F_02.ValorUnitAvpgDet) AS FLOAT) = 0 THEN 0 ELSE ROUND(CAST(SUM(CASE WHEN F_01.AvPgEstado = 2 THEN F_02.ValorUnitAvpgDet END) AS FLOAT) * 100.0 / CAST(SUM(F_02.ValorUnitAvpgDet) AS FLOAT), 2) END AS PorcentajeIngresos
        FROM F_01 INNER JOIN
        F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
        FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
        Aldea ON FC_03.CodAldea = Aldea.CodAldea
        WHERE (F_01.AvPgEstado IN (1, 2)) and (F_01.AvPgTipoImpuesto IN ({placeholders})) and ( F_01.FechaVenceAvPg < getdate())
        GROUP BY FC_03.CodAldea, Aldea.NombreAldea
        ORDER BY PorcentajeMora
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (lista_tipo))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def mora_bi_ubicacion(self, cod_aldea: str, ubicacion: int):

        query = f"""
            SELECT YEAR(F_01.FechaVenceAvPg) AS anio, FC_01.CodAldea, Aldea.NombreAldea, CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS TotalGenerado, COUNT(F_02.NumAvPg) AS totalFacturas, 
            CAST(SUM(CASE WHEN F_01.AvPgEstado = 1 THEN 1 ELSE 0 END) AS FLOAT) AS MoraTotalFacturas, CAST(SUM(CASE WHEN F_01.AvPgEstado = 1 THEN F_02.ValorUnitAvpgDet ELSE 0 END) AS FLOAT) AS MoraTotal, 
            CAST(SUM(CASE WHEN F_01.AvPgEstado = 2 THEN 1 ELSE 0 END) AS FLOAT) AS ingresosTotalFacturas, CAST(SUM(CASE WHEN F_01.AvPgEstado = 2 THEN F_02.ValorUnitAvpgDet ELSE 0 END) AS FLOAT) AS Ingresos, 
            CASE WHEN CAST(SUM(F_02.ValorUnitAvpgDet) AS FLOAT) = 0 THEN 0 ELSE ROUND(CAST(SUM(CASE WHEN F_01.AvPgEstado = 1 THEN F_02.ValorUnitAvpgDet END) AS FLOAT) * 100.0 / CAST(SUM(F_02.ValorUnitAvpgDet) AS FLOAT), 2) 
            END AS PorcentajeMora, CASE WHEN CAST(SUM(F_02.ValorUnitAvpgDet) AS FLOAT) = 0 THEN 0 ELSE ROUND(CAST(SUM(CASE WHEN F_01.AvPgEstado = 2 THEN F_02.ValorUnitAvpgDet END) AS FLOAT) * 100.0 / CAST(SUM(F_02.ValorUnitAvpgDet) AS FLOAT), 2) END AS PorcentajeIngresos
            FROM FC_01 INNER JOIN
            Aldea ON FC_01.CodAldea = Aldea.CodAldea INNER JOIN
            F_01 INNER JOIN
            F_02 ON F_01.NumAvPg = F_02.NumAvPg ON FC_01.CatClv = F_01.ClaveCatastro
            WHERE (F_01.AvPgEstado IN (1, 2)) AND (F_01.AvPgTipoImpuesto = 1) AND (F_01.FechaVenceAvPg < GETDATE()) AND (FC_01.CodAldea like ?) AND (FC_01.Ubicacion = ?)
            GROUP BY YEAR(F_01.FechaVenceAvPg), FC_01.CodAldea, Aldea.NombreAldea
            ORDER BY anio
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cod_aldea, ubicacion))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
