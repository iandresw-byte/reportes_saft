
from src.utils.cuentas_apremio_gob import clasificar_mora_gob

from src.services.parametro_service import ParametroService
from src.repositories.apremio_identificacion_repository import ApremioIdentifiacionRepository
from src.repositories.apremio_repository import ApremioRepository
from src.models.usuario_model import Usuario
import pandas as pd
import locale
for loc in ["es_ES", "Spanish", "es-ES", "es_HN", "es_ES.UTF-8"]:
    try:
        locale.setlocale(locale.LC_ALL, loc)
        break
    except locale.Error:
        pass


class ApremioIdentificacionService:
    def __init__(self, conexion, sistem, usuario_sesion: Usuario | None):
        self.repo = ApremioIdentifiacionRepository(conexion)
        self.repo_apremio = ApremioRepository(conexion, sistem=sistem)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem
        self.user = usuario_sesion
        self.data_ordenada = []

    def obtener_identificacion_mora(
            self,
            tipo_impuesto,
            tipo_persona="False",
            cod_aldea='070301',
            cod_barrio='070301001',
            mora_minima=0.0,
            fecha_min=None):

        self.data_ordenada = []

        if tipo_impuesto == '2':

            data_identifiacion = self.repo.obtener_top10_mora_ics(
                fecha_min,
                cod_aldea,
                cod_barrio,
                mora_minima
            )

            for dato in data_identifiacion:

                fila = {
                    'rtm': dato['RTM'],
                    'establecimiento': dato['Establecimiento'],
                    'dni': dato['DNI'],
                    'nombre': f"{dato['Pnombre']} {dato['SNombre']} {dato['PApellido']} {dato['SApellido']}",
                    'mes_ini': dato['mes_ini'],
                    'mes_fin': dato['mes_fin'],
                    'mora': dato['total'],
                }

                self.data_ordenada.append(fila)

        else:

            data_identifiacion = self.repo.obtener_top10_mora(
                fecha_min,
                tipo_impuesto,
                tipo_persona,
                cod_aldea,
                cod_barrio,
                mora_minima
            )

            for dato in data_identifiacion:

                fila = {
                    'dni': dato['DNI'],
                    'nombre': f"{dato['Pnombre']} {dato['SNombre']} {dato['PApellido']} {dato['SApellido']}",
                    'mes_ini': dato['mes_ini'],
                    'mes_fin': dato['mes_fin'],
                    'mora': dato['total'],
                }

                self.data_ordenada.append(fila)

        df = pd.DataFrame(self.data_ordenada)
        if df.empty:

            return df

        df['periodo'] = (
            df['mes_ini'].dt.strftime('%B %Y')
            + ' - ' +
            df['mes_fin'].dt.strftime('%B %Y')
        )

        return df
