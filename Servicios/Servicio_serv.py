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

def listar_servicios():
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
    sql = "SELECT * FROM servicios"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

def actualizar_servicio(servicio):
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
    sql = """
    UPDATE servicios
    SET nombre = %s, descripcion = %s, costo = %s
    WHERE id_servicio = %s
    """
    cursor.execute(sql, (
        servicio.nombre,
        servicio.descripcion,
        servicio.costo,
        servicio.id_servicio
    ))
    conexion.commit()
    conexion.close()

def eliminar_servicio(id_servicio):
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM servicios WHERE id_servicio = %s"
    cursor.execute(sql, (id_servicio,))
    conexion.commit()
    conexion.close()