class ConstanciaRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def licecia_uma_ics(self, num_recibo):
        query = """
                    SELECT CAST(F_04.ValorUnitReciboDet AS  Float) AS ValorUnitReciboDet, F_04.CtaIngreso, FC_03.Tipo, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion, FC_03.DNI, FC_03.IdRepresentante
                    FROM F_04 INNER JOIN
                    F_03 ON F_04.NumRecibo = F_03.NumRecibo INNER JOIN
                    FC_03 ON F_03.DNI = FC_03.DNI
                    WHERE (F_04.NumRecibo = ?)
                    GROUP BY F_04.ValorUnitReciboDet, F_04.CtaIngreso, FC_03.Tipo, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion, FC_03.DNI, FC_03.IdRepresentante
                    HAVING        (F_04.CtaIngreso LIKE N'125990105%')
             """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_recibo))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def insertar_tasa_uma_ics(self, NoLicencia, Periodo, Identidad, Propietario, rtm, Negocio, Ubicacion, NoRecibo, FechaSolicitud, FechaVence):
        query = """ INSERT INTO Tra_LiceAmbiental (NoLicencia, Periodo, Identidad, Propietario, rtm, Negocio, Ubicacion, NoRecibo, FechaSolicitud, FechaVence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
             """
        with self.conexion.cursor() as cur:
            cur.execute(query, (NoLicencia, Periodo, Identidad, Propietario,
                        rtm, Negocio, Ubicacion, NoRecibo, FechaSolicitud, FechaVence))

    def update_tasa_uma_ics(self, NoLicencia, Periodo, Identidad, Propietario, rtm, Negocio, Ubicacion, NoRecibo, FechaSolicitud, FechaVence,IdPermiso):
            query = """ UPDATE Tra_LiceAmbiental 
                        SET NoLicencia = ?, Periodo= ?,Identidad= ?,Propietario= ?, rtm= ?, Negocio= ?, Ubicacion= ?, NoRecibo= ?, FechaSolicitud= ?, FechaVence= ?
                        WHERE IdPermiso = ?
                 """
            with self.conexion.cursor() as cur: 
                cur.execute(query, (NoLicencia, Periodo, Identidad, Propietario,
                            rtm, Negocio, Ubicacion, NoRecibo, FechaSolicitud, FechaVence, IdPermiso))

    def existe_recibo(self, num_recibo: int) -> bool:
        query = "SELECT COUNT(*) as Total FROM Tra_LiceAmbiental WHERE NoRecibo = ?"
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_recibo,))
            row = cur.fetchone()
            if not row:
                return False
            return row[0] > 0

    def licencia_numero(self,) -> int:
        query = "SELECT MAX(NoLicencia) AS Num_Licencia FROM Tra_LiceAmbiental"
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row[0]:
                return 1
            return int(row[0]) + 1

    def recargar_licencia(self, num_recibo: int):
        query = """
                SELECT IdPermiso, NoLicencia, Periodo, Identidad, Propietario, rtm, Negocio, Ubicacion, NoRecibo, FechaSolicitud, FechaVence
                FROM Tra_LiceAmbiental
                where NoRecibo = ?
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_recibo,))
            row = cur.fetchone()
            if not row:
                return []
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def get_propietario(self, dni):
        query = """SELECT * FROM  FC_03 WHERE (DNI = ?) """
        with self.conexion.cursor() as cur:
            cur.execute(query, (dni))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def get_establecimiento(self, id_representante):
        query = """SELECT * FROM  FC_03 WHERE (IdRepresentante = ?) """
        with self.conexion.cursor() as cur:
            cur.execute(query, (id_representante))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
