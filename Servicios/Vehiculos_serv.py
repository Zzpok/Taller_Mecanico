from DataBase.conexion import Conexion
from Componentes.Vehiculos import Vehiculo

def crear_vehiculo(vehiculo): #CREATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO vehiculos (marca, modelo, año, color, placa, id_cliente)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (
    vehiculo.marca,
    vehiculo.modelo,
    vehiculo.año,
    vehiculo.color,
    vehiculo.placa,
    vehiculo.id_cliente
))

    conexion.commit()
    conexion.close()

def editar_vehiculo(vehiculo):#UPDATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
        
    sql = """
    UPDATE vehiculos
    SET marca = %s, 
    modelo = %s, 
    año = %s, 
    color = %s,
    placa = %s, 
    id_cliente = %s
    WHERE id_vehiculo = %s
    """
    
    cursor.execute(sql, (
        vehiculo.marca,
        vehiculo.modelo,
        vehiculo.año,
        vehiculo.color,
        vehiculo.placa,
        vehiculo.id_cliente,
        vehiculo.id_vehiculo
    ))
        
    conexion.commit()
    conexion.close()

def listar_vehiculos():
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = "SELECT * FROM vehiculos"

    cursor.execute(sql)
    resultados = cursor.fetchall()
    
    conexion.close()
    return resultados

def consultar_vehiculos_placa(placa):#READ
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT * FROM vehiculos WHERE placa = %s
    """

    cursor.execute(sql, (placa,))
    resultado = cursor.fetchone()

    conexion.close()

    return resultado

def historial_reparaciones(placa):
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT 
        v.placa,
        o.id_orden,
        o.fecha,
        s.nombre,
        d.cantidad,
        d.precio
    FROM vehiculos v
    JOIN orden_trabajo o ON v.id_vehiculo = o.id_vehiculo
    JOIN detalle_orden d ON o.id_orden = d.id_orden
    JOIN servicios s ON d.id_servicio = s.id_servicio
    WHERE v.placa = %s
    """

    cursor.execute(sql, (placa,))
    resultados = cursor.fetchall()

    conexion.close()

    return resultados