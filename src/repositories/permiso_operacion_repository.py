class PermisoOperacionReposirory:
    def __init__(self, conexion) -> None:
        self.conexion = conexion

    def existe_recibo(self, num_recibo: int) -> bool:
        query = "SELECT COUNT(*) as Total FROM Tra_PermOP WHERE NumRecibo = ?"
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_recibo,))
            row = cur.fetchone()
            if not row:
                return False
            return row[0] > 0

    def recargar_datos(self, num_recibo: int):
        query = """
            SELECT Tra_PermOP.NumRecibo, Tra_PermOP.Identidad, Tra_PermOP.NoPermiso,  FC_03.Direccion,  FC_03.IdRepresentante, Tra_PermOP.Periodo, Tra_PermOP.Negocio, Tra_PermOP.Propietario,
                Tra_PermOP.Ubicacion, Tra_PermOP.Actividad, Tra_PermOP.Usuario, Tra_PermOP.FirmaJ , Tra_PermOP.UsuarioMod, FC_03.CodProfesion, FC_03.FechaNac, FC_03.ClaveCatastro, Tra_PermOP.Observacion,
                FC_03.rtn, Tra_PermOP.CodAldea, FC_03.idrepresentante , FC_03.Telefono , Tra_PermOP.Fecha,  Tra_PermOP.HorarioAlcohol
            FROM Tra_PermOP INNER JOIN 
            FC_03 ON Tra_PermOP.Identidad = FC_03.DNI 
            WHERE  Tra_PermOP.NumRecibo = ?
        
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_recibo,))
            row = cur.fetchone()
            if not row:
                return []
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_datos(self, num_recibo: int):
        query = """
         SELECT F_04.NumRecibo, F_01.DNI, FC_03.Direccion, FC_03.IdRepresentante, FC_03.rtn,
             FC_03_1.Pnombre, FC_03_1.SNombre, FC_03_1.PApellido, FC_03_1.SApellido, 
             CuentaIngreso_A.NombreCtaIngreso, FC_03.CodProfesion, FC_03.FechaNac, FC_03.Pnombre AS Negocio, FC_03.ClaveCatastro , FC_03.Telefono , FC_03.UltPeriodoFact, FC_03.CodAldea
             FROM F_01 INNER JOIN F_04 ON F_01.NumAvPg = F_04.NumFactura 
             INNER JOIN FC_03 ON F_01.DNI = FC_03.DNI 
             INNER JOIN FC_03 AS FC_03_1 ON FC_03.IdRepresentante = FC_03_1.DNI 
             INNER JOIN CuentaIngreso_A ON FC_03.CodProfesion = CuentaIngreso_A.CtaIngreso AND FC_03.UltPeriodoFact = CuentaIngreso_A.Anio
             WHERE (F_04.NumRecibo = ?) AND (F_01.AvPgTipoImpuesto IN (0,2,3,7))
             GROUP BY F_04.NumRecibo, F_01.DNI, FC_03.Direccion, FC_03.IdRepresentante, FC_03.rtn, 
             FC_03_1.Pnombre, FC_03_1.SNombre, FC_03_1.PApellido, FC_03_1.SApellido, 
             CuentaIngreso_A.NombreCtaIngreso, FC_03.CodProfesion, FC_03.FechaNac, FC_03.Pnombre, FC_03.ClaveCatastro, FC_03.Telefono, FC_03.UltPeriodoFact, FC_03.CodAldea 

        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_recibo,))
            row = cur.fetchone()
            if not row:
                return []
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_num_po(self,):
        query1 = f"""SELECT UltNumPO FROM ParametroCont;
        """
        query2 = f"""SELECT COUNT(NoPermiso) AS UltNumPO FROM Tra_PermOP"""
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query1)
                row = cur.fetchone()
                if not row:
                    return []
                return int(row[0])+1
        except Exception as e:
            try:
                with self.conexion.cursor() as cur:
                    cur.execute(query2)
                    row = cur.fetchone()
                    if not row:
                        return []
                    columns = [column[0] for column in cur.description]
                    return dict(zip(columns, row))
            except Exception as e2:
                return []  # En caso de fallo total, datos vacíos

    def update_ult_po(self, ult_num_po: int) -> bool:
        query = "UPDATE ParametroCont SET  UltNumPO = ?"
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query, (ult_num_po,))
                return True
        except Exception as e:
            return False

    def insertar_tra_perm_ope(self, NoPermiso, Periodo, Identidad, Negocio, Propietario, Ubicacion, Actividad,  Observacion,  Fecha, CodAldea, NumRecibo, FirmaJ, Usuario, horario):
        query = """INSERT INTO Tra_PermOP (NoPermiso, Periodo, Identidad, Negocio, Propietario, Ubicacion, Actividad,  Observacion,  Fecha, CodAldea, NumRecibo, FirmaJ, Usuario, HorarioAlcohol) 
        VALUES (?, ?, ?, ?, ?, ?, ?,  ?,  ?, ?, ?, ?, ?, ?) """
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query, (NoPermiso, Periodo, Identidad, Negocio, Propietario,
                            Ubicacion, Actividad,  Observacion,  Fecha, CodAldea, NumRecibo, FirmaJ, Usuario, horario))
            self.update_ult_po(NoPermiso)
            return True

        except Exception as e:
            return False

    def insertar_horario_alcohol(self, horario):
        query = """INSERT INTO Tra_PerOpeHoraAlch (codPerOpe, horaApeDomJue, horaCieDomJue, horaApeVierSab, horaCieVierSab, horaApeFestivo, horaCieFestivo) 
        VALUES (?, ?, ?, ?, ?, ?, ?) """
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query, horario)
                return True
        except Exception as e:
            return False

    def get_horario_alcohol(self, cod_permiso):
        query = """SELECT  codPerOpe, horaApeDomJue, horaCieDomJue, horaApeVierSab, horaCieVierSab, horaApeFestivo, horaCieFestivo FROM Tra_PerOpeHoraAlch WHERE codPerOpe = ?   """
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query, (cod_permiso,))
                return True
        except Exception as e:
            return False

    def reporte_permisos_operacion(self, fecha_ini: str, fecha_fin: str, cod_aldea: str, cod_barrio: str, tipo_permiso: str):
        query = """
            SELECT        Tra_PermOP.Identidad, Tra_PermOP.Negocio, Tra_PermOP.Propietario, Tra_PermOP.Ubicacion, CONVERT(VARCHAR(20), Tra_PermOP.Fecha, 103) AS Fecha, Tra_PermOP.Actividad, Tra_PermOP.Observacion, 
            CAST(Tra_PermOP.NoPermiso AS INT) AS NoPermiso, CAST(F_04.ValorUnitReciboDet AS FLOAT) AS ValorUnitReciboDet, F_03.NumRecibo, Aldea.NombreAldea, TablaBarrio.NombreBarrio, Tra_PermOP.Periodo
            FROM            Tra_PermOP INNER JOIN
            F_03 ON Tra_PermOP.NumRecibo = F_03.NumRecibo INNER JOIN
            F_04 ON F_03.NumRecibo = F_04.NumRecibo INNER JOIN
            FC_03 ON F_03.DNI = FC_03.DNI INNER JOIN
            TablaBarrio ON FC_03.CodBarrio = TablaBarrio.CodBarrio INNER JOIN
            Aldea ON FC_03.CodAldea = Aldea.CodAldea INNER JOIN
            F_01 ON F_04.NumFactura = F_01.NumAvPg AND FC_03.DNI = F_01.DNI AND Tra_PermOP.Periodo = YEAR(F_01.FechaVenceAvPg)
            WHERE        (Tra_PermOP.Fecha BETWEEN ? AND ?) AND (SUBSTRING(F_04.CtaIngreso, 1, 8) IN ('11111921', '12599023')) AND (Tra_PermOP.Observacion LIKE ?) AND (FC_03.CodAldea LIKE ?) AND 
            (FC_03.CodBarrio LIKE ?)
            ORDER BY Fecha, NoPermiso
            """

        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini, fecha_fin,
                        f"{tipo_permiso}", f"{cod_aldea}", f"{cod_barrio}"))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def reporte_permisos_operacion_cta(self, fecha_ini: str, fecha_fin: str, cod_aldea: str, cod_barrio: str):
        query = """
                SELECT        F_03.DNI as Identidad, FC_03.Pnombre AS Negocio, FC_03_1.Pnombre + ' ' + FC_03_1.SNombre + ' ' + FC_03_1.PApellido + ' ' + FC_03_1.SApellido AS Propietario, FC_03.Direccion AS Ubicacion, CONVERT(VARCHAR(20), F_03.FechaRecibo, 
                103) AS Fecha, CuentaIngreso_A.NombreCtaIngreso AS Actividad, '' AS Observacion, '' AS NoPermiso, CAST(F_04.ValorUnitReciboDet AS FLOAT) AS ValorUnitReciboDet, F_03.NumRecibo, Aldea.NombreAldea, 
                TablaBarrio.NombreBarrio, FC_03.UltPeriodoFact AS Periodo
                FROM            F_04 INNER JOIN
                F_03 ON F_04.NumRecibo = F_03.NumRecibo INNER JOIN
                FC_03 ON F_03.DNI = FC_03.DNI INNER JOIN
                CuentaIngreso_A ON FC_03.CodProfesion = CuentaIngreso_A.CtaIngreso AND FC_03.UltPeriodoFact = CuentaIngreso_A.Anio INNER JOIN
                FC_03 AS FC_03_1 ON FC_03.IdRepresentante = FC_03_1.DNI INNER JOIN
                TablaBarrio ON FC_03.CodBarrio = TablaBarrio.CodBarrio INNER JOIN
                Aldea ON FC_03.CodAldea = Aldea.CodAldea AND TablaBarrio.CodAldea = Aldea.CodAldea
                WHERE   (SUBSTRING(F_04.CtaIngreso, 1, 8) IN ('11111921', '12599023')) AND (F_03.ReciboAnulado = 0) AND (F_03.FechaRecibo BETWEEN ? AND ?)  AND (FC_03.CodAldea LIKE ?) AND 
            (FC_03.CodBarrio LIKE ?)
                GROUP BY F_03.DNI, FC_03.Pnombre, FC_03_1.Pnombre + ' ' + FC_03_1.SNombre + ' ' + FC_03_1.PApellido + ' ' + FC_03_1.SApellido, FC_03.Direccion, CONVERT(VARCHAR(20), F_03.FechaRecibo, 103), 
                CuentaIngreso_A.NombreCtaIngreso, CAST(F_04.ValorUnitReciboDet AS FLOAT), F_03.NumRecibo, Aldea.NombreAldea, TablaBarrio.NombreBarrio, FC_03.UltPeriodoFact
"""

        with self.conexion.cursor() as cur:
            cur.execute(query, (fecha_ini, fecha_fin,
                                f"{cod_aldea}", f"{cod_barrio}"))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
