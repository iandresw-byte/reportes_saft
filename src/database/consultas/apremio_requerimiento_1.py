

CONSULTA_APREMIO_SAMI_NAT= """
SELECT top (?) 
    FC_03.DNI,
    FC_03.Pnombre,FC_03.SNombre, FC_03.PApellido,FC_03.SApellido, FC_03.Direccion,
    STUFF((SELECT DISTINCT ', ' + F2.ClaveCatastro FROM F_01 F1_2
            INNER JOIN F_02 F2 ON F1_2.NumAvPg = F2.NumAvPg
            WHERE F1_2.DNI = FC_03.DNI
            AND F1_2.AvPgEstado = 1
            AND F1_2.FechaVenceAvPg < ?
            AND F1_2.AvPgTipoImpuesto LIKE ?
            FOR XML PATH(''), TYPE
            ).value('.', 'VARCHAR(MAX)'), 1, 2, '') AS ClavesCatastro,
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
FROM F_01 INNER JOIN
    FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
    F_02 ON F_01.NumAvPg = F_02.NumAvPg
WHERE F_01.AvPgEstado = 1
    AND F_01.FechaVenceAvPg <  ?
    AND F_01.AvPgTipoImpuesto LIKE ?
    AND FC_03.Tipo LIKE ?
    AND FC_03.CodAldea LIKE ?
    AND FC_03.CodBarrio LIKE ?
    AND FC_03.DNI LIKE ?
    AND NOT EXISTS (
    SELECT 1
    FROM ApremioEnDoc A
    WHERE A.Identidad = FC_03.DNI
        AND  (A.TipoImpuesto = F_01.AvPgTipoImpuesto)
        AND  (Estado <> 'Anulado')
        )
GROUP BY  FC_03.DNI, FC_03.Pnombre, FC_03.SNombre, FC_03.PApellido, FC_03.SApellido, FC_03.Direccion
HAVING CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  > ?
ORDER BY  FC_03.DNI
"""

CONSULTA_APREMIO_GOB_ICS_X_NAT = """
        SELECT top  (?) FC_03.DNI,
            FC_03.Pnombre,FC_03.SNombre, FC_03.PApellido,FC_03.SApellido, FC_03.Direccion,
                                STUFF((
                SELECT DISTINCT ', ' + F2.ClaveCatastro
                FROM F_01 F1_2
                    INNER JOIN F_02 F2 ON F1_2.NumAvPg = F2.NumAvPg
                WHERE F1_2.DNI = FC_03.DNI
                    AND F1_2.AvPgEstado = 1
                    AND F1_2.FechaVenceAvPg < ?
                    AND F1_2.AvPgTipoImpuesto LIKE ?
                FOR XML PATH(''), TYPE
            ).value('.', 'VARCHAR(MAX)'), 1, 2, '') AS ClavesCatastro,
            min(F_01.FechaVenceAvPg) mes_ini,
            max(F_01.FechaVenceAvPg) mes_fin,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111111' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ip,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111112' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ic,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111113' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS com,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111114' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ser,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111110' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS bi,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111118' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS servicios,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111116' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS pecuario,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111119' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS tasas,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112120' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS multas,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112121' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recargos,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112122' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacion,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112123' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionSp,
            CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112126' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS intereses,
            CAST(SUM(F_02.ValorUnitAvPgDet ) AS FLOAT) AS total
        FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
            F_02 ON F_01.NumAvPg = F_02.NumAvPg
        WHERE (F_01.AvPgEstado = 1) AND 
            (F_01.FechaVenceAvPg < GETDATE()) AND 
            (F_01.AvPgTipoImpuesto in (2,3)) AND
            (FC_03.CodAldea LIKE ?) AND 
            (FC_03.CodBarrio LIKE ?) AND
            (FC_03.DNI LIKE ?) AND
            (NOT EXISTS (SELECT 1 AS Expr1 FROM ApremioEnDoc AS A  
            WHERE (Identidad = FC_03.DNI) AND 
            (TipoImpuesto = F_01.AvPgTipoImpuesto)
            AND  (Estado <> 'Anulado')))

        GROUP BY  FC_03.DNI, FC_03.Pnombre,FC_03.SNombre, FC_03.PApellido,FC_03.SApellido, FC_03.Direccion
        HAVING CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  > ?
        ORDER BY  FC_03.DNI 
"""

CONSULTA_APREMIO_SAMI_ICS_X_NAT = """
        SELECT top  (?) FC_03.DNI,
            FC_03.Pnombre,FC_03.SNombre, FC_03.PApellido,FC_03.SApellido, FC_03.Direccion,
                                STUFF((
                SELECT DISTINCT ', ' + F2.ClaveCatastro
                FROM F_01 F1_2
                    INNER JOIN F_02 F2 ON F1_2.NumAvPg = F2.NumAvPg
                WHERE F1_2.DNI = FC_03.DNI
                    AND F1_2.AvPgEstado = 1
                    AND F1_2.FechaVenceAvPg < ?
                    AND F1_2.AvPgTipoImpuesto LIKE ?
                FOR XML PATH(''), TYPE
            ).value('.', 'VARCHAR(MAX)'), 1, 2, '') AS ClavesCatastro,
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
        FROM F_01 INNER JOIN
            FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
            F_02 ON F_01.NumAvPg = F_02.NumAvPg
        WHERE (F_01.AvPgEstado = 1) AND 
            (F_01.FechaVenceAvPg < GETDATE()) AND 
            (F_01.AvPgTipoImpuesto in (2,3)) AND
            (FC_03.CodAldea LIKE ?) AND 
            (FC_03.CodBarrio LIKE ?) AND
            (FC_03.DNI LIKE ?) AND
            (NOT EXISTS (SELECT 1 AS Expr1 FROM ApremioEnDoc AS A  
            WHERE (Identidad = FC_03.DNI) AND 
            (TipoImpuesto = F_01.AvPgTipoImpuesto)
            AND  (Estado <> 'Anulado')))

        GROUP BY  FC_03.DNI, FC_03.Pnombre,FC_03.SNombre, FC_03.PApellido,FC_03.SApellido, FC_03.Direccion
        HAVING CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  > ?
        ORDER BY  FC_03.DNI 
"""

CONSULTA_APREMIO_GOB_ICS_JUR =""" 
                        SELECT  TOP  (?) FC_03_1.DNI, 
                        FC_03_1.Pnombre, FC_03_1.SNombre, FC_03_1.PApellido, FC_03_1.SApellido, FC_03.Direccion,
                                            STUFF((
                            SELECT DISTINCT ', ' + F2.ClaveCatastro
                            FROM F_01 F1_2
                                INNER JOIN F_02 F2 ON F1_2.NumAvPg = F2.NumAvPg
                            WHERE F1_2.DNI = FC_03.DNI
                                AND F1_2.AvPgEstado = 1
                                AND F1_2.FechaVenceAvPg < ?
                                AND F1_2.AvPgTipoImpuesto LIKE ?
                            FOR XML PATH(''), TYPE
                        ).value('.', 'VARCHAR(MAX)'), 1, 2, '') AS ClavesCatastro,
                        MIN(F_01.FechaVenceAvPg) AS mes_ini, 
                        MAX(F_01.FechaVenceAvPg) AS mes_fin, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111110' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS bi, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111111' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ip, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111112' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ic, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111113' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS com, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111114' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS ser, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111118' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS servicios, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111116' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS pecuario, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '111119' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS tasas, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112120' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS multas, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112121' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recargos, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112122' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacion, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6)  = '112123' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS recuperacionSp, 
                        CAST(SUM(CASE WHEN substring(F_02.CtaIngreso, 1, 6) = '112126' THEN F_02.ValorUnitAvPgDet ELSE 0 END) AS FLOAT) AS intereses, 
                        CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS total 
                    FROM  F_01 INNER JOIN
                        FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                        F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                        FC_03 AS FC_03_1 ON FC_03.IdRepresentante = FC_03_1.DNI
                    WHERE (F_01.AvPgEstado = 1) AND 
                        (F_01.FechaVenceAvPg < ? AND 
                        (F_01.AvPgTipoImpuesto in (2,3)) AND 
                        (FC_03.CodAldea LIKE ?) AND 
                        (FC_03.CodBarrio LIKE ?) AND
                        (FC_03.DNI LIKE ?) AND
                        (NOT EXISTS (SELECT 1 AS Expr1 FROM ApremioEnDoc AS A  WHERE (Identidad = FC_03.DNI) AND (TipoImpuesto = F_01.AvPgTipoImpuesto) AND (Estado <> 'Anulado')))
                    
                    GROUP BY FC_03.DNI, FC_03_1.DNI, FC_03_1.Pnombre, FC_03_1.SNombre, FC_03_1.PApellido, FC_03_1.SApellido, FC_03.Direccion
                    HAVING CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  > ?
                    ORDER BY FC_03.DNI
            """

CONSULTA_APREMIO_SAMI_ICS_JUR =""" 
                        SELECT  TOP  (?) FC_03_1.DNI, 
                        FC_03_1.Pnombre, FC_03_1.SNombre, FC_03_1.PApellido, FC_03_1.SApellido, FC_03.Direccion,
                                            STUFF((
                            SELECT DISTINCT ', ' + F2.ClaveCatastro
                            FROM F_01 F1_2
                                INNER JOIN F_02 F2 ON F1_2.NumAvPg = F2.NumAvPg
                            WHERE F1_2.DNI = FC_03.DNI
                                AND F1_2.AvPgEstado = 1
                                AND F1_2.FechaVenceAvPg < ?
                                AND F1_2.AvPgTipoImpuesto LIKE ?
                            FOR XML PATH(''), TYPE
                        ).value('.', 'VARCHAR(MAX)'), 1, 2, '') AS ClavesCatastro,
                        MIN(F_01.FechaVenceAvPg) AS mes_ini, 
                        MAX(F_01.FechaVenceAvPg) AS mes_fin, 
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
                        CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT) AS total 
                    FROM  F_01 INNER JOIN
                        FC_03 ON F_01.DNI = FC_03.DNI INNER JOIN
                        F_02 ON F_01.NumAvPg = F_02.NumAvPg INNER JOIN
                        FC_03 AS FC_03_1 ON FC_03.IdRepresentante = FC_03_1.DNI
                    WHERE (F_01.AvPgEstado = 1) AND 
                        (F_01.FechaVenceAvPg < ? AND 
                        (F_01.AvPgTipoImpuesto in (2,3)) AND 
                        (FC_03.CodAldea LIKE ?) AND 
                        (FC_03.CodBarrio LIKE ?) AND
                        (FC_03.DNI LIKE ?) AND
                        (NOT EXISTS (SELECT 1 AS Expr1 FROM ApremioEnDoc AS A  WHERE (Identidad = FC_03.DNI) AND (TipoImpuesto = F_01.AvPgTipoImpuesto) AND (Estado <> 'Anulado')))
                    
                    GROUP BY FC_03.DNI, FC_03_1.DNI, FC_03_1.Pnombre, FC_03_1.SNombre, FC_03_1.PApellido, FC_03_1.SApellido, FC_03.Direccion
                    HAVING CAST(SUM(F_02.ValorUnitAvPgDet) AS FLOAT)  > ?
                    ORDER BY FC_03.DNI
            """