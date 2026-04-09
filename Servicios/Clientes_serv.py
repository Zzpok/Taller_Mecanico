from DataBase.conexion import Conexion
from Componentes.Clientes import Cliente

def crear_cliente(cliente): #CREATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO clientes (nombre, apellido, telefono, correo, direccion)
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (
        cliente.nombre,
        cliente.apellido,
        cliente.telefono,
        cliente.correo,
        cliente.direccion
    ))

    conexion.commit()
    conexion.close()

def listar_clientes():#READ
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = "SELECT * FROM clientes"

    cursor.execute(sql)
    resultados = cursor.fetchall()

    conexion.close()

    return resultados
    
def actualizar_cliente(cliente):#UPDATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
        
    sql = """
    UPDATE clientes
    SET nombre = %s, 
    apellido = %s, 
    telefono = %s, 
    correo = %s, 
    direccion = %s
    WHERE id_cliente = %s
    """
    
    cursor.execute(sql, (
        cliente.nombre,
        cliente.apellido,
        cliente.telefono,
        cliente.correo,
        cliente.direccion,
        cliente.id_cliente
    ))
        
    conexion.commit()
    conexion.close()
        
def eliminar_cliente(id_cliente):#DELETE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
        
    sql = "DELETE FROM clientes WHERE id_cliente = %s"
        
    cursor.execute(sql, (id_cliente,))
        
    conexion.commit()
    conexion.close()        