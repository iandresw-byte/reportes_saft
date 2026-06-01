class EstratificacionRepository:
    def __init__(self, conexion) -> None:
        self.conexion = conexion

    def estratificacion(self, val_minimo: float, val_maximo: float, periodo: int) -> list[dict]:
        query = """ SELECT     FC_03.DNI AS rtm, FC_03.Pnombre AS nombreComercial, FC_03.RTN, CuentaIngreso_A.NombreCtaIngreso AS Actividad, FC_03.Direccion, FC_03.Constitucion, FC_03.FechaNac AS FechaInicio, 
                    cast(DeclaraContJurid.ProdNoReg + DeclaraContJurid.ProdReg + DeclaraContJurid.ProdExento AS FLOAT) AS val_declarado, DeclaraContJurid.Periodo AS utlAnioDeclarado
                    FROM         FC_03 INNER JOIN
                    DeclaraContJurid ON FC_03.DNI = DeclaraContJurid.Identidad INNER JOIN
                    CuentaIngreso_A ON FC_03.CodProfesion = CuentaIngreso_A.CtaIngreso AND DeclaraContJurid.Periodo = CuentaIngreso_A.Anio
                    WHERE     (cast(DeclaraContJurid.ProdNoReg + DeclaraContJurid.ProdReg + DeclaraContJurid.ProdExento AS FLOAT) BETWEEN ? AND ?) AND (DeclaraContJurid.EstadoDeclaraIC <> 2) AND 
                    (DeclaraContJurid.Periodo LIKE ?)
                    GROUP BY FC_03.DNI, FC_03.Pnombre, FC_03.RTN, CuentaIngreso_A.NombreCtaIngreso, FC_03.Direccion, FC_03.Constitucion, FC_03.FechaNac, DeclaraContJurid.ProdNoReg, DeclaraContJurid.ProdReg, 
                    DeclaraContJurid.ProdExento, DeclaraContJurid.Periodo
                    ORDER BY nombreComercial"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (val_minimo, val_maximo, f'%{periodo}%'))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
