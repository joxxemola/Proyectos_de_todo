
Funcion nota <- LeerNota(mensaje)
	
	Definir nota Como Real
	Definir intentos Como Entero
	
	intentos <- 0
	nota <- -1
	
	Repetir
		
		Escribir mensaje
		Leer nota
		
		Si nota < 0 O nota > 5 Entonces
			intentos <- intentos + 1
			Escribir "Nota invalida. Intento ", intentos, " de 3."
		FinSi
		
	Hasta Que (nota >= 0 Y nota <= 5) O intentos = 3
	
	Si intentos = 3 Y (nota < 0 O nota > 5) Entonces
		nota <- -1
	FinSi
	
FinFuncion


// ============================================================
//  FUNCIÓN: PromedioMateria
//  Lee las 3 notas de una materia y devuelve su promedio.
//  Devuelve -1 si hubo demasiados errores en alguna nota.
// ============================================================
Funcion prom <- PromedioMateria(nombreMateria)
	
	Definir n1, n2, n3 Como Real
	Definir error Como Logico
	
	error <- Falso
	prom <- -1
	
	Escribir ""
	Escribir "=== ", nombreMateria, " ==="
	
	n1 <- LeerNota("  Ingrese nota 1:")
	Si n1 = -1 Entonces
		Escribir "Demasiados errores. Proceso cancelado."
		error <- Verdadero
	FinSi
	
	Si error = Falso Entonces
		n2 <- LeerNota("  Ingrese nota 2:")
		Si n2 = -1 Entonces
			Escribir "Demasiados errores. Proceso cancelado."
			error <- Verdadero
		FinSi
	FinSi
	
	Si error = Falso Entonces
		n3 <- LeerNota("  Ingrese nota 3:")
		Si n3 = -1 Entonces
			Escribir "Demasiados errores. Proceso cancelado."
			error <- Verdadero
		FinSi
	FinSi
	
	Si error = Falso Entonces
		prom <- (n1 + n2 + n3) / 3
		Escribir "  Promedio ", nombreMateria, ": ", prom
	FinSi
	
FinFuncion


// ============================================================
//  SUBPROCESO: MostrarResultados
//  Muestra los promedios por materia y el promedio final.
// ============================================================
SubProceso MostrarResultados(p1, p2, p3, p4, p5, ingresadas)
	
	Definir promFinal Como Real
	
	Escribir ""
	Escribir "======= RESULTADOS ======="
	
	Si ingresadas = Falso Entonces
		
		Escribir "Promedio Calculo 1           : 0"
		Escribir "Promedio Algebra Lineal      : 0"
		Escribir "Promedio Ingles              : 0"
		Escribir "Promedio COYE                : 0"
		Escribir "Promedio Algoritmia y Prog.  : 0"
		Escribir "---------------------------"
		Escribir "PROMEDIO FINAL               : 0"
		
	SiNo
		
		promFinal <- (p1 + p2 + p3 + p4 + p5) / 5
		
		Escribir "Promedio Calculo 1           : ", p1
		Escribir "Promedio Algebra Lineal      : ", p2
		Escribir "Promedio Ingles              : ", p3
		Escribir "Promedio COYE                : ", p4
		Escribir "Promedio Algoritmia y Prog.  : ", p5
		Escribir "---------------------------"
		Escribir "PROMEDIO FINAL               : ", promFinal
		
		Si promFinal >= 3 Entonces
			Escribir ">>> APROBADO <<<"
		SiNo
			Escribir ">>> REPROBADO <<<"
		FinSi
		
	FinSi
	
	Escribir "==========================="
	Escribir ""
	
FinSubProceso


// ============================================================
//  ALGORITMO PRINCIPAL
// ============================================================
Algoritmo PromedioEstudianteDC
	
	Definir opc Como Entero
	Definir prom1, prom2, prom3, prom4, prom5 Como Real
	Definir ingresadas Como Logico
	
	opc <- 0
	ingresadas <- Falso
	prom1 <- 0
	prom2 <- 0
	prom3 <- 0
	prom4 <- 0
	prom5 <- 0
	
	Mientras opc <> 3 Hacer
		
		Escribir "-------- MENU ---------"
		Escribir "1. Ingresar notas"
		Escribir "2. Ver promedio"
		Escribir "3. Salir"
		Leer opc
		
		Si opc = 1 Entonces
			
			prom1 <- PromedioMateria("CALCULO 1")
			
			Si prom1 <> -1 Entonces
				prom2 <- PromedioMateria("ALGEBRA LINEAL")
			FinSi
			
			Si prom1 <> -1 Y prom2 <> -1 Entonces
				prom3 <- PromedioMateria("INGLES")
			FinSi
			
			Si prom1 <> -1 Y prom2 <> -1 Y prom3 <> -1 Entonces
				prom4 <- PromedioMateria("COYE")
			FinSi
			
			Si prom1 <> -1 Y prom2 <> -1 Y prom3 <> -1 Y prom4 <> -1 Entonces
				prom5 <- PromedioMateria("ALGORITMIA Y PROGRAMACION")
			FinSi
			
			Si prom1 = -1 O prom2 = -1 O prom3 = -1 O prom4 = -1 O prom5 = -1 Entonces
				Escribir "Se superaron los errores permitidos. Saliendo..."
				opc <- 3
			SiNo
				ingresadas <- Verdadero
				Escribir ""
				Escribir "Notas ingresadas correctamente."
			FinSi
			
		SiNo
			
			Si opc = 2 Entonces
				
				MostrarResultados(prom1, prom2, prom3, prom4, prom5, ingresadas)
				
			SiNo
				
				Si opc = 3 Entonces
					Escribir "Hasta luego."
				SiNo
					Escribir "Opcion invalida. Ingrese 1, 2 o 3."
				FinSi
				
			FinSi
			
		FinSi
		
	FinMientras
	
FinAlgoritmo
