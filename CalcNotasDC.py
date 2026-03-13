def leer_nota(numero_nota):         
    intentos = 0

    while intentos < 3:
        nota = float(input("  Ingrese nota " + str(numero_nota) + ": "))

        if nota >= 0 and nota <= 5:
            return nota
        else:
            intentos = intentos + 1
            print("  Nota inválida. Debe estar entre 0 y 5.")

    print("  Demasiados errores.")
    return -1

def promedio_materia(nombre):
    print("\n--- " + nombre + " ---")

    n1 = leer_nota(1)
    if n1 == -1:
        return -1

    n2 = leer_nota(2)
    if n2 == -1:
        return -1

    n3 = leer_nota(3)
    if n3 == -1:
        return -1

    promedio = (n1 + n2 + n3) / 3
    print("  Promedio " + nombre + ": " + str(round(promedio, 2)))
    return promedio

def mostrar_resultados(p1, p2, p3, p4, p5, hay_notas):  
    print("\n-------- RESULTADOS --------")

    if hay_notas == False:
        print("No ingresaste notas válidas.")
    else:
        prom_final = (p1 + p2 + p3 + p4 + p5) / 5

    
        print("Cálculo 1           : " + str(round(p1, 2)))
        print("Álgebra Lineal      : " + str(round(p2, 2)))
        print("Inglés              : " + str(round(p3, 2)))
        print("COYE                : " + str(round(p4, 2)))
        print("Algoritmia y Prog.  : " + str(round(p5, 2)))
        print("--------------------------")
        print("PROMEDIO FINAL      : " + str(round(prom_final, 2)))

        if prom_final >= 3:
            print("Has aprobado el semestre.")
        else:
            print("No has aprobado el semestre.")

    print("--------------------------------")

def main():
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    p5 = 0
    hay_notas = False
    opc = 0

    while opc != 3:
        print("\n----------- MENÚ -------------")
        print("1. Ingresar notas")
        print("2. Promedio del estudiante")
        print("3. Salir")

        opc = int(input("Seleccione una opción: "))

        if opc == 1:
            p1 = promedio_materia("CÁLCULO 1")
            if p1 == -1:             # BUG 4 CORREGIDO: era "!= -1", debia ser "== -1"
                opc = 3

            if opc != 3:
                p2 = promedio_materia("ÁLGEBRA LINEAL")
                if p2 == -1:         # BUG 4 CORREGIDO: este if estaba sin indentar dentro del bloque
                    opc = 3

            if opc != 3:
                p3 = promedio_materia("INGLÉS")
                if p3 == -1:
                    opc = 3

            if opc != 3:
                p4 = promedio_materia("COYE")
                if p4 == -1:
                    opc = 3

            if opc != 3:
                p5 = promedio_materia("ALGORITMIA Y PROGRAMACIÓN")
                if p5 == -1:
                    opc = 3

            if opc != 3:
                hay_notas = True
                print("\nNotas ingresadas correctamente.")
            else:
                print("Se superaron los errores. Se finalizará el sistema.")

        elif opc == 2:
            mostrar_resultados(p1, p2, p3, p4, p5, hay_notas)

        elif opc == 3:
            print("Hasta luego.")

        else:
            print("Opción inválida. Ingrese 1, 2 o 3.")

main()