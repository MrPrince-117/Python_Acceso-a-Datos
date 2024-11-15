import mysql.connector as bd

bd_conexion = bd.connect(host='localhost', port='3306',
                                   user='prueba1', password='prueba1', database='prueba1')
cursor = bd_conexion.cursor()
try:
    cursor.execute("SELECT Nombre FROM alumno")

    for Nombre in cursor:
        print("Nombre: " , Nombre)

except bd_conexion.Error as error:
    print("Error: ",error)

bd_conexion.close()

