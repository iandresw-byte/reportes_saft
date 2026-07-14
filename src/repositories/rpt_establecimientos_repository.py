class RptEstablecimientoRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_mora_establecimiento_por_tipo(self, cta_cuentas_list:list):
        query = """
            DECLARE @CTA_INDUSTRIA VARCHAR(20)= ?;
            DECLARE @CTA_COMERCIO VARCHAR(20)= ?;
            DECLARE @CTA_SERVICIOS VARCHAR(20)= ?;

            DECLARE @CTA_RECUPERACION_I VARCHAR(20)= ?;
            DECLARE @CTA_RECUPERACION_C VARCHAR(20)= ?;
            DECLARE @CTA_RECUPERACION_S VARCHAR(20)= ?;

            DECLARE @CTA_PERMISO_OPERACION VARCHAR(20)= ?;

            DECLARE @CTA_INTERESES VARCHAR(20)= ?;
            DECLARE @CTA_RECARGOS VARCHAR(20)= ?;

            DECLARE @CTA_DESCUENTOS VARCHAR(20)= ?;
            DECLARE @CTA_MULTAS VARCHAR(20)= ?;
            
            DECLARE @CTA_ACTIVIDAD VARCHAR(20)= ?;

            SELECT FC_03.DNI AS rtm, FC_03.pNombre AS Establecimiento, PC_03.DNI, PC_03.PNombre, PC_03.SNombre, PC_03.PApellido, PC_03.SApellido,
            FC_03.CodProfesion as CodActividad, FC_03.Direccion, FC_03.Telefono,
            CAST(MONTH(MIN(f_01.fechavenceavpg)) AS int) AS mes_inicial,
            CAST(YEAR(MIN(f_01.fechavenceavpg)) AS int) AS anio_inicial,
            CAST(MONTH(MAX(f_01.fechavenceavpg)) AS int) AS mes_final,
            CAST(YEAR(MAX(f_01.fechavenceavpg)) AS int) AS anio_final,
            CAST(SUM(CASE WHEN F_02.CtaIngreso LIKE LTRIM(@CTA_INDUSTRIA) THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS float) AS MoraIndusActual,
            CAST(SUM(CASE WHEN F_02.CtaIngreso LIKE LTRIM(@CTA_COMERCIO) THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS float) AS MoraComerActual,
            CAST(SUM(CASE WHEN F_02.CtaIngreso LIKE LTRIM(@CTA_SERVICIOS) THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS float) AS MoraServicActual,
            CAST(SUM(CASE WHEN F_02.CtaIngreso LIKE LTRIM(@CTA_RECUPERACION_I) THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS float) AS MoraAniosAnte_I,
            CAST(SUM(CASE WHEN F_02.CtaIngreso LIKE LTRIM(@CTA_RECUPERACION_C) THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS float) AS MoraAniosAnte_C,
            CAST(SUM(CASE WHEN F_02.CtaIngreso LIKE LTRIM(@CTA_RECUPERACION_S) THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS float) AS MoraAniosAnte_S,
            CAST(SUM(CASE WHEN F_02.CtaIngreso LIKE LTRIM(@CTA_PERMISO_OPERACION) THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS float) AS PermisoOpetacion,
            CAST(SUM(CASE WHEN F_02.CtaIngreso LIKE LTRIM(@CTA_INTERESES) THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS float) AS Intereses,
            CAST(SUM(CASE WHEN F_02.CtaIngreso LIKE LTRIM(@CTA_RECARGOS) THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS float) AS Recargos,
            CAST(SUM(CASE WHEN F_02.CtaIngreso LIKE LTRIM(@CTA_MULTAS) THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS float) AS Multas,
            CAST(SUM(CASE WHEN F_02.CtaIngreso LIKE LTRIM(@CTA_DESCUENTOS) THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS float) AS Descuentos,
            CAST(SUM(F_02.ValorUnitAvPgDet) AS float) AS Saldo_Sumado
            FROM 
            F_01 INNER JOIN F_02  ON F_01.NumAvPg = F_02.NumAvPg 
            INNER JOIN FC_03 ON F_01.DNI = FC_03.DNI
            INNER JOIN FC_03 AS PC_03 ON  FC_03.IdRepresentante = PC_03.DNI
            WHERE  F_01.AvPgEstado = 1 AND F_02.CtaIngreso LIKE @CTA_ACTIVIDAD
            GROUP BY FC_03.DNI, FC_03.pNombre, PC_03.DNI, PC_03.pNombre, PC_03.snombre, PC_03.papellido, PC_03.sapellido,
            FC_03.CodProfesion, FC_03.Direccion, FC_03.Telefono
            ORDER BY CodActividad
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, cta_cuentas_list)
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]