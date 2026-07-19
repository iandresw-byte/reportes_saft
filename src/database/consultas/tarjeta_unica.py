CONSULTA_REGISTRO_UNICO_GOB = """


SELECT  
F_03.NumRecibo, 
F_03.FechaRecibo, 
cast(SUM(F_04.ValorUnitReciboDet) as Float) AS ValorRecibo, 
F_03.DNI, 
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '111110' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS BienesInmuebles,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '111111' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS Personal,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '111112' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS Industria,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '111113' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS Comercio,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '111114' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS Servicio,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '111115' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS Pecuario,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '111116' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS ExtraccionRecursos,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '111117' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS Telecomunicaciones,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '111118' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS ServiciosPublicos,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '111119' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS TasasDerechos,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '112120' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS Multas,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '112121' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS Recargos,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '112122' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS RecuperacionImpuestos,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '112123' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS RecuperacionServicios,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '112124' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS RecuperacionRentas,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '112125' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS Rentas,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '112126' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS Intereses,
CAST(SUM(CASE WHEN SUBSTRING(F_04.CtaIngreso, 1, 6) = '112127' THEN F_04.ValorUnitReciboDet ELSE 0 END) AS float) AS Descuentos
FROM            F_04 INNER JOIN
                         F_03 ON F_04.NumRecibo = F_03.NumRecibo INNER JOIN
                         F_01 ON F_04.NumFactura = F_01.NumAvPg
WHERE        (F_03.ReciboAnulado = 0) AND (F_03.DNI = ?)
GROUP BY F_03.NumRecibo, F_03.FechaRecibo, F_03.DNI
ORDER BY F_03.DNI;
"""