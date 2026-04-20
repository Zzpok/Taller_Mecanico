from DataBase.conexion import Conexion
from Componentes.DetalleOrd import DetalleOrd

def crear_detalle_orden(detalle_orden): #CREATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO detalle_orden (id_detalle, id_orden, id_repuesto, id_servicio, cantidad, precio)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (
        detalle_orden.id_detalle,
        detalle_orden.id_orden,
        detalle_orden.id_repuesto,
        detalle_orden.id_servicio,
        detalle_orden.cantidad,
        detalle_orden.precio
    ))

    conexion.commit()
    conexion.close()

def listar_detalle_orden():#READ
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = "SELECT * FROM detalle_orden"

    cursor.execute(sql)
    resultados = cursor.fetchall()

    conexion.close()

    return resultados
    
def actualizar_detalle_orden(detalle_orden):#UPDATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
        
    sql = """
    UPDATE detalle_orden
    SET id_orden = %s, 
    id_servicio = %s, 
    cantidad = %s, 
    precio = %s
    WHERE id_detalle = %s
    """
    
    cursor.execute(sql, (
        detalle_orden.id_orden,
        detalle_orden.id_servicio,
        detalle_orden.cantidad,
        detalle_orden.precio,
        detalle_orden.id_detalle
    ))
        
    conexion.commit()
    conexion.close()
        
def eliminar_detalle_orden(id_detalle):#DELETE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
        
    sql = "DELETE FROM detalle_orden WHERE id_detalle = %s"
        
    cursor.execute(sql, (id_detalle,))
        
    conexion.commit()
    conexion.close()        