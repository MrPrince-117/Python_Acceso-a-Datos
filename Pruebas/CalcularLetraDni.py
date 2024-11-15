print("--------------CALCULAR LETRA DNI CON IF-------------")
dni=int(input("Introduzca DNI:"))
resultado=dni%23
letrasDni="TRWAGMYFPDXBNJZSQVHLCKET";

letra=letrasDni[resultado]
print (letra)