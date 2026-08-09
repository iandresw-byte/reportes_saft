BIENES_INMUEBLES_INICIO_TOP_GOB_AVISO ="""
DECLARE @Cantidad_filas INT = ?
DECLARE @FechaVenceAvPg DATE = ?
DECLARE @AvPgTipoImpuesto VARCHAR(1) =?
DECLARE @Tipo VARCHAR(1) = ?
DECLARE @CodBarrio VARCHAR(9) = ?
DECLARE @CodAldea VARCHAR(6) =?
DECLARE @DNI VARCHAR(50) = ?
DECLARE @ValorUnitAvPgDet FLOAT = ?

SELECT top (@Cantidad_filas) 
    FC_01.DNI,
    FC_03.Pnombre,FC_03.SNombre, FC_03.PApellido,FC_03.SApellido, FC_01.Direccion,
    FC_01.CodBarrio,
    FC_01.CodAldea,
    FC_01.CatClv AS ClavesCatastro,
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
FROM         F_01 INNER JOIN
                         FC_01 ON F_01.ClaveCatastro = FC_01.CatClv INNER JOIN
                         F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                         FC_03 ON F_01.DNI = FC_03.DNI AND FC_01.DNI = FC_03.DNI

WHERE F_01.AvPgEstado = 1

    AND F_01.AvPgTipoImpuesto = 1
    AND FC_03.Tipo LIKE  @Tipo
   AND FC_01.CodAldea LIKE @CodAldea
   AND FC_01.CodBarrio LIKE @CodBarrio
   AND FC_01.DNI LIKE @DNI
    AND NOT EXISTS (
    SELECT 1
    FROM ApremioEnDoc A
    WHERE A.Identidad = FC_01.CatClv
        AND  (A.TipoImpuesto = F_01.AvPgTipoImpuesto)
        AND  (Estado <> 'Anulado')
        )
GROUP BY  FC_01.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_01.Direccion, FC_01.CodBarrio, FC_01.CodAldea, FC_01.CatClv 
HAVING CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  > @ValorUnitAvPgDet
ORDER BY  FC_01.CatClv
    """



BIENES_INMUEBLES_INICIO_TOP_GOB ="""
DECLARE @Cantidad_filas INT = ?
DECLARE @FechaVenceAvPg DATE = ?
DECLARE @AvPgTipoImpuesto VARCHAR(1) =?
DECLARE @Tipo VARCHAR(1) = ?
DECLARE @CodBarrio VARCHAR(9) = ?
DECLARE @CodAldea VARCHAR(6) =?
DECLARE @DNI VARCHAR(50) = ?
DECLARE @ValorUnitAvPgDet FLOAT = ?

SELECT top (@Cantidad_filas) 
    FC_01.DNI,
    FC_03.Pnombre,FC_03.SNombre, FC_03.PApellido,FC_03.SApellido, FC_01.Direccion,
    FC_01.CodBarrio,
    FC_01.CodAldea,
    FC_01.CatClv AS ClavesCatastro,
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
FROM         F_01 INNER JOIN
                         FC_01 ON F_01.ClaveCatastro = FC_01.CatClv INNER JOIN
                         F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                         FC_03 ON F_01.DNI = FC_03.DNI AND FC_01.DNI = FC_03.DNI

WHERE F_01.AvPgEstado = 1
  AND F_01.FechaVenceAvPg <  @FechaVenceAvPg
    AND F_01.AvPgTipoImpuesto = 1
    AND FC_03.Tipo LIKE  @Tipo
   AND FC_01.CodAldea LIKE @CodAldea
   AND FC_01.CodBarrio LIKE @CodBarrio
   AND FC_01.DNI LIKE @DNI
    AND NOT EXISTS (
    SELECT 1
    FROM ApremioEnDoc A
    WHERE A.Identidad = FC_01.CatClv
        AND  (A.TipoImpuesto = F_01.AvPgTipoImpuesto)
        AND  (Estado <> 'Anulado')
        )
GROUP BY  FC_01.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_01.Direccion, FC_01.CodBarrio, FC_01.CodAldea, FC_01.CatClv 
HAVING CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  > @ValorUnitAvPgDet
ORDER BY  FC_01.CatClv
    """



BIENES_INMUEBLES_INICIO_TOP_SAMI ="""
DECLARE @Cantidad_filas INT = ?
DECLARE @FechaVenceAvPg DATE = ?
DECLARE @AvPgTipoImpuesto VARCHAR(1) =?
DECLARE @Tipo VARCHAR(1) = ?
DECLARE @CodBarrio VARCHAR(9) = ?
DECLARE @CodAldea VARCHAR(6) =?
DECLARE @DNI VARCHAR(50) = ?
DECLARE @ValorUnitAvPgDet FLOAT = ?

SELECT top (@Cantidad_filas) 
    FC_01.DNI,
    FC_03.Pnombre,FC_03.SNombre, FC_03.PApellido,FC_03.SApellido, FC_01.Direccion,
    FC_01.CodBarrio,
    FC_01.CodAldea,
    FC_01.CatClv AS ClavesCatastro,
    min(F_01.FechaVenceAvPg) mes_ini,
    max(F_01.FechaVenceAvPg) mes_fin,
    CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '117101' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ic,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '117102' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS com,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '117103' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ser,
    
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '117201' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS bi_urb,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '117202' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS bi_ru,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '117301' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ip,
        
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '117401' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS extranccion,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '117501' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS pecuario,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '117601' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS telecomunicaciones,
    
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 7) = '1259901' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS tasas,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 7) = '1259902' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS derecos,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 7) = '1259903' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS multas,
    
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 7) = '1521902' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS servicios,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 7) = '1521996' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recargos_servicios,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 7) = '1521997' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS intereses_servicios,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 7) = '1521998' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacion_Servicios,
    
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) IN ('117196','117296','117396') THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recargos,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) IN ('117197','117297','117397')  THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS intereses,
        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) IN ('117198','117298','117398')  THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacion,
        CAST(SUM(F_02.ValorUnitAvPgDet ) AS FLOAT) AS total
FROM         F_01 INNER JOIN
                         FC_01 ON F_01.ClaveCatastro = FC_01.CatClv INNER JOIN
                         F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                         FC_03 ON F_01.DNI = FC_03.DNI AND FC_01.DNI = FC_03.DNI

WHERE F_01.AvPgEstado = 1
  AND F_01.FechaVenceAvPg <  @FechaVenceAvPg
    AND F_01.AvPgTipoImpuesto = 1
    AND FC_03.Tipo LIKE  @Tipo
   AND FC_01.CodAldea LIKE @CodAldea
   AND FC_01.CodBarrio LIKE @CodBarrio
   AND FC_01.DNI LIKE @DNI
    AND NOT EXISTS (
    SELECT 1
    FROM ApremioEnDoc A
    WHERE A.Identidad = FC_01.CatClv
        AND  (A.TipoImpuesto = F_01.AvPgTipoImpuesto)
        AND  (Estado <> 'Anulado')
        )
GROUP BY  FC_01.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_01.Direccion, FC_01.CodBarrio, FC_01.CodAldea, FC_01.CatClv 
HAVING CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  > @ValorUnitAvPgDet
ORDER BY  FC_01.CatClv
    """

