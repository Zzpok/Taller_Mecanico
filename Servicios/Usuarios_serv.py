from DataBase.conexion import Conexion
from Componentes.Usuarios import Usuario

def crear_usuario(usuario):
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
    sql = """
    INSERT INTO usuarios (username, password, rol)
    VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (
        usuario.username,
        usuario.password,
        usuario.rol
    ))
    conexion.commit()
    conexion.close()

def listar_usuarios():
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
    sql = "SELECT * FROM usuarios"
    cursor.execute(sql)
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

def eliminar_usuario(id_usuario):
    conexion = Conexion().conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM usuarios WHERE id_usuario = %s"
    cursor.execute(sql, (id_usuario,))
    conexion.commit()
    conexion.close()