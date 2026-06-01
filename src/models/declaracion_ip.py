from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from decimal import Decimal


@dataclass
class DeclaraImpInd:
    Identidad: str
    FechaPresenta: datetime
    PeriodoDeclara: int
    Impuesto: Decimal
    CodDeclaraIP: str
    EstadoDeclaraIP: int
    IngSueldos: Decimal
    Descuento: Decimal
    MultaDeclaraTardeIP: Decimal
    RecMoraIP: Decimal
    RecSobreSaldoIP: Decimal
    Descuento: Decimal
    HonorariosProf: Optional[Decimal] = Decimal('0.0')
    IngNoGrabados: Optional[Decimal] = Decimal('0.0')
    IngAlquileres: Optional[Decimal] = Decimal('0.0')
    OtrosIngresos: Optional[Decimal] = Decimal('0.0')
    Retencion: Optional[Decimal] = Decimal('0.0')
    NroFactura: Optional[int] = None
    FechaPagoIP: Optional[datetime] = None
    FechaFacturadoIP: Optional[datetime] = None
    MontoPagado: Optional[Decimal] = Decimal('0.0')


@dataclass
class DeclaraNat:
    Empresa: str
    Identidad: str
    Nombre: str
    Ingreso: Decimal
    Impuesto: Decimal
    Multa: Decimal
    Interes: Decimal
    Recargo: Decimal
    Descuento: Decimal
    Total: Decimal
    Fecha: datetime
    NumRecibo: int
    AnioDeclara: int
    FechaPresenta: datetime
    UsuarioCrea: str
    CodDeclaraIP: str
    NumAvPg: int
    Tasas: Decimal
    RTM: str
