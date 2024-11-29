from datetime import date

from peewee import *

from Pruebas import Cliente

# Conexión a la base de datos (ajusta el tipo y los parámetros según tu configuración)
db = MySQLDatabase('tienda', user='user1', password='Password_123',
                    host='localhost', port=3306)

class BaseModel(Model):
    class Meta:
        database = db

# Modelo para la tabla 'clientes'
class Clientes(BaseModel):
    codigo_cli = SmallIntegerField(primary_key=True)
    nombre = CharField(max_length=20)
    localidad = CharField(max_length=15)
    tlf = CharField(max_length=10)

# Modelo para la tabla 'proveedores'
class Proveedores(BaseModel):
    codigo_prov = SmallIntegerField(primary_key=True)
    nombre = CharField(max_length=20)
    localidad = CharField(max_length=15)
    fecha_alta = DateField()
    comision = FloatField()

# Modelo para la tabla 'articulos'
class Articulos(BaseModel):
    codarticulo = SmallIntegerField(primary_key=True)
    denominacion = CharField(max_length=25)
    precio = FloatField()
    stock = SmallIntegerField()
    zona = CharField(max_length=10)
    codigo_prov = ForeignKeyField(Proveedores, backref='articulos')

# Modelo para la tabla 'compras'
class Compras(BaseModel):
    numcompra = SmallIntegerField(primary_key=True)
    codigo_cli = ForeignKeyField(Clientes, backref='compras')
    fechacompra = DateField()

# Modelo para la tabla 'detallecompras'
class DetalleCompras(BaseModel):
    numcompra = ForeignKeyField(Compras, backref='detalles')
    codarticulo = ForeignKeyField(Articulos, backref='detalles')
    unidades = SmallIntegerField()

    class Meta:
        primary_key = False  # No se usa una clave primaria automática
        indexes = (
            (('numcompra', 'codarticulo'), True),  # Clave primaria compuesta
        )


# Crear las tablas en la base de datos
def crear_tablas():
    with db:
        db.create_tables([Clientes, Proveedores, Articulos, Compras, DetalleCompras])
def insertar_datos():
    try:
        # Insertar 3 clientes
        Clientes.insert_many([
            {'codigo_cli': 1, 'nombre': 'Juan Perez', 'localidad': 'Madrid', 'tlf': '600123456'},
            {'codigo_cli': 2, 'nombre': 'Ana López', 'localidad': 'Barcelona', 'tlf': '601987654'},
            {'codigo_cli': 3, 'nombre': 'Carlos Ruiz', 'localidad': 'Valencia', 'tlf': '602345678'}
        ]).execute()

        # Insertar 3 proveedores
        Proveedores.insert_many([
            {'codigo_prov': 1, 'nombre': 'Proveedor A', 'localidad': 'Sevilla', 'fecha_alta': date(2021, 5, 1), 'comision': 5.5},
            {'codigo_prov': 2, 'nombre': 'Proveedor B', 'localidad': 'Bilbao', 'fecha_alta': date(2022, 3, 15), 'comision': 4.0},
            {'codigo_prov': 3, 'nombre': 'Proveedor C', 'localidad': 'Granada', 'fecha_alta': date(2023, 7, 10), 'comision': 6.0}
        ]).execute()

        # Insertar 3 artículos
        Articulos.insert_many([
            {'codarticulo': 101, 'denominacion': 'Laptop', 'precio': 799.99, 'stock': 10, 'zona': 'A1', 'codigo_prov': 1},
            {'codarticulo': 102, 'denominacion': 'Mouse', 'precio': 19.99, 'stock': 100, 'zona': 'B1', 'codigo_prov': 2},
            {'codarticulo': 103, 'denominacion': 'Teclado', 'precio': 49.99, 'stock': 50, 'zona': 'C1', 'codigo_prov': 3}
        ]).execute()

        # Insertar 3 compras
        Compras.insert_many([
            {'numcompra': 1001, 'codigo_cli': 1, 'fechacompra': date(2024, 11, 15)},
            {'numcompra': 1002, 'codigo_cli': 2, 'fechacompra': date(2024, 11, 16)},
            {'numcompra': 1003, 'codigo_cli': 3, 'fechacompra': date(2024, 11, 17)}
        ]).execute()

        # Insertar 3 detalles de compra
        DetalleCompras.insert_many([
            {'numcompra': 1001, 'codarticulo': 101, 'unidades': 2},
            {'numcompra': 1002, 'codarticulo': 102, 'unidades': 5},
            {'numcompra': 1003, 'codarticulo': 103, 'unidades': 3}
        ]).execute()

        print("Datos insertados correctamente.")

    except IntegrityError as e:
        print("Error al insertar datos:", e)

def consultas():
    query = Cliente.select().where(Cliente.codigo_cli == 1)

if __name__ == "__main__":
    insertar_datos()
    print("Se insertaron correctamente los datos")


    def consultas():
        query = (Clientes
                 .select(Clientes, Compras)
                 .join(Compras, JOIN.LEFT_OUTER, on=(Clientes.codigo_cli == Compras.codigo_cli))
                 .dicts())  # Devuelve los resultados como diccionarios

        for registro in query:
            print(registro)


    def obtener_clientes_y_compras_detallado():
        query = (Clientes
                 .select(
            Clientes.codigo_cli.alias('codigo_cliente'),
            Clientes.nombre,
            Clientes.localidad,
            Compras.numcompra.coalesce(0).alias('numero_compra'),
            Compras.fechacompra.coalesce('Sin Compra').alias('fecha_compra')
        )
                 .join(Compras, JOIN.LEFT_OUTER, on=(Clientes.codigo_cli == Compras.codigo_cli))
                 .dicts())

        for registro in query:
            print(registro)


    # Llama a la función
    obtener_clientes_y_compras_detallado()

    # Llama a la función
    consultas()


