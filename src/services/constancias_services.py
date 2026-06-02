from datetime import date
from pandas import DataFrame
from src.repositories.constancias_repository import ConstanciaRepository


class ConstanciasService:
    def __init__(self, conexion):
        self.constancias = ConstanciaRepository(conexion)

    def obtener_licencia_uma_ics(self, num_recibo):
        hoy = date.today()
        periodo = hoy.year
        fecha = date.today().strftime("%d-%m-%Y")
        fecha_vence = date(hoy.year, 12, 31).strftime("%d-%m-%Y")
        existe = self.constancias.existe_recibo(num_recibo)
        licencia = []
        if existe:
            datos = self.constancias.recargar_licencia(num_recibo)
            if datos:
                licencia.append({
                    "propietario": datos["Propietario"],
                    "dni": datos["Identidad"],
                    "establecimiento": datos["Negocio"],
                    "direccion_establecimento": datos["Ubicacion"],
                    "fecha_solicitud": datos["FechaSolicitud"],
                    "fecha_vence": datos["FechaVence"],
                    "num_recibo": datos["NoRecibo"],
                    "rtm": datos["rtm"],
                    "no_licencia": datos["NoLicencia"],
                    "periodo": datos["Periodo"],
                })
        else:
            datos = self.constancias.licecia_uma_ics(num_recibo)
            num_licencia = self.constancias.licencia_numero()
            if not datos:
                raise ValueError(
                    "No se encontraron datos bajo este numero de recibo.")

            if datos["Tipo"]:
                datos_contribuyente = self.constancias.get_propietario(
                    datos["IdRepresentante"])
                if datos_contribuyente:
                    licencia.append({
                        "propietario": f"{datos_contribuyente["Pnombre"]} {datos_contribuyente["SNombre"]} {datos_contribuyente["PApellido"]} {datos_contribuyente["SApellido"]}",
                        "dni": datos_contribuyente["DNI"],
                        "establecimiento": datos["Pnombre"],
                        "direccion_propietario": datos_contribuyente["Direccion"],
                        "direccion_establecimento": datos["Direccion"],
                        "fecha_solicitud": fecha,
                        "fecha_vence": fecha_vence,
                        "num_recibo": num_recibo,
                        "rtm": datos["DNI"],
                        "no_licencia": num_licencia,
                        "periodo": periodo,
                    })
            else:
                datos_establecimeinto = self.constancias.get_establecimiento(
                    datos["DNI"])
                if datos_establecimeinto:
                    licencia.append({
                        "propietario": f"{datos["Pnombre"]} {datos["SNombre"]} {datos["PApellido"]} {datos["SApellido"]}",
                        "dni": datos["DNI"],
                        "establecimiento": datos_establecimeinto[0]["Pnombre"],
                        "direccion_propietario": datos["Direccion"],
                        "direccion_establecimento": datos_establecimeinto[0]["Direccion"],
                        "fecha_solicitud": fecha,
                        "fecha_vence": fecha_vence,
                        "num_recibo": num_recibo,
                        "rtm": datos_establecimeinto[0]["DNI"],
                        "no_licencia": num_licencia,
                        "periodo": periodo,
                    })
                else:
                    licencia.append({
                        "propietario": f"{datos["Pnombre"]} {datos["SNombre"]} {datos["PApellido"]} {datos["SApellido"]}",
                        "dni": datos["DNI"],
                        "establecimiento": "",
                        "direccion_propietario": datos["Direccion"],
                        "direccion_establecimento": "",
                        "fecha_solicitud": fecha,
                        "fecha_vence": fecha_vence,
                        "num_recibo": num_recibo,
                        "rtm": "",
                        "no_licencia": num_licencia,
                        "periodo": periodo,
                    })
            self.insertar_licencia_uma_ics(licencia)

        return licencia

    def insertar_licencia_uma_ics(self, data_licencia):
        data_licencia = data_licencia[0]
        self.constancias.insertar_licecia_uma_ics(data_licencia["no_licencia"],
                                                  data_licencia["periodo"],
                                                  data_licencia["dni"],
                                                  data_licencia["propietario"],
                                                  data_licencia["rtm"],
                                                  data_licencia["establecimiento"],
                                                  data_licencia["direccion_establecimento"],
                                                  data_licencia["num_recibo"],
                                                  data_licencia["fecha_solicitud"],
                                                  data_licencia["fecha_vence"])

    def existe_licencia(self, num_recibo: int):
        return self.constancias.existe_recibo(num_recibo=num_recibo)
