from dataclasses import dataclass
from datetime import datetime


@dataclass
class Tra_LiceAmbie:
    NumRecibo: int
    Identidad: str
    Direccion: str
    idrepresentante: str
    Negocio: str
    NoPermiso: int
    Periodo: int
    Propietario: str
    Ubicacion: str
    Actividad: str
    Observacion: str
    Fecha: datetime
    CodAldea: str
    CodBarrio: str
    Usuario: str
    UsuarioMod: str
    FechaSolicitud: datetime
    FechaVencimiento: datetime
    rtn: str
    Telefono: str
    NumeroRenovacion: int
    HorarioAlcohol: int
