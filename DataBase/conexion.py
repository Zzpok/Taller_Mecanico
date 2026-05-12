import mysql.connector
import mysql.connector.errors as error

class Conexion:
    def __init__(self):
        self.host     = "localhost"
        self.user     = "root"
        self.password = "Da.1016947482"
        self.database = "taller_mecanico"

    def conectar(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conexion
        except error.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None


    def crear_tablas(self):
        con = self.conectar()
        if con is None:
            print(" No se pudo conectar. Las tablas no fueron creadas.")
            return

        cursor = con.cursor()

        tablas = {
            "usuarios": """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario  INT          AUTO_INCREMENT PRIMARY KEY,
                    username    VARCHAR(50)  NOT NULL,
                    password    VARCHAR(100) NOT NULL,
                    rol         VARCHAR(20)  NOT NULL
                )
            """,

            "clientes": """
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente  INT          AUTO_INCREMENT PRIMARY KEY,
                    nombre      VARCHAR(100) NOT NULL,
                    apellido    VARCHAR(100) NOT NULL,
                    telefono    VARCHAR(20),
                    correo      VARCHAR(100),
                    direccion   VARCHAR(100)
                )
            """,

            "mecanicos": """
                CREATE TABLE IF NOT EXISTS mecanicos (
                    id_mecanico    INT           AUTO_INCREMENT PRIMARY KEY,
                    nombre         VARCHAR(100)  NOT NULL,
                    apellido       VARCHAR(100)  NOT NULL,
                    especialidad   VARCHAR(100),
                    disponibilidad ENUM('disponible','no_disponible') NOT NULL DEFAULT 'disponible',
                    salario        DECIMAL(10,2)
                )
            """,

            "vehiculos": """
                CREATE TABLE IF NOT EXISTS vehiculos (
                    id_vehiculo INT          AUTO_INCREMENT PRIMARY KEY,
                    placa       VARCHAR(100) NOT NULL UNIQUE,
                    marca       VARCHAR(100),
                    modelo      VARCHAR(20),
                    año         INT,
                    color       VARCHAR(100),
                    id_cliente  INT NOT NULL,
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )
            """,

            "repuestos": """
                CREATE TABLE IF NOT EXISTS repuestos (
                    id_repuesto INT          AUTO_INCREMENT PRIMARY KEY,
                    nombre      VARCHAR(100) NOT NULL,
                    marca       VARCHAR(100),
                    stock       INT          NOT NULL DEFAULT 0,
                    precio      VARCHAR(100)
                )
            """,

            "servicios": """
                CREATE TABLE IF NOT EXISTS servicios (
                    id_servicio INT          AUTO_INCREMENT PRIMARY KEY,
                    nombre      VARCHAR(100) NOT NULL,
                    descripcion VARCHAR(200),
                    costo       VARCHAR(20)
                )
            """,

            "ordenes": """
                CREATE TABLE IF NOT EXISTS ordenes (
                    id_orden     INT  AUTO_INCREMENT PRIMARY KEY,
                    fecha_inicio DATE,
                    fecha_fin    DATE,
                    estado       ENUM('pendiente','en_proceso','terminado','entregado') NOT NULL DEFAULT 'pendiente',
                    diagnostico  VARCHAR(200),
                    id_mecanico  INT NOT NULL,
                    id_vehiculo  INT NOT NULL,
                    id_cliente   INT NOT NULL,
                    FOREIGN KEY (id_mecanico) REFERENCES mecanicos(id_mecanico)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (id_cliente)  REFERENCES clientes(id_cliente)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )
            """,

            "detalle_orden": """
                CREATE TABLE IF NOT EXISTS detalle_orden (
                    id_detalle  INT           AUTO_INCREMENT PRIMARY KEY,
                    id_orden    INT           NOT NULL,
                    id_repuesto INT,
                    cantidad    INT           NOT NULL DEFAULT 1,
                    precio      DECIMAL(10,0),
                    id_servicio INT,
                    FOREIGN KEY (id_orden)    REFERENCES ordenes(id_orden)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (id_repuesto) REFERENCES repuestos(id_repuesto)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )
            """,

            "facturas": """
                CREATE TABLE IF NOT EXISTS facturas (
                    id_factura  INT           AUTO_INCREMENT PRIMARY KEY,
                    fecha       DATE,
                    subtotal    DECIMAL(10,2),
                    impuestos   DECIMAL(10,2),
                    total       DECIMAL(10,2),
                    metodo_pago VARCHAR(20),
                    id_orden    INT NOT NULL UNIQUE,
                    FOREIGN KEY (id_orden) REFERENCES ordenes(id_orden)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )
            """,
        }

        print("Creando tablas en 'taller_mecanico'...\n")
        try:
            for nombre, sql in tablas.items():
                cursor.execute(sql)
                print(f" creada la tabla {nombre}")
            con.commit()
            print("\n Todas las tablas fueron creadas correctamente.")
        except error.Error as e:
            print(f" Error al crear tablas: {e}")
        finally:
            cursor.close()
            con.close()



if __name__ == "__main__":
    db = Conexion()
    db.crear_tablas()