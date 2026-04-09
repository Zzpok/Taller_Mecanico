from DataBase.conexion import Conexion
from Componentes.OrdenTrabajo import OrdenTrabajo

def crear_orden_trabajo(orden_trabajo):  # CREATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO orden_trabajo (
        fecha_inicio,
        fecha_fin,
        estado,
        diagnostico,
        id_mecanico,
        id_vehiculo,
        id_cliente
    )
    VALUES (NOW(), %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (
        orden_trabajo.fecha_fin,
        "pendiente",  # estado inicial fijo
        orden_trabajo.diagnostico,
        orden_trabajo.id_mecanico,
        orden_trabajo.id_vehiculo,
        orden_trabajo.id_cliente
    ))

    conexion.commit()
    conexion.close()

def asignar_mecanico(id_orden, id_mecanico):
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    UPDATE orden_trabajo
    SET id_mecanico = %s
    WHERE id_orden = %s
    """

    cursor.execute(sql, (id_mecanico, id_orden))
    conexion.commit()
    conexion.close()

def registrar_diagnostico(id_orden, diagnostico):
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    UPDATE orden_trabajo
    SET diagnostico = %s
    WHERE id_orden = %s
    """

    cursor.execute(sql, (diagnostico, id_orden))
    conexion.commit()
    conexion.close()

def cambiar_estado(id_orden, estado):
    estados_validos = ["pendiente", "en_proceso", "terminado", "entregado"]

    if estado not in estados_validos:
        print("¡Estado inválido!")
        return

    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    UPDATE orden_trabajo
    SET estado = %s
    WHERE id_orden = %s
    """

    cursor.execute(sql, (estado, id_orden))
    conexion.commit()
    conexion.close()