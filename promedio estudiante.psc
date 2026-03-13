Proceso PromedioEstudiante
	
	Definir opcion Como Entero
	Definir nota Como Real
	Definir promMateria Como Real
	Definir promEstudiante Como Real
	Definir sumatoria Como Real
	Definir intentos Como Entero
	Definir i Como Entero
	Definir j Como Entero
	Definir notaValida Como Logico
	Definir notasIngresadas Como Logico
	
	Dimension notas[5,3]
	Dimension promedios[5]
	Dimension materias[5]
	
	// Inicializar arreglo de materias
	materias[1] <- "Calculo 1"
	materias[2] <- "Algebra Lineal"
	materias[3] <- "Ingles"
	materias[4] <- "COYE"
	materias[5] <- "Algoritmos y Programacion"
	
	// Inicializar arreglo de promedios
	Para i <- 1 Hasta 5 Con Paso 1 Hacer
		promedios[i] <- -1  
	FinPara
	
	notasIngresadas <- Falso
	opcion <- 0
	
	Repetir
		Escribir "------------- SISTEMA DE NOTAS -------------"
		Escribir "  1. Ingresar notas"
		Escribir "  2. Promedio estudiante"
		Escribir "  3. Salir"
		Escribir "Seleccione una opcion: "
		Leer opcion
		
		Segun opcion Hacer
			1:
				Escribir ""
				Escribir "--- INGRESO DE NOTAS ---"
				Escribir ""
				
				Para i <- 1 Hasta 5 Con Paso 1 Hacer
					Escribir ">>> Materia ", i, ": ", materias[i]
					
					Para j <- 1 Hasta 3 Con Paso 1 Hacer
						
						intentos <- 0
						notaValida <- Falso
						
						Repetir
							
							intentos <- intentos + 1
							
							Si intentos > 3 Entonces
								
								Escribir ""
								Escribir "ERROR: Ha superado los 3 intentos permitidos."
								Escribir "El programa se cerrara."
								Escribir ""
								Escribir "Presione ENTER para salir..."
								Leer opcion
								// Forzar salida del programa
								opcion <- 3
								j <- 4     // Salir del bucle de notas
								i <- 6     // Salir del bucle de materias
								notaValida <- Verdadero  // Salir del Repetir
							SiNo
								Escribir "  Nota ", j, " (Intento ", intentos, "/3): "
								Leer nota
								
								Si nota >= 0 Y nota <= 5 Entonces
									notas[i,j] <- nota
									notaValida <- Verdadero
								SiNo
									Escribir "  !! NOTA INVALIDA !! La nota debe estar entre 0 y 5."
									Escribir "     Intentos restantes: ", 3 - intentos
								FinSi
							FinSi
							
						Hasta Que notaValida = Verdadero
						
					FinPara
					
					// Calcular promedio de la materia (solo si no hubo error fatal)
					Si i <= 5 Entonces
						promedios[i] <- (notas[i,1] + notas[i,2] + notas[i,3]) / 3
						Escribir "  Promedio de ", materias[i], ": ", promedios[i]
						Escribir ""
					FinSi
					
				FinPara
				
				// Verificar que se completaron todas las materias
				Si opcion <> 3 Entonces
					notasIngresadas <- Verdadero
					Escribir ">>> Notas registradas exitosamente para todas las materias."
				FinSi
				
			2:
				Escribir ""
				Si notasIngresadas = Falso Entonces
					Escribir "ADVERTENCIA: Aun no ha ingresado las notas."
					Escribir "Por favor seleccione la opcion 1 primero."
				SiNo
					Escribir "============================================"
					Escribir "       REPORTE DE NOTAS DEL ESTUDIANTE      "
					Escribir "============================================"
					
					sumatoria <- 0
					
					Para i <- 1 Hasta 5 Con Paso 1 Hacer
						Escribir ""
						Escribir "Materia: ", materias[i]
						Escribir "  Nota 1: ", notas[i,1]
						Escribir "  Nota 2: ", notas[i,2]
						Escribir "  Nota 3: ", notas[i,3]
						Escribir "  Promedio: ", promedios[i]
						sumatoria <- sumatoria + promedios[i]
					FinPara
					
					promEstudiante <- sumatoria / 5
					
					Escribir ""
					Escribir "============================================"
					Escribir "  PROMEDIO TOTAL DEL ESTUDIANTE: ", promEstudiante
					
					Si promEstudiante >= 3.0 Entonces
						Escribir "  ESTADO: APROBADO"
					SiNo
						Escribir "  ESTADO: REPROBADO"
					FinSi
					
					Escribir "============================================"
				FinSi
				
			3:
				Escribir ""
				Escribir "Gracias por usar el sistema. Hasta luego!"
				Escribir ""
				
			De Otro Modo:
				Escribir ""
				Escribir "Opcion no valida. Por favor ingrese 1, 2 o 3."
		FinSegun
		
	Hasta Que opcion = 3
	
FinProceso