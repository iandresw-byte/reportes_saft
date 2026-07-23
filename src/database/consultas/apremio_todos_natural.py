CONSULTA_APREMIO_GOB_NAT_TODOS= """
DECLARE @Cantidad_filas INT = ?
DECLARE @FechaVenceAvPg DATE = ?
DECLARE @AvPgTipoImpuesto VARCHAR(1) =?
DECLARE @Tipo VARCHAR(1) =?
DECLARE @CodBarrio VARCHAR(50) =  ?
DECLARE @CodAldea VARCHAR(50) =?
DECLARE @DNI VARCHAR(50) = ?
DECLARE @ValorUnitAvPgDet FLOAT = ?


SELECT top (@Cantidad_filas) 
    FC_03.DNI,
    FC_03.Pnombre,FC_03.SNombre, FC_03.PApellido,FC_03.SApellido, FC_03.Direccion,
    FC_03.CodBarrio, FC_03.CodAldea,
    F_02.ClaveCatastro  AS ClavesCatastro,
    min(F_01.FechaVenceAvPg) mes_ini,
    max(F_01.FechaVenceAvPg) mes_fin,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111110' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS bi,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111111' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ip,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111112' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ind,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111113' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS com,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111114' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ser,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111115' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS pecuario,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111116' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS extraccion,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111117' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS selectivo,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111118' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS servicios,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111119' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS tasas,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112120' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS multas,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112121' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recargos,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112122' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacion,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11212201' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionbi,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11212202' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionip,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11212203' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionind,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11212204' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacioncom,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11212205' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionser,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11212206' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionexctracion,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11212207' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionslectivo,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11212209' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionBillares,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11212210' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionTasas,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112123' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionSp,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112124' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionAl,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112125' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS alquileres,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112126' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS intereses,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112127' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS descuentos,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 3) in ('221','222','223','224') THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS otros_ingresos,
    CAST(SUM(F_02.ValorUnitAvPgDet ) AS FLOAT) AS total
FROM F_01 INNER JOIN
    FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
    F_02 ON F_01.NumAvPg = F_02.NumAvPg
WHERE F_01.AvPgEstado = 1
    AND F_01.FechaVenceAvPg <  @FechaVenceAvPg
    AND F_01.AvPgTipoImpuesto in (0,1,2,3,4,5,7)
    AND FC_03.Tipo LIKE  @Tipo
    AND FC_03.CodAldea LIKE @CodAldea
    AND FC_03.CodBarrio LIKE @CodBarrio
    AND FC_03.DNI LIKE @DNI
    AND NOT EXISTS (
    SELECT 1
    FROM ApremioEnDoc A
    WHERE A.Identidad = FC_03.DNI
        AND  (A.TipoImpuesto = 10)
        AND  (Estado <> 'Anulado')
        )
GROUP BY  FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion, F_02.ClaveCatastro, FC_03.CodBarrio, FC_03.CodAldea
HAVING CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  > @ValorUnitAvPgDet
ORDER BY  FC_03.DNI
"""