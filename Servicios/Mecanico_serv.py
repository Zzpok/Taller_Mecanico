from DataBase.conexion import Conexion
from Componentes.Mecanico import Mecanico

def crear_mecanico(mecanico): #CREATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO mecanicos (nombre, apellido, especialidad, disponibilidad, salario)
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (
        mecanico.nombre,
        mecanico.apellido,
        mecanico.especialidad,
        mecanico.disponibilidad,
        mecanico.salario
    ))

    conexion.commit()
    conexion.close()

def listar_mecanicos():#READ
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = "SELECT * FROM mecanicos"

    cursor.execute(sql)
    resultados = cursor.fetchall()

    conexion.close()

    return resultados
    
def actualizar_mecanico(mecanico):#UPDATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
        
    sql = """
    UPDATE mecanicos
    SET nombre = %s, 
    apellido = %s, e
    specialidad = %s, 
    disponibilidad = %s, 
    salario = %s
    WHERE id_mecanico = %s
    """
    
    cursor.execute(sql, (
        mecanico.nombre,
        mecanico.apellido,
        mecanico.especialidad,
        mecanico.disponibilidad,
        mecanico.salario,
        mecanico.id_mecanico
    ))
        
    conexion.commit()
    conexion.close()
        
def eliminar_mecanico(id_mecanico):#DELETE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
        
    sql = "DELETE FROM mecanicos WHERE id_mecanico = %s"
        
    cursor.execute(sql, (id_mecanico,))
        
    conexion.commit()
    conexion.close()        

def consultar_disponibilidad(disponibilidad):#READ
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = "SELECT * FROM mecanicos WHERE disponibilidad = %s"

    cursor.execute(sql, (disponibilidad,))
    resultados = cursor.fetchall()

    conexion.close()

    return resultados