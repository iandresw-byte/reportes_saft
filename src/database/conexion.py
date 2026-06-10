import configparser

from cryptography.fernet import Fernet, InvalidToken
import pyodbc
import time
import os
from contextlib import contextmanager
from src.utils.config_manager import Config
from cryptography.fernet import Fernet


class ConexionBD:
    def __init__(self, tipo_bd, logger):
        self.tipo_bd = tipo_bd
        self.conexion = None
        self.log = logger
        self._conectar()

    def _conectar(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(base_dir)
        config_path = os.path.join(base_dir,  "config.ini")

        config = configparser.ConfigParser()
        config.read(config_path)
        key = b'sXKA2F58MaGlAEgZDRRYJ-xLedKzXq4rWw6gD8_iBVA='
        f = Fernet(key)

        clave_encriptada = 'gAAAAABpq5BMbtaMNHLv1uViW7XcSMAs6LnaJSIZxuooc5VCZP71vKxlgfAVGdZIJeWAzjdJs2ov9n-bkmucTCdYJCdUuV4EXg=='
        server_user = 'ANDBE'

        server_pass = f.decrypt(clave_encriptada.encode()).decode()

        self.log.info(f"Ruta config:, {server_user}")
        self.log.info(f"clave_encriptada: {clave_encriptada}")
        self.log.info(f"Password: {server_pass}")
        self.log.info(server_user)
        if self.tipo_bd == 'SAFT':
            self.conexion = pyodbc.connect(
                f"DSN=SAFTSQL;"
                f"UID={server_user};"
                f"PWD={server_pass};",
                autocommit=True
            )
        elif self.tipo_bd == 'SAFTBIT':
            self.conexion = pyodbc.connect(
                f"DSN=SAFTBIT;"
                f"UID={server_user};"
                f"PWD={server_pass};",
                autocommit=True
            )
        else:
            self.log.error("Tipo de base de datos no válido", exc_info=True)
            raise ValueError(
                f"Tipo de base de datos no válido: {self.tipo_bd}")

    def reconectar(self, intentos=3, espera=5):
        """Reintenta reconectar en caso de error."""
        for intento in range(1, intentos + 1):
            try:
                self.log.info(
                    f"Intentando reconectar a {self.tipo_bd} (Intento {intento}/{intentos})...")
                self._conectar()
                self.log.info(f"Reconectado a {self.tipo_bd} exitosamente.")
                return
            except Exception as e:
                self.log.info(f"Falló el intento {intento}: {e}")
                time.sleep(espera)
        raise ConnectionError(
            f"No se pudo reconectar a {self.tipo_bd} después de {intentos} intentos.")

    def obtener_cursor(self):
        if self.conexion:
            return self.conexion.cursor()
        else:
            self.log.info(f"La conexión no está establecida.")
            raise ValueError("La conexión no está establecida.")

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
            self.log.info(f"Conexión {self.tipo_bd} cerrada correctamente.")
        else:
            self.log.info(f"No hay conexión activa para cerrar.")

    @contextmanager
    def cursor(self):
        """Context manager para manejar cursores de forma segura."""
        cur = self.obtener_cursor()
        try:
            yield cur
        except (pyodbc.Error) as e:
            print(e)
            self.conexion.rollback()  # type: ignore
            self.log.error(f"Rollback realizado en {e} {self.tipo_bd}")
            self.reconectar()

            raise
        except Exception as e:
            self.conexion.rollback()  # type: ignore
            self.log.error(f"Rollback realizado en {e} {self.tipo_bd}")
            print(e)
            raise e
        finally:
            self.log.info(f"Conexión {self.tipo_bd} cerrada.")
            cur.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conexion:
            try:
                if exc_type is None:
                    self.conexion.commit()
                    self.log.info(
                        f"Commit realizado correctamente en {self.tipo_bd}")
                else:
                    self.conexion.rollback()
                    self.log.info(f"Rollback realizado en {self.tipo_bd}")
            finally:
                self.conexion.close()
                self.log.info(f"Conexión {self.tipo_bd} cerrada.")
