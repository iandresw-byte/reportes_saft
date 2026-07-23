SERVICIOS_PUBLICOS_INICIO_TOP ="""
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
    STUFF((SELECT DISTINCT ', ' + F2.ClaveCatastro FROM F_01 F1_2
            INNER JOIN F_02 F2 ON F1_2.NumAvPg = F2.NumAvPg
            WHERE F1_2.DNI = FC_03.DNI
            AND F1_2.AvPgEstado = 1
            AND F1_2.FechaVenceAvPg <  @FechaVenceAvPg
            AND F1_2.AvPgTipoImpuesto LIKE 1
            and F2.ClaveCatastro is not null
            FOR XML PATH(''), TYPE
            ).value('.', 'VARCHAR(MAX)'), 1, 2, '') AS ClavesCatastro,
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
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111801' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS agua,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111802' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS alcantarillado,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111803' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS alumbrado,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111804' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS tren,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111805' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS conexiones,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111806' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS bomberos,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111807' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS rastro,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111808' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS trasporte_carme,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111809' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS balanza,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111810' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS limpieza_solares,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111811' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS aseo_parques_ave,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111812' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS limpieza_cementerio,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111813' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS servicios_secretaria,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111814' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS muellaje,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111815' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS turismo,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111816' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS seguridad,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111820' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS tasa_ambiental,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 8) = '11111899' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS otros_servicios,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111119' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS tasas,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112120' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS multas,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112121' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recargos,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112122' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacion,
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
    AND F_01.AvPgTipoImpuesto = 5
    AND FC_03.Tipo LIKE @Tipo
    AND FC_03.CodAldea LIKE @CodAldea
    AND FC_03.CodBarrio LIKE @CodBarrio
    AND FC_03.DNI LIKE @DNI
    AND NOT EXISTS (
    SELECT 1
    FROM ApremioEnDoc A
    WHERE A.Identidad = FC_03.DNI
        AND  (A.TipoImpuesto = F_01.AvPgTipoImpuesto)
        AND  (Estado <> 'Anulado')
        )
GROUP BY  FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion, FC_03.CodBarrio, FC_03.CodAldea
HAVING CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  > @ValorUnitAvPgDet
ORDER BY  FC_03.DNI
    """

