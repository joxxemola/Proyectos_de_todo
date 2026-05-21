import tkinter as tk
from random import randint
from PIL import Image, ImageTk
import os
import pygame

ventana = tk.Tk()
ventana.title("Huevos en fuga")

canvas = tk.Canvas(ventana, width=600, height=500, bg='#1a0a00')
canvas.pack()

carpeta = os.path.dirname(__file__)

ruta_gallina = os.path.join(carpeta,"gallina.PNG")
ruta_huevo   = os.path.join(carpeta,"huevo.PNG")
ruta_pelota  = os.path.join(carpeta,"pelota.PNG")
ruta_fondo   = os.path.join(carpeta,"fondo.PNG")
ruta_carro   = os.path.join(carpeta,"carro.png")

pygame.mixer.init()
sonido_punto = pygame.mixer.Sound(os.path.join(carpeta,"Win.mp3"))
sonido_muerte = pygame.mixer.Sound(os.path.join(carpeta,"Game Over.mp3"))
sonido_huevo  = pygame.mixer.Sound(os.path.join(carpeta,"Huevo.mp3"))
pygame.mixer.music.load(os.path.join(carpeta,"Musica Ciudad.mp3"))
pygame.mixer.music.set_volume(0.5)

JUGADOR_Y      = 445
VELOCIDAD      = 8
TAM_GALLINA    = 70
TAM_HUEVO      = 20
TAM_PELOTA     = 40
MAX_PELOTAS    = 5
MAX_HUEVOS     = 2
VIDAS_INICIALES = 1
HUEVOS_PARA_GANAR = 5
TAM_CARRO_AL = 65
TAM_CARRO_AH = 95
MAX_CARRO = 4
CARRILES = [330, 380]  

img_fondo  = Image.open(ruta_fondo).resize((600, 500), Image.LANCZOS)
fondo_img  = ImageTk.PhotoImage(img_fondo)

img_gallina_der = Image.open(ruta_gallina).resize((TAM_GALLINA, TAM_GALLINA), Image.LANCZOS)
img_gallina_izq = img_gallina_der.transpose(Image.FLIP_LEFT_RIGHT) #transpose/es el método de Pillow que espeja una imagen horizontalmente.
gallina_der_img = ImageTk.PhotoImage(img_gallina_der)
gallina_izq_img = ImageTk.PhotoImage(img_gallina_izq)

img_huevo  = Image.open(ruta_huevo).resize((TAM_HUEVO, TAM_HUEVO), Image.LANCZOS)
huevo_img  = ImageTk.PhotoImage(img_huevo)
img_pelota = Image.open(ruta_pelota).resize((TAM_PELOTA, TAM_PELOTA), Image.LANCZOS)
pelota_img = ImageTk.PhotoImage(img_pelota)

img_carro_der = Image.open(ruta_carro).resize((TAM_CARRO_AH, TAM_CARRO_AL), Image.LANCZOS)
img_carro_izq = img_carro_der.transpose(Image.FLIP_LEFT_RIGHT)
carro_der_img = ImageTk.PhotoImage(img_carro_der)
carro_izq_img = ImageTk.PhotoImage(img_carro_izq)

jugador = {"x": 275, "y": JUGADOR_Y, "vel_x": 0, "figura": None}
pelotas = []
huevos  = []
puntos  = 0
vidas   = VIDAS_INICIALES
juego_activo   = False
texto_vidas    = None
texto_puntos   = None
elementos_inicio = []
carro = []

def mostrar_pantalla_inicio():
    canvas.create_image(0, 0, image=fondo_img, anchor="nw")
    overlay = canvas.create_rectangle(0, 0, 600, 500, fill="#0d0500", stipple="gray50", outline="")
    panel   = canvas.create_rectangle(120, 130, 480, 390, fill="#1a0a00", outline="#FFD700", width=3)
    titulo  = canvas.create_text(300, 195, text="Huevos en", fill="#FFD700", font=('Arial', 22, 'bold'))
    titulo2 = canvas.create_text(300, 235, text="Fuga",      fill="#FFD700", font=('Arial', 22, 'bold'))
    instr   = canvas.create_text(300, 285, text="← → para mover   |   ¡Recoge 5 huevos!", fill="#CCCCCC", font=('Arial', 11))
    instr2  = canvas.create_text(300, 310, text="¡Evita las pelotas o perderás!", fill="#FF6666", font=('Arial', 11))

    btn_jugar = tk.Button(
        ventana, text="▶  JUGAR",
        font=('Arial', 16, 'bold'),
        bg="#FFD700", fg="#1a0a00",
        activebackground="#FFA500", activeforeground="#1a0a00",
        relief="flat", padx=24, pady=10,
        cursor="hand2", command=iniciar_juego
    )
    btn_window = canvas.create_window(300, 355, window=btn_jugar)
    elementos_inicio.extend([overlay, panel, titulo, titulo2, instr, instr2, btn_window])

def iniciar_juego():
    global juego_activo, texto_vidas, texto_puntos
    for elem in elementos_inicio:
        canvas.delete(elem)
    elementos_inicio.clear()
    canvas.create_image(0, 0, image=fondo_img, anchor="nw")
    texto_vidas, texto_puntos = crear_hud()
    crear_gallina()
    for y in CARRILES:
        crear_carro(y)
    for _ in range(MAX_PELOTAS):
        crear_pelota()
    for _ in range(MAX_HUEVOS):
        crear_huevo()
    ventana.bind('<KeyPress>',   mover_jugador)
    ventana.bind('<KeyRelease>', detener_movimiento)
    pygame.mixer.music.play(-1)
    juego_activo = True
    actualizar()

def reiniciar_juego():
    global puntos, vidas, juego_activo, texto_vidas, texto_puntos
    puntos = 0
    vidas  = VIDAS_INICIALES
    juego_activo = False
    jugador["x"]     = 275
    jugador["vel_x"] = 0
    jugador["figura"] = None
    for p in pelotas:
        canvas.delete(p["figura"])
    pelotas.clear()
    for h in huevos:
        canvas.delete(h["figura"])
    huevos.clear()
    for c in carro:
        canvas.delete(c["figura"])
    carro.clear()
    canvas.delete("all")
    canvas.create_image(0, 0, image=fondo_img, anchor="nw")
    texto_vidas, texto_puntos = crear_hud()
    crear_gallina()
    for y in CARRILES:
        crear_carro(y)
    for _ in range(MAX_PELOTAS):
        crear_pelota()
    for _ in range(MAX_HUEVOS):
        crear_huevo()
    pygame.mixer.music.play(-1)
    juego_activo = True
    actualizar()

def crear_gallina():
    jugador["figura"] = canvas.create_image(jugador["x"], jugador["y"], image=gallina_der_img)

def mover_gallina_grafica():
    canvas.coords(jugador["figura"], jugador["x"], jugador["y"])

def crear_pelota():
    x = randint(20, 560)
    y = randint(-120, -30)
    vel = randint(2, 6)
    figura = canvas.create_image(x, y, image=pelota_img)
    pelotas.append({"x": x, "y": y, "vel_y": vel, "figura": figura})

def crear_huevo():
    x = randint(20, 560)
    y = randint(-120, -30)
    vel = randint(1, 4)
    figura = canvas.create_image(x, y, image=huevo_img)
    huevos.append({"x": x, "y": y, "vel_y": vel, "figura": figura})

def crear_carro(carril_y):
    direccion = randint(0, 1)
    if direccion == 0:        # va a la derecha
        x   = randint(-200, -60)
        vel = randint(2, 4)
        img = carro_izq_img
    else:                     # va a la izquierda
        x   = randint(650, 780)
        vel = -randint(2, 4)
        img = carro_der_img
    figura = canvas.create_image(x, carril_y, image=img)
    carro.append({"x": x, "y": carril_y, "vel_x": vel, "figura": figura})

def crear_hud():
    canvas.create_rectangle(0, 0, 600, 50, fill="#2d1400", outline="")
    canvas.create_text(60,  25, text="VIDAS:",  fill="#FF6666", font=('Arial', 13, 'bold'))
    canvas.create_text(340, 25, text="PUNTOS:", fill="#FFD700", font=('Arial', 13, 'bold'))
    tv = canvas.create_text(160, 25, text=str(VIDAS_INICIALES), fill="white", font=('Arial', 14, 'bold'))
    tp = canvas.create_text(430, 25, text="0",                  fill="white", font=('Arial', 14, 'bold'))
    return tv, tp

def mover_jugador(event):
    if not juego_activo:
        return
    if event.keysym == 'Left':
        jugador["vel_x"] = -VELOCIDAD
        canvas.itemconfig(jugador["figura"], image=gallina_izq_img)
    elif event.keysym == 'Right':
        jugador["vel_x"] = VELOCIDAD
        canvas.itemconfig(jugador["figura"], image=gallina_der_img)

def detener_movimiento(event):
    if event.keysym in ('Left', 'Right'):
        jugador["vel_x"] = 0

def colision_rect(cj, co, margen=10):
    cj = (cj[0] + margen, cj[1] + margen, cj[2] - margen, cj[3] - margen)
    co = (co[0] + margen, co[1] + margen, co[2] - margen, co[3] - margen)
    return (cj[0] < co[2] and cj[2] > co[0] and cj[1] < co[3] and cj[3] > co[1])

def verificar_colisiones():
    global puntos, vidas, juego_activo
    cj = canvas.bbox(jugador["figura"])
    for p in pelotas[:]:
        co = canvas.bbox(p["figura"])
        if colision_rect(cj, co):
            canvas.delete(p["figura"])
            pelotas.remove(p)
            vidas -= 1
            canvas.itemconfig(texto_vidas, text=str(vidas))
            if vidas <= 0:
                juego_activo = False
                pygame.mixer.music.stop()
                sonido_muerte.play()
                game_over()
                return
            crear_pelota()
    for h in huevos[:]:
        co = canvas.bbox(h["figura"])
        if colision_rect(cj, co):
            canvas.delete(h["figura"])
            huevos.remove(h)
            puntos += 1
            sonido_huevo.play()
            canvas.itemconfig(texto_puntos, text=str(puntos))
            if puntos >= HUEVOS_PARA_GANAR:
                juego_activo = False
                ganar_juego()
                return
            crear_huevo()

def ganar_juego():
    canvas.create_rectangle(100, 180, 500, 320, fill="#1a0a00", outline="#FFD700", width=3)
    canvas.create_text(300, 215, text="🏆 ¡GANASTE! 🏆", fill="#FFD700", font=('Arial', 30, 'bold'))
    canvas.create_text(300, 260, text=f"¡Recogiste {puntos} huevos de oro!", fill="white", font=('Arial', 14))
    btn = tk.Button(
        ventana, text="▶  JUGAR DE NUEVO",
        font=('Arial', 13, 'bold'),
        bg="#FFD700", fg="#1a0a00",
        activebackground="#FFA500", activeforeground="#1a0a00",
        relief="flat", padx=16, pady=8,
        cursor="hand2", command=reiniciar_juego
    )
    canvas.create_window(300, 300, window=btn)

def game_over():
    canvas.create_rectangle(100, 160, 500, 340, fill="#1a0a00", outline="#FF4444", width=3)
    canvas.create_text(300, 205, text=" GAME OVER ", fill="red",  font=('Arial', 30, 'bold'))
    canvas.create_text(300, 250, text=f"Huevos recogidos: {puntos}", fill="gold", font=('Arial', 14))
    btn_reiniciar = tk.Button(
        ventana, text="🔄  VOLVER A JUGAR",
        font=('Arial', 13, 'bold'),
        bg="#FF4444", fg="white",
        activebackground="#CC0000", activeforeground="white",
        relief="flat", padx=16, pady=8,
        cursor="hand2", command=reiniciar_juego
    )
    canvas.create_window(300, 300, window=btn_reiniciar)

def actualizar():
    if not juego_activo:
        return
    jugador["x"] = max(45, min(jugador["x"] + jugador["vel_x"], 555))
    mover_gallina_grafica()
    for p in pelotas:
        p["y"] += p["vel_y"]
        if p["y"] > 520:
            p["y"] = randint(-120, -30)
            p["x"] = randint(20, 560)
        canvas.coords(p["figura"], p["x"], p["y"])
    for h in huevos:
        h["y"] += h["vel_y"]
        if h["y"] > 520:
            h["y"] = randint(-120, -30)
            h["x"] = randint(20, 560)
        canvas.coords(h["figura"], h["x"], h["y"])
    for c in carro:
        c["x"] += c["vel_x"]
        if c["x"] > 670:          # salió por la derecha
            c["x"] = -60
            c["vel_x"] = randint(2, 4)
            canvas.itemconfig(c["figura"], image=carro_izq_img)
        elif c["x"] < -120:       # salió por la izquierda
            c["x"] = 660
            c["vel_x"] = -randint(2, 4)
            canvas.itemconfig(c["figura"], image=carro_der_img)
        canvas.coords(c["figura"], c["x"], c["y"])
    
    verificar_colisiones()
    ventana.after(16, actualizar)

mostrar_pantalla_inicio()
ventana.mainloop()