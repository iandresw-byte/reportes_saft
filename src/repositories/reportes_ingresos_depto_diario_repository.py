import datetime


class IngresosDeptosDiarioRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_diario_catastro(self, fecha_ini: str, fecha_fin: str):
        query = """SELECT F_03.FechaRecibo, 
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '2111010200' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS VentaDominioPleno,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990220' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Constancias,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '152190101' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS ServiciosDocimentacion,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '152190103' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS MedidasRemedidas,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 11) = '12599021701' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS RegistrosPropiedad,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '21110101' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS LotesCementerio,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990207' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Inspeccion,
                    CAST(SUM(F_04.ValorUnitReciboDet) AS float) AS TotalReciboPagado
                    FROM  F_03 INNER JOIN
                    F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
                    Usuario INNER JOIN
                    PLA_DEPARTAMENTOS ON Usuario.CodDepto = PLA_DEPARTAMENTOS.IdDeptos INNER JOIN
                    F_01 ON Usuario.UsuarioCod = F_01.CreadoPor ON F_04.NumFactura = F_01.NumAvPg INNER JOIN
                    FC_03 ON F_03.DNI = FC_03.DNI
                    WHERE (F_03.ReciboAnulado = 0) AND  (F_03.FechaRecibo BETWEEN ? AND ?)  AND (PLA_DEPARTAMENTOS.IdDeptos = 1)
                    GROUP BY F_03.FechaRecibo
                    ORDER BY F_03.FechaRecibo
                   """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini,  fecha_fin,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_diario_ics_otras(self, fecha_ini: str, fecha_fin: str):
        query = """SELECT F_03.FechaRecibo,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 8) = '12599022' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT)  AS Constancias, 
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 3) = '117' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Impuestos,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1521902' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Servicios,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 8) = '125990221' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Certificaciones, 
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '152190101' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Documentacion, 
                    CAST(SUM(F_04.ValorUnitReciboDet) AS FLOAT) AS TotalReciboPagado
                    FROM  F_03 INNER JOIN
                    F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
                    Usuario INNER JOIN
                    PLA_DEPARTAMENTOS ON Usuario.CodDepto = PLA_DEPARTAMENTOS.IdDeptos INNER JOIN
                    F_01 ON Usuario.UsuarioCod = F_01.CreadoPor ON F_04.NumFactura = F_01.NumAvPg INNER JOIN
                    FC_03 ON F_03.DNI = FC_03.DNI
                    WHERE        (F_03.ReciboAnulado = 0) AND (F_03.FechaRecibo BETWEEN ? AND ?) AND (PLA_DEPARTAMENTOS.IdDeptos = 2) AND (F_01.AvPgTipoImpuesto = 0)
                    GROUP BY F_03.FechaRecibo
                    ORDER BY F_03.FechaRecibo
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini,  fecha_fin,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_diario_ics_ab(self, fecha_ini: str, fecha_fin: str):
        query = """SELECT F_03.FechaRecibo,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 8) = '12599022' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT)  AS Constancias, 
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 3) = '117' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Impuestos,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1521902' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Servicios,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 8) = '125990221' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Certificaciones, 
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '152190101' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Documentacion, 
                    CAST(SUM(F_04.ValorUnitReciboDet) AS FLOAT) AS TotalReciboPagado
                    FROM  F_03 INNER JOIN
                    F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
                    Usuario INNER JOIN
                    PLA_DEPARTAMENTOS ON Usuario.CodDepto = PLA_DEPARTAMENTOS.IdDeptos INNER JOIN
                    F_01 ON Usuario.UsuarioCod = F_01.CreadoPor ON F_04.NumFactura = F_01.NumAvPg INNER JOIN
                    FC_03 ON F_03.DNI = FC_03.DNI
                    WHERE        (F_03.ReciboAnulado = 0) AND (F_03.FechaRecibo BETWEEN ? AND ?) AND (PLA_DEPARTAMENTOS.IdDeptos = 2) AND (F_01.AvPgTipoImpuesto = 8)
                    GROUP BY F_03.FechaRecibo
                    ORDER BY F_03.FechaRecibo
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini,  fecha_fin,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_diario_ics_bienes(self, fecha_ini: str, fecha_fin: str):
        query = """SELECT F_03.FechaRecibo, 
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 5) = '11720' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS ImpuestoBI,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '117298' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS RecuperacionBI,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '117297' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Intereses,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '117296' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Recargos,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1259903' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Multas,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '152190206' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Bomberos,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1521998' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS RecuBomberos,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1521997' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS IntereBomberos,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1521996' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS RecargosBomberos,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '112127' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS descuentos,
                    CAST(SUM(F_04.ValorUnitReciboDet) AS FLOAT ) AS TotalReciboPagado
                    FROM F_03 INNER JOIN
                    F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
                    Usuario INNER JOIN
                    PLA_DEPARTAMENTOS ON Usuario.CodDepto = PLA_DEPARTAMENTOS.IdDeptos INNER JOIN
                    F_01 ON Usuario.UsuarioCod = F_01.CreadoPor ON F_04.NumFactura = F_01.NumAvPg INNER JOIN
                    FC_03 ON F_03.DNI = FC_03.DNI
                    WHERE        (F_03.ReciboAnulado = 0) AND (F_03.FechaRecibo BETWEEN ? AND ?) AND (PLA_DEPARTAMENTOS.IdDeptos = 2) and f_01.AvPgTipoImpuesto in (1)
                    GROUP BY F_03.FechaRecibo
                    ORDER BY F_03.FechaRecibo"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini,  fecha_fin,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_diario_ics_comercio(self, fecha_ini: str, fecha_fin: str):
        query = """
                SELECT F_03.FechaRecibo,
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 5) = '11710' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT)  AS Comercio, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '117198' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS RecuperacionComercio,
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990230' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS PermisoOperacion, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990205' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Rotulos, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '117197' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Intereses, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '117196' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Recargos, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1259903' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Multas, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '152190206' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Bomberos, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1521998' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS RecuBomberos, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1521997' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS IntereBomberos, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1521996' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS RecargosBomberos, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '112127' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS descuentos, 
                CAST(SUM(F_04.ValorUnitReciboDet) AS FLOAT) AS TotalReciboPagado
                FROM  F_03 INNER JOIN
                F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
                Usuario INNER JOIN
                PLA_DEPARTAMENTOS ON Usuario.CodDepto = PLA_DEPARTAMENTOS.IdDeptos INNER JOIN
                F_01 ON Usuario.UsuarioCod = F_01.CreadoPor ON F_04.NumFactura = F_01.NumAvPg INNER JOIN
                FC_03 ON F_03.DNI = FC_03.DNI INNER JOIN
                CuentaIngreso_A ON FC_03.CodProfesion = CuentaIngreso_A.CtaIngreso AND FC_03.UltPeriodoFact = CuentaIngreso_A.Anio
                WHERE        (F_03.ReciboAnulado = 0) AND (F_03.FechaRecibo BETWEEN ? AND ?) AND (PLA_DEPARTAMENTOS.IdDeptos = 2) AND (F_01.AvPgTipoImpuesto in (2,3))
                GROUP BY F_03.FechaRecibo
                ORDER BY F_03.FechaRecibo
            """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini,  fecha_fin,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_diario_ics_personal(self, fecha_ini: str, fecha_fin: str):
        query = """
                SELECT F_03.FechaRecibo,
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '117301' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT)  AS Impuesto, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '117398' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Recuperacion,
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '117397' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Intereses, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '117396' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Recargos, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1259903' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Multas,  
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 11) = '12599022019' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Solvencia,  
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 6) = '112127' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Descuentos, 
                CAST(SUM(F_04.ValorUnitReciboDet) AS FLOAT) AS TotalReciboPagado
                FROM  F_03 INNER JOIN
                F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
                Usuario INNER JOIN
                PLA_DEPARTAMENTOS ON Usuario.CodDepto = PLA_DEPARTAMENTOS.IdDeptos INNER JOIN
                F_01 ON Usuario.UsuarioCod = F_01.CreadoPor ON F_04.NumFactura = F_01.NumAvPg INNER JOIN
                FC_03 ON F_03.DNI = FC_03.DNI
                WHERE        (F_03.ReciboAnulado = 0) AND (F_03.FechaRecibo BETWEEN ? AND ?) AND (PLA_DEPARTAMENTOS.IdDeptos = 2) AND (F_01.AvPgTipoImpuesto = 4)
                GROUP BY F_03.FechaRecibo
                ORDER BY F_03.FechaRecibo
            """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini,  fecha_fin,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_diario_uma(self, fecha_ini: str, fecha_fin: str):
        query = """SELECT F_03.FechaRecibo,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso,  1, 9) = '125990241' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS LicenciasExtranccion,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso,  1, 8) = '11740106' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS BosquesDerivados,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso,  1, 9) = '125990105' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS TasaAmbiental,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso,  1, 9) = '125990258' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS MatriculaMotoSierra,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso,  1, 9) = '125990242' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS PerforacionPozos,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso,  1, 9) = '125990220' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Constancias,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso,  1, 9) = '125990207' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Inspeccion,
                    cast(SUM(F_04.ValorUnitReciboDet) as float) AS TotalReciboPagado
                    FROM F_03 INNER JOIN
                    F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
                    Usuario INNER JOIN
                    PLA_DEPARTAMENTOS ON Usuario.CodDepto = PLA_DEPARTAMENTOS.IdDeptos INNER JOIN
                    F_01 ON Usuario.UsuarioCod = F_01.CreadoPor ON F_04.NumFactura = F_01.NumAvPg INNER JOIN
                    FC_03 ON F_03.DNI = FC_03.DNI
                    WHERE (F_03.ReciboAnulado = 0) AND (F_03.FechaRecibo BETWEEN ? AND ?) AND (PLA_DEPARTAMENTOS.IdDeptos = 3)
                    GROUP BY F_03.FechaRecibo
                    ORDER BY F_03.FechaRecibo
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini,  fecha_fin,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_diario_secretaria(self, fecha_ini: str, fecha_fin: str):
        query = """SELECT F_03.FechaRecibo,
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990201' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Matrimonios, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990220' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Constancias, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990221' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Certificaciones, 
                CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990222' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS VistosBuenos, 
                CAST(SUM(F_04.ValorUnitReciboDet) AS float) AS TotalReciboPagado
                FROM F_03 INNER JOIN
                F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
                Usuario INNER JOIN
                PLA_DEPARTAMENTOS ON Usuario.CodDepto = PLA_DEPARTAMENTOS.IdDeptos INNER JOIN
                F_01 ON Usuario.UsuarioCod = F_01.CreadoPor ON F_04.NumFactura = F_01.NumAvPg INNER JOIN
                FC_03 ON F_03.DNI = FC_03.DNI
                WHERE        (F_03.ReciboAnulado = 0) AND (F_03.FechaRecibo BETWEEN ? AND ?) AND (PLA_DEPARTAMENTOS.IdDeptos = 6)
                GROUP BY F_03.FechaRecibo
                ORDER BY F_03.FechaRecibo
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini,  fecha_fin,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_diario_urbanizacion(self, fecha_ini: str, fecha_fin: str):
        query = """SELECT F_03.FechaRecibo,
            CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990222' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Autorizaciones, 
            CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990225' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS LicenciaEjercer,
            CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990234' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS PermisoConstrir,
            CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990238' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS ConstrucccionAntenas,
            CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990205' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Rotulos,
            CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990220' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Constancias,
            CAST(SUM(F_04.ValorUnitReciboDet) AS FLOAT ) AS Totalrecibo 
            FROM F_03 INNER JOIN
            F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
            Usuario INNER JOIN
            PLA_DEPARTAMENTOS ON Usuario.CodDepto = PLA_DEPARTAMENTOS.IdDeptos INNER JOIN
            F_01 ON Usuario.UsuarioCod = F_01.CreadoPor ON F_04.NumFactura = F_01.NumAvPg INNER JOIN
            FC_03 ON F_03.DNI = FC_03.DNI
            WHERE        (F_03.ReciboAnulado = 0) AND (F_03.FechaRecibo BETWEEN ? AND ?) AND (PLA_DEPARTAMENTOS.IdDeptos = 8) 
            GROUP BY F_03.FechaRecibo
            ORDER BY F_03.FechaRecibo"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini,  fecha_fin,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_diario_justicia(self, fecha_ini: str, fecha_fin: str):
        query = """SELECT F_03.FechaRecibo,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990222' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Autorizaciones, 
                    CAST(SUM(CASE WHEN F_04.CtaIngreso = '12599022201' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS CartasVenta, 
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990244' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS GuiasTransporte, 
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990239' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS ForjarFierro,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990252' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS MatriculaFierro,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990257' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS MatriculaArmas,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990224' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Buhunero,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 7) = '1521997' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS InscripcionArrendamiento,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990220' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS Constancias,
                    CAST(SUM(F_04.ValorUnitReciboDet) AS FLOAT ) AS Totalrecibo 
                    FROM F_03 INNER JOIN
                    F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
                    Usuario INNER JOIN
                    PLA_DEPARTAMENTOS ON Usuario.CodDepto = PLA_DEPARTAMENTOS.IdDeptos INNER JOIN
                    F_01 ON Usuario.UsuarioCod = F_01.CreadoPor ON F_04.NumFactura = F_01.NumAvPg INNER JOIN
                    FC_03 ON F_03.DNI = FC_03.DNI
                    WHERE        (F_03.ReciboAnulado = 0) AND (F_03.FechaRecibo BETWEEN ? AND ?) AND (PLA_DEPARTAMENTOS.IdDeptos = 4) 
                    GROUP BY F_03.FechaRecibo
                    ORDER BY F_03.FechaRecibo
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini,  fecha_fin,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_diario_procamut(self, fecha_ini: str, fecha_fin: str):
        query = """SELECT F_03.FechaRecibo,
                    CAST(SUM(CASE WHEN substring(F_04.CtaIngreso, 1, 9) = '125990101' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS FLOAT) AS RastroMunicipal, 
                    CAST(SUM(F_04.ValorUnitReciboDet) AS FLOAT ) AS Totalrecibo 
                    FROM F_03 INNER JOIN
                    F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
                    Usuario INNER JOIN
                    PLA_DEPARTAMENTOS ON Usuario.CodDepto = PLA_DEPARTAMENTOS.IdDeptos INNER JOIN
                    F_01 ON Usuario.UsuarioCod = F_01.CreadoPor ON F_04.NumFactura = F_01.NumAvPg INNER JOIN
                    FC_03 ON F_03.DNI = FC_03.DNI
                    WHERE        (F_03.ReciboAnulado = 0) AND (F_03.FechaRecibo BETWEEN ? AND ?) AND (PLA_DEPARTAMENTOS.IdDeptos = 7) 
                    GROUP BY F_03.FechaRecibo
                    ORDER BY F_03.FechaRecibo
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini,  fecha_fin,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
