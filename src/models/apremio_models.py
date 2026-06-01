from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum
hoy = datetime.now().strftime("%Y/%m/%d")


@dataclass
class ApremioEnDoc:
    Identidad: str
    IdDocumento: int
    TipoDoc: int
    TipoImpuesto: int
    TotalMora: Decimal
    CodBarrio: str
    Observacion: Optional[str] = 'Generado'
    Estado: Optional[str] = 'Generado'
    FechaGeneracion: Optional[datetime] = field(default_factory=datetime.now)
    FechaEntrega: Optional[datetime] = None


@dataclass
class ApremioDetalle:
    IdDocumento: int
    TipoImpuesto: int
    Descripcion: str
    Observacion: str
    Monto: Decimal


@dataclass
class ApremioAvPg:
    idDocumento: int
    NumAvPg: int
    ValNumAvPg: Decimal


@dataclass
class ApremioRelacion:
    IdDocumento: int
    TipoDoc: int
    Id1erRequerimiento: int


class EstadoApremio(str, Enum):
    VENCIDO = "Vencido"
    ENTREGADO = "Entregado"
    GENERADO = "Generado"
    NO_GENERADO = "No Generado"
    PRONTO_VENCE = "Pronto Vence"
    ANULADO = "Anulado"
