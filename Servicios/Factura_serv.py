from DataBase.conexion import Conexion
from Componentes.Facturas import Factura

def crear_factura(factura): #CREATE
    conexion = Conexion().conectar()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO facturas (fecha, subtotal, impuestos, total, metodo_pago, id_orden)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (
        factura.fecha,
        factura.subtotal,
        factura.impuestos,
        factura.total,
        factura.metodo_pago,
        factura.id_orden

    ))

    conexion.commit()
    conexion.close()