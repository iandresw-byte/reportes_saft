class DataBaseRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def parametroCont(self):
        query = """
            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'Ambiental' AND Object_ID = OBJECT_ID('ParametroCont'))
            BEGIN
                ALTER TABLE ParametroCont ADD Ambiental NVARCHAR(255) DEFAULT '' NOT NULL;
            END;

	        IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'FirmaPO_1' AND Object_ID = OBJECT_ID('ParametroCont'))
            BEGIN
                ALTER TABLE ParametroCont ADD FirmaPO_1 int DEFAULT 0 NOT NULL;
            END;

            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'FirmaPO_2' AND Object_ID = OBJECT_ID('ParametroCont'))
            BEGIN
                ALTER TABLE ParametroCont ADD FirmaPO_2 int DEFAULT 0 NOT NULL;
            END;

            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'Justicia' AND Object_ID = OBJECT_ID('ParametroCont'))
            BEGIN
                ALTER TABLE ParametroCont ADD Justicia NVARCHAR(255) DEFAULT '' NOT NULL;
            END;

            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'Secretaria' AND Object_ID = OBJECT_ID('ParametroCont'))
            BEGIN
                ALTER TABLE ParametroCont ADD Secretaria NVARCHAR(255) DEFAULT '' NOT NULL;
            END;

            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'DesarrolloUrbano' AND Object_ID = OBJECT_ID('ParametroCont'))
            BEGIN
                ALTER TABLE ParametroCont ADD DesarrolloUrbano NVARCHAR(255) DEFAULT '' NOT NULL;
            END;

            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'UltNumPO' AND Object_ID = OBJECT_ID('ParametroCont'))
            BEGIN
                ALTER TABLE ParametroCont ADD UltNumPO INT DEFAULT 0 NOT NULL;
            END;

            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'HorarioAlcohol' AND Object_ID = OBJECT_ID('Tra_PermOP'))
            BEGIN
                ALTER TABLE Tra_PermOP ADD HorarioAlcohol INT DEFAULT 0 NOT NULL;
            END;

            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'FinAmni' AND Object_ID = OBJECT_ID('SystemParam'))
            BEGIN
                ALTER TABLE SystemParam ADD FinAmni date DEFAULT 0 NOT NULL;
            END;


            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'FechaRegistro' AND Object_ID = OBJECT_ID('FC_03'))
            BEGIN
                ALTER TABLE FC_03 ADD FechaRegistro date DEFAULT (getdate());
            END;

       
            
        """
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query)
            return True
        except Exception as e:
            print("Error en parametroCont:", e)
            return False

    def actualizar_login(self):
        query = """
            ALTER LOGIN ANDBE WITH PASSWORD = 'df4414da57';
            """
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query)
            return True
        except Exception as e:
            print("Error en actualizar login:", e)
            return False

    def modifiaciones_apremio(self):
        query = query = """
--TABLA ENCABEZADO
IF NOT EXISTS (
    SELECT 1 
    FROM sys.tables 
    WHERE name = 'ApremioEnDoc' 
    AND schema_id = SCHEMA_ID('dbo')
)
BEGIN
    CREATE TABLE dbo.ApremioEnDoc (
        IdDocumento INT  NOT NULL,
        Identidad NVARCHAR(15) NOT NULL,
        TipoDoc INT NOT NULL,
        TipoImpuesto INT NOT NULL,
        FechaGeneracion DATETIME NOT NULL DEFAULT(GETDATE()),
        FechaEntrega DATETIME NULL,
        Estado NVARCHAR(20) NOT NULL,
        TotalMora DECIMAL(18,2) NOT NULL DEFAULT(0),
        CodBarrio NCHAR(10) NULL,
        Observacion NVARCHAR(255) NULL,

        CONSTRAINT PK_ApremioEnDoc 
            PRIMARY KEY (IdDocumento),

        CONSTRAINT CK_ApremioEnDoc_Estado 
            CHECK (Estado IN 
            ('Vencido','Entregado','Generado',
             'No Generado','Pronto Vence','Anulado'))
    );
END;

-- TABLA RELACION 
IF NOT EXISTS (
    SELECT 1 
    FROM sys.tables 
    WHERE name = 'ApremioRelacion'
    AND schema_id = SCHEMA_ID('dbo')
)
BEGIN
    CREATE TABLE dbo.ApremioRelacion (
        IdDocumento INT NOT NULL,
        TipoDoc INT NOT NULL,
        Id1erRequerimiento INT NULL,

        CONSTRAINT PK_ApremioRelacion 
            PRIMARY KEY (IdDocumento),

        CONSTRAINT FK_ApremioRelacion_Documento
            FOREIGN KEY (IdDocumento)
            REFERENCES dbo.ApremioEnDoc(IdDocumento)
            ON DELETE CASCADE
    );
END;

-- TABLA DETALLE 
IF NOT EXISTS (
    SELECT 1 
    FROM sys.tables 
    WHERE name = 'ApremioDetalle'
    AND schema_id = SCHEMA_ID('dbo')
)
BEGIN
    CREATE TABLE dbo.ApremioDetalle (
        Id INT IDENTITY(1,1) NOT NULL,
        IdDocumento INT NOT NULL,
        TipoImpuesto INT NOT NULL,
        Descripcion VARCHAR(100) NULL,
        Observacion VARCHAR(100) NULL,
        Monto DECIMAL(18,2) NOT NULL DEFAULT(0),

        CONSTRAINT PK_ApremioDetalle 
            PRIMARY KEY (Id),

        CONSTRAINT FK_ApremioDetalle_Documento
            FOREIGN KEY (IdDocumento)
            REFERENCES dbo.ApremioEnDoc(IdDocumento)
            ON DELETE CASCADE
    );
END;

-- TABLA FACTURA 
IF NOT EXISTS (
    SELECT 1 
    FROM sys.tables 
    WHERE name = 'ApremioAvPg'
    AND schema_id = SCHEMA_ID('dbo')
)
BEGIN
    CREATE TABLE dbo.ApremioAvPg (
        IdDocumento INT NOT NULL,
        NumAvPg INT NOT NULL,
        ValNumAvPg DECIMAL(18,2) NOT NULL DEFAULT(0),

        CONSTRAINT FK_ApremioAvPg_Documento
            FOREIGN KEY (IdDocumento)
            REFERENCES dbo.ApremioEnDoc(IdDocumento)
            ON DELETE CASCADE
    );
END;
"""
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query)
            return True
        except Exception as e:
            print("Error en parametModificaciones Apremio:", e)
            return False

    def crear_vistas_powerBI(self):
        query = """
CREATE VIEW dbo.vw_MoraBienesInmuebles
AS
SELECT
    dbo.F_01.DNI,
    dbo.FC_03.Pnombre + ' ' + dbo.FC_03.SNombre + ' ' +
    dbo.FC_03.PApellido + ' ' + dbo.FC_03.SApellido AS Nombre_completo,
    dbo.F_01.ClaveCatastro,
    dbo.Aldea.NombreAldea,
    dbo.TablaBarrio.NombreBarrio,
    MIN(YEAR(dbo.F_01.FechaVenceAvPg)) AS Inicio,
    MAX(YEAR(dbo.F_01.FechaVenceAvPg)) AS Fin,
    MAX(YEAR(dbo.F_01.FechaVenceAvPg)) - MIN(YEAR(dbo.F_01.FechaVenceAvPg)) + 1 AS CantidadAnios,

    CAST(SUM(CASE
                WHEN SUBSTRING(dbo.F_02.CtaIngreso,1,6)='111110'
                THEN dbo.F_02.ValorUnitAvPgDet
                ELSE 0
             END) AS FLOAT) AS ImpuestoBI,

    CAST(SUM(CASE
                WHEN SUBSTRING(dbo.F_02.CtaIngreso,1,6)='111119'
                THEN dbo.F_02.ValorUnitAvPgDet
                ELSE 0
             END) AS FLOAT) AS TasasBI,

    CAST(SUM(CASE
                WHEN SUBSTRING(dbo.F_02.CtaIngreso,1,6)='112121'
                THEN dbo.F_02.ValorUnitAvPgDet
                ELSE 0
             END) AS FLOAT) AS RecargosBI,

    CAST(SUM(CASE
                WHEN SUBSTRING(dbo.F_02.CtaIngreso,1,6)='112122'
                THEN dbo.F_02.ValorUnitAvPgDet
                ELSE 0
             END) AS FLOAT) AS RecuperacionBI,

    CAST(SUM(CASE
                WHEN SUBSTRING(dbo.F_02.CtaIngreso,1,6)='112126'
                THEN dbo.F_02.ValorUnitAvPgDet
                ELSE 0
             END) AS FLOAT) AS InteresesBI,

    CAST(SUM(CASE
                WHEN SUBSTRING(dbo.F_02.CtaIngreso,1,6)='112127'
                THEN dbo.F_02.ValorUnitAvPgDet
                ELSE 0
             END) AS FLOAT) AS DescuentosBI,

    CAST(SUM(dbo.F_02.ValorUnitAvPgDet) AS FLOAT) AS Mora

FROM dbo.F_01
INNER JOIN dbo.F_02
    ON dbo.F_01.NumAvPg = dbo.F_02.NumAvPg
INNER JOIN dbo.FC_03
    ON dbo.F_01.DNI = dbo.FC_03.DNI
INNER JOIN dbo.FC_01
    ON dbo.F_01.ClaveCatastro = dbo.FC_01.CatClv
INNER JOIN dbo.Aldea
    ON dbo.FC_01.CodAldea = dbo.Aldea.CodAldea
INNER JOIN dbo.TablaBarrio
    ON dbo.FC_01.CodBarrio = dbo.TablaBarrio.CodBarrio
   AND dbo.Aldea.CodAldea = dbo.TablaBarrio.CodAldea

WHERE dbo.F_01.AvPgEstado = 1
  AND dbo.F_01.AvPgTipoImpuesto = 1

GROUP BY
    dbo.F_01.DNI,
    dbo.FC_03.Pnombre,
    dbo.FC_03.SNombre,
    dbo.FC_03.PApellido,
    dbo.FC_03.SApellido,
    dbo.F_01.ClaveCatastro,
    dbo.Aldea.NombreAldea,
    dbo.TablaBarrio.NombreBarrio;
GO
"""
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query)
            return True
        except Exception as e:
            print("Error al crear vistas:", e)
            return False