class SARReportesRepository:
    def __init__(self, conexion) -> None:
        self.conexion = conexion

    def declaraciones_sar(self, val_minimo: str,  periodo: str) -> list[dict]:
        val_minimo = val_minimo.replace(",", "")
        val_minimo = val_minimo.replace(".00", "")
        query = """
SELECT 
    FC_03.RTN,
    FC_03.DNI AS rtm,
    FC_03.Pnombre AS nombreComercial,
    '' AS NumPermiso,
    FC_03.UltPeriodoFact AS ultPeriodoUltPermiso,
    CuentaIngreso_A.NombreCtaIngreso AS Actividad,
    FC_03.Direccion,
    FC_03.Telefono,
    FC_03.Constitucion,
    FC_03.FechaNac AS FechaInicio,

    CAST(
        DeclaraContJurid.ProdNoReg 
      + DeclaraContJurid.ProdReg 
      + DeclaraContJurid.ProdExento 
    AS FLOAT) AS val_declarado,

    DeclaraContJurid.Periodo AS utlAnioDeclarado

FROM FC_03
INNER JOIN DeclaraContJurid 
    ON FC_03.DNI = DeclaraContJurid.Identidad
INNER JOIN CuentaIngreso_A 
    ON FC_03.CodProfesion = CuentaIngreso_A.CtaIngreso 
    AND DeclaraContJurid.Periodo = CuentaIngreso_A.Anio

WHERE 
    (DeclaraContJurid.ProdNoReg 
   + DeclaraContJurid.ProdReg 
   + DeclaraContJurid.ProdExento > ?)
    AND (DeclaraContJurid.EstadoDeclaraIC <> 2)
    AND (DeclaraContJurid.Periodo = ?)

GROUP BY 
    FC_03.DNI, FC_03.Pnombre, FC_03.RTN,
    CuentaIngreso_A.NombreCtaIngreso,
    FC_03.Direccion, FC_03.Constitucion,
    FC_03.FechaNac,
    DeclaraContJurid.ProdNoReg,
    DeclaraContJurid.ProdReg,
    DeclaraContJurid.ProdExento,
    DeclaraContJurid.Periodo,
    FC_03.Telefono,
    FC_03.UltPeriodoFact

ORDER BY val_declarado
"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (val_minimo, periodo))
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def declaraciones_sar_ip(self, val_minimo: str,  periodo: str) -> list[dict]:
        val_minimo = val_minimo.replace(",", "")
        val_minimo = val_minimo.replace(".00", "")
        query = """
SELECT 
    FC_03.RTN,
    FC_03.DNI AS rtm,
    FC_03.Pnombre AS nombreComercial,
    '' AS NumPermiso,
    FC_03.UltPeriodoFact AS ultPeriodoUltPermiso,
    CuentaIngreso_A.NombreCtaIngreso AS Actividad,
    FC_03.Direccion,
    FC_03.Telefono,
    FC_03.Constitucion,
    FC_03.FechaNac AS FechaInicio,

    CAST(
        DeclaraContJurid.ProdNoReg 
      + DeclaraContJurid.ProdReg 
      + DeclaraContJurid.ProdExento 
    AS FLOAT) AS val_declarado,

    DeclaraContJurid.Periodo AS utlAnioDeclarado

FROM FC_03
INNER JOIN DeclaraContJurid 
    ON FC_03.DNI = DeclaraContJurid.Identidad
INNER JOIN CuentaIngreso_A 
    ON FC_03.CodProfesion = CuentaIngreso_A.CtaIngreso 
    AND DeclaraContJurid.Periodo = CuentaIngreso_A.Anio

WHERE 
    (DeclaraContJurid.ProdNoReg 
   + DeclaraContJurid.ProdReg 
   + DeclaraContJurid.ProdExento > ?)
    AND (DeclaraContJurid.EstadoDeclaraIC <> 2)
    AND (DeclaraContJurid.Periodo = ?)

GROUP BY 
    FC_03.DNI, FC_03.Pnombre, FC_03.RTN,
    CuentaIngreso_A.NombreCtaIngreso,
    FC_03.Direccion, FC_03.Constitucion,
    FC_03.FechaNac,
    DeclaraContJurid.ProdNoReg,
    DeclaraContJurid.ProdReg,
    DeclaraContJurid.ProdExento,
    DeclaraContJurid.Periodo,
    FC_03.Telefono,
    FC_03.UltPeriodoFact

ORDER BY val_declarado
"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (val_minimo, periodo))
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
