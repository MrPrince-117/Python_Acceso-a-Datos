import mysql.connector as bd

bd_conexion = bd.connect(host='localhost', port='3306',
                                   user='root', password='Password_123', database='hospitalet')
cursor = bd_conexion.cursor()
try:
    print ("Introduzca rango Salarial\n")
    v1=input("Valor 1:")
    v2 = input("Valor 2:")
    consulta=("SELECT apellido,oficio,salario FROM emp where salario between %s and %s")
    cursor.execute(consulta,(v1,v2))

    resultado=False
    print ("\n")
    for ape, ofi, sal in cursor:
         print("Apellido: ", ape)
         print("Oficio: " ,ofi)
         print("Salario: " , str(sal))
         print("-----------")
         resultado=True
    if resultado==False:
       print ("Sin resultados")

except bd_conexion.Error as error:
    print("Error: ",error)

bd_conexion.close()

