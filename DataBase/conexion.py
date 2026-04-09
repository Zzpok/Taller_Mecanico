import mysql.connector

class Conexion:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "Da.1016947482"
        self.database = "taller_mecanico"

    def conectar(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conexion
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None