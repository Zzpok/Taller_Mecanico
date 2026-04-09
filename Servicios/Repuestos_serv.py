from DataBase import Conexion
from Componentes.Repuestos import Repuesto

def crear_repuesto(repuesto): #CREATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO repuestos (nombre, marca, stock, precio)
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(sql, (
        repuesto.nombre,
        repuesto.marca,
        repuesto.stock,
        repuesto.precio
    ))

    conexion.commit()
    conexion.close()

def actualizar_repuesto(repuesto):#UPDATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
        
    sql = """
    UPDATE repuestos
    SET nombre = %s, 
    marca = %s, 
    stock = %s, 
    precio = %s
    WHERE id_repuesto = %s
    """
    
    cursor.execute(sql, (
        repuesto.nombre,
        repuesto.marca,
        repuesto.stock,
        repuesto.precio,
        repuesto.id_repuesto
    ))
        
    conexion.commit()
    conexion.close()

def consultar_repuestos():#READ
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT id_repuesto, nombre, stock
    FROM repuestos
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()

    conexion.close()

    return resultados 

def alertar_stock_bajo():
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT id_repuesto, nombre, stock
    FROM repuestos
    WHERE stock < 5
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()

    conexion.close()

    return resultados