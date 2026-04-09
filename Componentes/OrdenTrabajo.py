class OrdenTrabajo:
    def __init__(self, id_orden, fecha_inicio, fecha_fin, estado, diagnostico, id_mecanico, id_vehiculo, id_cliente):
        self.id_orden = id_orden
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.diagnostico = diagnostico
        self.id_cliente = id_cliente
        self.id_mecanico = id_mecanico
        self.id_vehiculo = id_vehiculo  
