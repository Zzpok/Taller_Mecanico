from DataBase.conexion import Conexion
from Componentes.Servicio import Servicio

def crear_servicio(servicio): #CREATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO servicios (nombre, descripcion, costo)
    VALUES (%s,%s,%s)
    """

    cursor.execute(sql, (
        servicio.nombre,
        servicio.descripcion,
        servicio.costo
    ))

    conexion.commit()
    conexion.close()