class Factura:
    def __init__(self, id_factura, fecha, subtotal, impuestos, total, metodo_pago, id_orden):
        self.id_factura = id_factura
        self.fecha = fecha
        self.subtotal = subtotal
        self.impuestos = impuestos
        self.total = total
        self.metodo_pago = metodo_pago
        self.id_orden = id_orden

