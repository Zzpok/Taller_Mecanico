from DataBase.conexion import Conexion
from Componentes.Usuarios import Usuario

def login(username, password):
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT * FROM usuarios
    WHERE username = %s AND password = %s
    """

    cursor.execute(sql, (username, password))
    resultado = cursor.fetchone()

    conexion.close()

    if resultado:
        usuario = Usuario(*resultado)
        return usuario
    else:
        return None