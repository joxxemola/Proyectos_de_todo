# IMPORTACIONES DE LIBRERÍAS
import tkinter as tk                    # Crea la interfaz gráfica y ventanas
from random import randint              # Genera números aleatorios (posiciones, velocidades)
from PIL import Image, ImageTk          # Carga y redimensiona imágenes PNG
import os                               # Maneja rutas de archivos (para imágenes/sonidos)
import pygame                           # Reproduce música y efectos de sonido

# CONFIGURACIÓN DE LA VENTANA PRINCIPAL
ventana = tk.Tk()                       # Crea la ventana principal del juego
ventana.title("La Gallina y los Huevos de Oro")  # Establece el título de la ventana

# CREA EL ÁREA DE DIBUJO (LIENZO)
canvas = tk.Canvas(ventana, width=600, height=500, bg='#1a0a00')  # Crea un lienzo de 600x500 con fondo marrón oscuro
canvas.pack()                           # Coloca el lienzo dentro de la ventana

# OBTIENE LA RUTA DE LA CARPETA DEL PROYECTO
carpeta = os.path.dirname(__file__)     # Obtiene la carpeta donde está guardado el script

# RUTAS DE LAS IMÁGENES
ruta_gallina = os.path.join(carpeta, "gallina.PNG")  # Ruta de la imagen de la gallina
ruta_huevo   = os.path.join(carpeta, "huevo.PNG")    # Ruta de la imagen del huevo
ruta_pelota  = os.path.join(carpeta, "pelota.PNG")   # Ruta de la imagen de la pelota (obstáculo)
ruta_fondo   = os.path.join(carpeta, "fondo.png")    # Ruta de la imagen de fondo

# CONFIGURACIÓN DE SONIDOS CON PYGAME
pygame.mixer.init()                     # Inicializa el sistema de sonido de pygame
sonido_punto = pygame.mixer.Sound(os.path.join(carpeta, "Win.mp3"))  # Carga el sonido de ganar (no se usa realmente)
sonido_muerte = pygame.mixer.Sound(os.path.join(carpeta, "Game Over.mp3"))  # Carga el sonido de game over
sonido_huevo  = pygame.mixer.Sound(os.path.join(carpeta, "Huevo.mp3"))  # Carga el sonido al recoger huevo
pygame.mixer.music.load(os.path.join(carpeta, "Musica Ciudad.mp3"))  # Carga la música de fondo
pygame.mixer.music.set_volume(0.5)      # Establece el volumen de la música al 50%

# CONSTANTES DEL JUEGO
JUGADOR_Y      = 445                    # Posición Y fija de la gallina
VELOCIDAD      = 8                      # Velocidad de movimiento de la gallina
TAM_GALLINA    = 70                     # Tamaño de la imagen de la gallina (ancho y alto)
TAM_HUEVO      = 20                     # Tamaño de la imagen del huevo
TAM_PELOTA     = 40                     # Tamaño de la imagen de la pelota
MAX_PELOTAS    = 5                      # Número máximo de pelotas en pantalla
MAX_HUEVOS     = 2                      # Número máximo de huevos en pantalla
VIDAS_INICIALES = 1                     # Vidas al comenzar (solo 1)
HUEVOS_PARA_GANAR = 10                  # Huevos necesarios para ganar

# CARGA Y REDIMENSIONA LAS IMÁGENES
img_fondo  = Image.open(ruta_fondo).resize((600, 500), Image.LANCZOS)  # Abre el fondo y lo redimensiona a 600x500
fondo_img  = ImageTk.PhotoImage(img_fondo)  # Convierte la imagen para usarla en tkinter

img_gallina = Image.open(ruta_gallina).resize((TAM_GALLINA, TAM_GALLINA), Image.LANCZOS)  # Redimensiona gallina
gallina_img = ImageTk.PhotoImage(img_gallina)  # Convierte gallina para tkinter

img_huevo  = Image.open(ruta_huevo).resize((TAM_HUEVO, TAM_HUEVO), Image.LANCZOS)  # Redimensiona huevo
huevo_img  = ImageTk.PhotoImage(img_huevo)  # Convierte huevo para tkinter

img_pelota = Image.open(ruta_pelota).resize((TAM_PELOTA, TAM_PELOTA), Image.LANCZOS)  # Redimensiona pelota
pelota_img = ImageTk.PhotoImage(img_pelota)  # Convierte pelota para tkinter

# VARIABLES GLOBALES DEL JUEGO
jugador = {"x": 275, "y": JUGADOR_Y, "vel_x": 0, "figura": None}  # Datos de la gallina: posición, velocidad y su imagen en canvas
pelotas = []                            # Lista para guardar todas las pelotas (obstáculos)
huevos  = []                            # Lista para guardar todos los huevos
puntos  = 0                             # Contador de puntos (huevos recogidos)
vidas   = VIDAS_INICIALES               # Vidas actuales del jugador
juego_activo   = False                  # Indica si el juego está en curso
texto_vidas    = None                   # Referencia al texto de vidas en el canvas
texto_puntos   = None                   # Referencia al texto de puntos en el canvas
elementos_inicio = []                   # Lista de elementos de la pantalla de inicio

# FUNCIÓN PARA MOSTRAR PANTALLA DE INICIO
def mostrar_pantalla_inicio():
    canvas.create_image(0, 0, image=fondo_img, anchor="nw")  # Dibuja el fondo
    overlay = canvas.create_rectangle(0, 0, 600, 500, fill="#0d0500", stipple="gray50", outline="")  # Capa semitransparente oscura
    panel   = canvas.create_rectangle(120, 130, 480, 390, fill="#1a0a00", outline="#FFD700", width=3)  # Panel central dorado
    titulo  = canvas.create_text(300, 195, text="Huevos en", fill="#FFD700", font=('Arial', 22, 'bold'))  # Texto título parte 1
    titulo2 = canvas.create_text(300, 235, text="Fuga",      fill="#FFD700", font=('Arial', 22, 'bold'))  # Texto título parte 2
    instr   = canvas.create_text(300, 285, text="← → para mover   |   ¡Recoge 10 huevos!", fill="#CCCCCC", font=('Arial', 11))  # Instrucciones
    instr2  = canvas.create_text(300, 310, text="¡Evita las pelotas o perderás!", fill="#FF6666", font=('Arial', 11))  # Advertencia

    btn_jugar = tk.Button(               # Crea botón de jugar
        ventana, text="▶  JUGAR",
        font=('Arial', 16, 'bold'),
        bg="#FFD700", fg="#1a0a00",
        activebackground="#FFA500", activeforeground="#1a0a00",
        relief="flat", padx=24, pady=10,
        cursor="hand2", command=iniciar_juego  # Al hacer click, llama a iniciar_juego
    )
    btn_window = canvas.create_window(300, 355, window=btn_jugar)  # Coloca el botón en el canvas
    elementos_inicio.extend([overlay, panel, titulo, titulo2, instr, instr2, btn_window])  # Guarda elementos para borrarlos después

# FUNCIÓN PARA INICIAR EL JUEGO
def iniciar_juego():
    global juego_activo, texto_vidas, texto_puntos
    for elem in elementos_inicio:       # Borra todos los elementos de la pantalla de inicio
        canvas.delete(elem)
    elementos_inicio.clear()            # Limpia la lista
    canvas.create_image(0, 0, image=fondo_img, anchor="nw")  # Dibuja el fondo
    
    texto_vidas, texto_puntos = crear_hud()  # Crea el HUD (vidas y puntos)
    crear_gallina()                   # Crea la gallina en el canvas
    for _ in range(MAX_PELOTAS):      # Crea todas las pelotas (obstáculos)
        crear_pelota()
    for _ in range(MAX_HUEVOS):       # Crea todos los huevos
        crear_huevo()
    
    ventana.bind('<KeyPress>',   mover_jugador)   # Detecta cuando se presiona una tecla
    ventana.bind('<KeyRelease>', detener_movimiento)  # Detecta cuando se suelta una tecla
    
    pygame.mixer.music.play(-1)       # Reproduce música en bucle infinito (-1)
    juego_activo = True               # Activa el juego
    actualizar()                      # Comienza el bucle de actualización

# FUNCIÓN PARA REINICIAR EL JUEGO COMPLETAMENTE
def reiniciar_juego():
    global puntos, vidas, juego_activo, texto_vidas, texto_puntos
    puntos = 0                        # Reinicia los puntos
    vidas  = VIDAS_INICIALES          # Reinicia las vidas
    juego_activo = False              # Desactiva el juego actual
    jugador["x"]     = 275            # Reinicia posición X de la gallina
    jugador["vel_x"] = 0              # Reinicia velocidad
    jugador["figura"] = None          # Limpia referencia de la figura
    
    for p in pelotas:                 # Elimina todas las pelotas del canvas
        canvas.delete(p["figura"])
    pelotas.clear()                   # Vacía la lista de pelotas
    
    for h in huevos:                  # Elimina todos los huevos del canvas
        canvas.delete(h["figura"])
    huevos.clear()                    # Vacía la lista de huevos
    
    canvas.delete("all")              # Limpia todo el canvas
    canvas.create_image(0, 0, image=fondo_img, anchor="nw")  # Redibuja fondo
    
    texto_vidas, texto_puntos = crear_hud()  # Recrea el HUD
    crear_gallina()                   # Recrea la gallina
    for _ in range(MAX_PELOTAS):      # Recrea las pelotas
        crear_pelota()
    for _ in range(MAX_HUEVOS):       # Recrea los huevos
        crear_huevo()
    
    pygame.mixer.music.play(-1)       # Reinicia la música
    juego_activo = True               # Activa el juego
    actualizar()                      # Comienza actualización

# FUNCIÓN PARA CREAR LA GALLINA EN EL CANVAS
def crear_gallina():
    jugador["figura"] = canvas.create_image(jugador["x"], jugador["y"], image=gallina_img)  # Dibuja la gallina

# FUNCIÓN PARA MOVER LA GALLINA (ACTUALIZA SU POSICIÓN GRÁFICA)
def mover_gallina_grafica():
    canvas.coords(jugador["figura"], jugador["x"], jugador["y"])  # Actualiza coordenadas de la imagen

# FUNCIÓN PARA CREAR UNA PELOTA (OBSTÁCULO)
def crear_pelota():
    x = randint(20, 560)              # Posición X aleatoria
    y = randint(-120, -30)            # Posición Y arriba de la pantalla (fuera)
    vel = randint(2, 6)               # Velocidad de caída aleatoria
    figura = canvas.create_image(x, y, image=pelota_img)  # Dibuja la pelota
    pelotas.append({"x": x, "y": y, "vel_y": vel, "figura": figura})  # Guarda sus datos

# FUNCIÓN PARA CREAR UN HUEVO
def crear_huevo():
    x = randint(20, 560)              # Posición X aleatoria
    y = randint(-120, -30)            # Posición Y arriba (fuera)
    vel = randint(1, 4)               # Velocidad de caída aleatoria (más lenta que pelotas)
    figura = canvas.create_image(x, y, image=huevo_img)   # Dibuja el huevo
    huevos.append({"x": x, "y": y, "vel_y": vel, "figura": figura})  # Guarda sus datos

# FUNCIÓN PARA CREAR EL HUD (Vidas y Puntos)
def crear_hud():
    canvas.create_rectangle(0, 0, 600, 50, fill="#2d1400", outline="")  # Barra superior oscura
    canvas.create_text(60,  25, text="VIDAS:",  fill="#FF6666", font=('Arial', 13, 'bold'))  # Etiqueta "VIDAS"
    canvas.create_text(340, 25, text="PUNTOS:", fill="#FFD700", font=('Arial', 13, 'bold'))  # Etiqueta "PUNTOS"
    tv = canvas.create_text(160, 25, text=str(VIDAS_INICIALES), fill="white", font=('Arial', 14, 'bold'))  # Texto con número de vidas
    tp = canvas.create_text(430, 25, text="0", fill="white", font=('Arial', 14, 'bold'))  # Texto con puntos
    return tv, tp                     # Retorna referencias para actualizarlos después

# FUNCIÓN PARA MOVER EL JUGADOR (CUANDO SE PRESIONA TECLA)
def mover_jugador(event):
    if not juego_activo:              # Si el juego no está activo, no hace nada
        return
    if event.keysym == 'Left':        # Si presiona flecha izquierda
        jugador["vel_x"] = -VELOCIDAD  # Velocidad negativa (mover a la izquierda)
    elif event.keysym == 'Right':     # Si presiona flecha derecha
        jugador["vel_x"] = VELOCIDAD   # Velocidad positiva (mover a la derecha)

# FUNCIÓN PARA DETENER EL MOVIMIENTO (CUANDO SE SUELTA LA TECLA)
def detener_movimiento(event):
    if event.keysym in ('Left', 'Right'):  # Si soltó flecha izquierda o derecha
        jugador["vel_x"] = 0          # Detiene el movimiento

# FUNCIÓN PARA VERIFICAR COLISIONES ENTRE RECTÁNGULOS
def colision_rect(cj, co):            # cj = coordenadas jugador, co = coordenadas objeto
    return (cj[0] < co[2] and cj[2] > co[0] and cj[1] < co[3] and cj[3] > co[1])  # Detecta si dos rectángulos se tocan

# FUNCIÓN PRINCIPAL PARA VERIFICAR TODAS LAS COLISIONES
def verificar_colisiones():
    global puntos, vidas, juego_activo
    cj = canvas.bbox(jugador["figura"])  # Obtiene el rectángulo (x1,y1,x2,y2) de la gallina
    
    # Verifica colisiones con pelotas
    for p in pelotas[:]:              # [:] crea copia para poder modificar la lista mientras se recorre
        co = canvas.bbox(p["figura"]) # Obtiene rectángulo de la pelota
        if colision_rect(cj, co):     # Si hay colisión
            canvas.delete(p["figura"]) # Elimina la pelota del canvas
            pelotas.remove(p)         # Elimina la pelota de la lista
            vidas -= 1                # Resta una vida
            canvas.itemconfig(texto_vidas, text=str(vidas))  # Actualiza el texto de vidas
            if vidas <= 0:            # Si no quedan vidas
                juego_activo = False  # Desactiva el juego
                pygame.mixer.music.stop()  # Detiene la música
                sonido_muerte.play()  # Reproduce sonido de game over
                game_over()           # Muestra pantalla de game over
                return
            crear_pelota()            # Crea una nueva pelota para reemplazar la eliminada
    
    # Verifica colisiones con huevos
    for h in huevos[:]:               # [:] crea copia para poder modificar
        co = canvas.bbox(h["figura"]) # Obtiene rectángulo del huevo
        if colision_rect(cj, co):     # Si hay colisión
            canvas.delete(h["figura"]) # Elimina el huevo del canvas
            huevos.remove(h)          # Elimina el huevo de la lista
            puntos += 1               # Aumenta los puntos
            sonido_huevo.play()       # Reproduce sonido de recoger huevo
            canvas.itemconfig(texto_puntos, text=str(puntos))  # Actualiza puntos
            
            if puntos >= HUEVOS_PARA_GANAR:  # Si alcanzó los huevos necesarios
                juego_activo = False   # Desactiva el juego
                ganar_juego()          # Muestra pantalla de victoria
                return
            crear_huevo()             # Crea un nuevo huevo

# FUNCIÓN PARA MOSTRAR PANTALLA DE VICTORIA
def ganar_juego():
    canvas.create_rectangle(100, 180, 500, 320, fill="#1a0a00", outline="#FFD700", width=3)  # Panel dorado
    canvas.create_text(300, 215, text="🏆 ¡GANASTE! 🏆", fill="#FFD700", font=('Arial', 30, 'bold'))  # Texto de victoria
    canvas.create_text(300, 260, text=f"¡Recogiste {puntos} huevos de oro!", fill="white", font=('Arial', 14))  # Muestra puntos obtenidos
    
    btn = tk.Button(                  # Botón para jugar de nuevo
        ventana, text="▶  JUGAR DE NUEVO",
        font=('Arial', 13, 'bold'),
        bg="#FFD700", fg="#1a0a00",
        activebackground="#FFA500", activeforeground="#1a0a00",
        relief="flat", padx=16, pady=8,
        cursor="hand2", command=reiniciar_juego
    )
    canvas.create_window(300, 300, window=btn)  # Coloca el botón

# FUNCIÓN PARA MOSTRAR PANTALLA DE GAME OVER
def game_over():
    canvas.create_rectangle(100, 160, 500, 340, fill="#1a0a00", outline="#FF4444", width=3)  # Panel rojo
    canvas.create_text(300, 205, text=" GAME OVER ", fill="red",  font=('Arial', 30, 'bold'))  # Texto game over
    canvas.create_text(300, 250, text=f"Huevos recogidos: {puntos}", fill="gold", font=('Arial', 14))  # Muestra puntos
    
    btn_reiniciar = tk.Button(        # Botón para reiniciar
        ventana, text="🔄  VOLVER A JUGAR",
        font=('Arial', 13, 'bold'),
        bg="#FF4444", fg="white",
        activebackground="#CC0000", activeforeground="white",
        relief="flat", padx=16, pady=8,
        cursor="hand2", command=reiniciar_juego
    )
    canvas.create_window(300, 300, window=btn_reiniciar)  # Coloca el botón

# FUNCIÓN PRINCIPAL DE ACTUALIZACIÓN (LOOP DEL JUEGO)
def actualizar():
    if not juego_activo:              # Si el juego no está activo, no actualiza
        return
    
    # MOVIMIENTO DEL JUGADOR
    jugador["x"] = max(45, min(jugador["x"] + jugador["vel_x"], 555))  # Actualiza X, limitando bordes (45-555)
    mover_gallina_grafica()           # Actualiza la posición gráfica de la gallina
    
    # MOVIMIENTO DE PELOTAS
    for p in pelotas:
        p["y"] += p["vel_y"]          # Mueve la pelota hacia abajo
        if p["y"] > 520:              # Si sale de la pantalla por abajo
            p["y"] = randint(-120, -30)  # Reinicia arriba de la pantalla
            p["x"] = randint(20, 560)    # Nueva posición X aleatoria
        canvas.coords(p["figura"], p["x"], p["y"])  # Actualiza gráficamente
    
    # MOVIMIENTO DE HUEVOS
    for h in huevos:
        h["y"] += h["vel_y"]          # Mueve el huevo hacia abajo
        if h["y"] > 520:              # Si sale de la pantalla
            h["y"] = randint(-120, -30)  # Reinicia arriba
            h["x"] = randint(20, 560)    # Nueva posición X
        canvas.coords(h["figura"], h["x"], h["y"])  # Actualiza gráficamente
    
    verificar_colisiones()            # Verifica colisiones entre gallina y objetos
    ventana.after(16, actualizar)     # Llama a actualizar nuevamente después de 16ms (~60 FPS)

# INICIO DEL PROGRAMA
mostrar_pantalla_inicio()             # Muestra la pantalla de inicio
ventana.mainloop()                    # Inicia el bucle principal de la ventana (mantiene el programa corriendo)