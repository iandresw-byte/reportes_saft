from datetime import date
from pandas import DataFrame
from src.repositories.contribuyente_reposiory import ContribuyenteReposiory
from src.repositories.apremio_identificacion_repository import ApremioIdentifiacionRepository


class ContribuyenteService:
    def __init__(self, conexion):
        self.repo = ContribuyenteReposiory(conexion)
        self.apremio = ApremioIdentifiacionRepository(conexion)

    def obtener_datos_contribuyente(self, identidad):
        fecha = date.today().strftime("%d-%m-%Y")

        datos = self.repo.obtener_contribuyente(
            dni=identidad, fecha_ahora=fecha)
        if not datos:
            raise ValueError(
                "No se encontraron datos bajo esta Identidad.")

        return datos

    def obtener_datos_contribuyente_proceso(self, identidad):
        data_res = []
        datos_1er = self.apremio.otener_info_1er_req_by_dni(dni=identidad)
        datos_2do = self.apremio.otener_info_2do_req_by_dni(dni=identidad)
        datos_certi = self.apremio.otener_info_cerificacion_by_dni(
            dni=identidad)

        if datos_1er:
            data_res.append(
                {
                    "Id": datos_1er[0]["IdDocumento"],
                    "TipoDoc":  datos_1er[0]["TipoDoc"],
                    "Estado":  datos_1er[0]["Estado"],
                    "FechaGeneracion": datos_1er[0]["FechaGeneracion"],
                    "FechaEntrega":  datos_1er[0]["FechaEntrega"],
                }
            )

        if datos_2do:
            data_res.append(
                {
                    "Id": datos_2do[0]["IdDocumento"],
                    "TipoDoc":  datos_2do[0]["TipoDoc"],
                    "Estado":  datos_2do[0]["Estado"],
                    "FechaGeneracion": datos_2do[0]["FechaGeneracion"],
                    "FechaEntrega":  datos_2do[0]["FechaEntrega"],
                }
            )

        if datos_certi:
            data_res.append(
                {
                    "Id": datos_certi[0]["IdDocumento"],
                    "TipoDoc":  datos_certi[0]["TipoDoc"],
                    "Estado":  datos_certi[0]["Estado"],
                    "FechaGeneracion": datos_certi[0]["FechaGeneracion"],
                    "FechaEntrega":  datos_certi[0]["FechaEntrega"],
                }
            )

        if not data_res:
            return None

        return data_res
