import pygame
import random
import sys

pygame.init()

# ============================================================
#                     INICIALIZACIÓN AUDIO
# ============================================================
try:
    pygame.mixer.init()
except:
    print("Advertencia: pygame.mixer no pudo inicializarse.")

# Carga segura de música
def safe_load_music(path):
    try:
        pygame.mixer.music.load(path)
        return True
    except Exception as e:
        print(f"No se pudo cargar música '{path}': {e}")
        return False

# Carga segura de efectos de sonido
def safe_load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        print(f"No se pudo cargar sonido '{path}'.")
        return None

# Detener música actual
def stop_music():
    try:
        pygame.mixer.music.stop()
    except:
        pass

# Reproducir música con ruta y volumen
def reproducir_musica(path, volumen):
    stop_music()
    if safe_load_music(path):
        try:
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(-1)  # -1 = loop infinito
        except:
            pass

# Efectos
hit_sound = safe_load_sound("hit.wav")
score_sound = safe_load_sound("score.wav")

# ============================================================
#                        VENTANA PRINCIPAL
# ============================================================
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ping Pong Vertical")
reloj = pygame.time.Clock()

# ============================================================
#                          FONDOS
# ============================================================
def safe_load_image(path, size):
    """Carga una imagen de forma segura. Si falta, crea un fondo azul oscuro."""
    try:
        return pygame.transform.scale(pygame.image.load(path), size)
    except:
        s = pygame.Surface(size)
        s.fill((20, 20, 40))
        return s

fondos = {
    1: safe_load_image("nivel1_bg.png", (ANCHO, ALTO)),
    2: safe_load_image("nivel2_bg.png", (ANCHO, ALTO))
}

menu_bg = safe_load_image("menu_bg.png", (ANCHO, ALTO))

# ============================================================
#                         COLORES
# ============================================================
BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
GRIS_OSCURO = (80, 80, 80)
FONDO_FINAL = (15, 10, 25)

# ============================================================
#                       VARIABLES PALETAS
# ============================================================
ancho_paleta = 140
alto_paleta = 15
velocidad_jugador = 8
velocidad_cpu_base = 6  # velocidad CPU en nivel 1

# Posiciones iniciales
paleta_jugador_x = ANCHO//2 - ancho_paleta//2
paleta_jugador_y = ALTO - 60

paleta_cpu_x = ANCHO//2 - ancho_paleta//2
paleta_cpu_y = 80

# ============================================================
#                          PELOTA
# ============================================================
# Se usa diccionario para agrupar sus datos
pelota = {
    "x": ANCHO//2,
    "y": ALTO//2,
    "dx": 6,   # velocidad horizontal
    "dy": 6,   # velocidad vertical
    "r": 12    # radio
}

# ============================================================
#                      ESTADO DEL JUEGO
# ============================================================
puntos_jugador = 0
puntos_cpu = 0
nivel = 1
menu = True
juego_terminado = False
ganador = ""
pausa = False
velocidad_cpu = velocidad_cpu_base  # velocidad actual CPU

# ============================================================
#                       FUNCIONES ÚTILES
# ============================================================
def clamp(v, minv, maxv):
    """Limita un valor a un rango"""
    return max(minv, min(v, maxv))

def reset_velocidad_nivel():
    """Retorna la velocidad básica de pelota según el nivel"""
    return 5 if nivel == 1 else 7

def reiniciar_pelota():
    """Vuelve pelota al centro y restaura velocidad según nivel"""
    pelota["x"] = ANCHO//2
    pelota["y"] = ALTO//2
    vel = reset_velocidad_nivel()
    pelota["dx"] = vel
    pelota["dy"] = vel

def reset_juego():
    """Resetea paletas y pelota"""
    global paleta_cpu_x, paleta_jugador_x
    paleta_jugador_x = ANCHO//2 - ancho_paleta//2
    paleta_cpu_x = ANCHO//2 - ancho_paleta//2
    reiniciar_pelota()

def activar_nivel(num):
    """Activa nivel, configura velocidades y música"""
    global nivel, velocidad_cpu
    nivel = num

    # Ajustes de dificultad
    velocidad_cpu = velocidad_cpu_base if num == 1 else velocidad_cpu_base + 3

    # Música del nivel
    if num == 1:
        reproducir_musica("nivel1_music.wav", 0.7)
    else:
        reproducir_musica("nivel2_music.wav", 0.8)

    reset_juego()

def boton(texto, x, y, w, h, mouse, big=False):
    """
    Dibuja un botón interactivo.
    Retorna True si el mouse está encima.
    """
    dentro = x <= mouse[0] <= x + w and y <= mouse[1] <= y + h
    color = GRIS if dentro else GRIS_OSCURO

    pygame.draw.rect(ventana, color, (x, y, w, h), border_radius=18)

    fuente = pygame.font.SysFont(None, 50 if big else 40)
    img = fuente.render(texto, True, BLANCO)
    ventana.blit(img, (x + w//2 - img.get_width()//2,
                       y + h//2 - img.get_height()//2))
    return dentro

# Música principal (menú)
reproducir_musica("menu_music.wav", 0.6)

# ============================================================
#                     LOOP PRINCIPAL DEL JUEGO
# ============================================================
while True:

    # ---------------------------------------------------------
    #                LECTURA DE EVENTOS
    # ---------------------------------------------------------
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ---------------------- CLIC EN MENÚ ----------------------
        if menu and ev.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if boton("Nivel 1", 250, 230, 300, 70, (mx, my)):
                activar_nivel(1)
                menu = False

            if boton("Nivel 2", 250, 330, 300, 70, (mx, my)):
                activar_nivel(2)
                menu = False

        # -------------------- CLIC EN FIN DEL JUEGO --------------------
        if juego_terminado and ev.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if boton("VOLVER AL MENÚ", ANCHO//2 - 150, 360, 300, 70, (mx, my)):
                puntos_cpu = puntos_jugador = 0
                juego_terminado = False
                menu = True
                reproducir_musica("menu_music.wav", 0.6)

        # ---------------------- PAUSA ----------------------
        if ev.type == pygame.KEYDOWN and not menu and not juego_terminado:
            if ev.key == pygame.K_p:
                pausa = not pausa

    # ---------------------------------------------------------
    #                    PANTALLA DE MENÚ
    # ---------------------------------------------------------
    if menu:
        ventana.blit(menu_bg, (0, 0))

        fuente = pygame.font.SysFont(None, 60)
        ventana.blit(fuente.render("Ping - Pong", True, BLANCO), (ANCHO//2 - 200, 120))

        mouse = pygame.mouse.get_pos()
        boton("Nivel 1", 250, 230, 300, 70, mouse)
        boton("Nivel 2", 250, 330, 300, 70, mouse)

        pygame.display.flip()
        reloj.tick(60)
        continue

    # ---------------------------------------------------------
    #                 PANTALLA DE FIN DE PARTIDA
    # ---------------------------------------------------------
    if juego_terminado:
        ventana.fill(FONDO_FINAL)

        # Texto GANASTE / PERDISTE
        fuente = pygame.font.SysFont(None, 100)
        txt = fuente.render(ganador, True, BLANCO)
        ventana.blit(txt, (ANCHO//2 - txt.get_width()//2, 200))

        mouse = pygame.mouse.get_pos()
        boton("VOLVER AL MENÚ", ANCHO//2 - 150, 360, 300, 70, mouse, big=True)

        pygame.display.flip()
        reloj.tick(60)
        continue

    # ---------------------------------------------------------
    #                        PAUSA
    # ---------------------------------------------------------
    if pausa:
        ventana.blit(fondos[nivel], (0, 0))

        # Dibujar paletas y pelota congeladas
        pygame.draw.rect(ventana, BLANCO, (int(paleta_jugador_x), paleta_jugador_y, ancho_paleta, alto_paleta), border_radius=8)
        pygame.draw.rect(ventana, BLANCO, (int(paleta_cpu_x), paleta_cpu_y, ancho_paleta, alto_paleta), border_radius=8)
        pygame.draw.circle(ventana, BLANCO, (int(pelota["x"]), int(pelota["y"])), pelota["r"])

        # Overlay oscuro
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((10, 10, 10, 180))
        ventana.blit(s, (0, 0))

        fuente = pygame.font.SysFont(None, 80)
        ventana.blit(fuente.render("PAUSA", True, BLANCO), (ANCHO//2 - 120, ALTO//2 - 40))

        pygame.display.flip()
        reloj.tick(60)
        continue

    # ---------------------------------------------------------
    #                 CONTROLES DEL JUGADOR
    # ---------------------------------------------------------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paleta_jugador_x > 0:
        paleta_jugador_x -= velocidad_jugador
    if keys[pygame.K_RIGHT] and paleta_jugador_x < ANCHO - ancho_paleta:
        paleta_jugador_x += velocidad_jugador

    # ---------------------------------------------------------
    #                MOVIMIENTO DE LA PELOTA
    # ---------------------------------------------------------
    pelota["x"] += pelota["dx"]
    pelota["y"] += pelota["dy"]

    # Rebote con paredes laterales
    if pelota["x"] - pelota["r"] <= 0 or pelota["x"] + pelota["r"] >= ANCHO:
        pelota["dx"] *= -1

    # ---------------------------------------------------------
    #                   IA DE LA CPU
    # ---------------------------------------------------------
    error = 12 if nivel == 1 else 6  # CPU del nivel 2 es más precisa

    # CPU no siempre sigue la pelota (probabilidad de error)
    if random.random() > (1 / error):
        objetivo = pelota["x"] - ancho_paleta//2
        suav = 0.07 if nivel == 1 else 0.12
        paleta_cpu_x += (objetivo - paleta_cpu_x) * suav

    # Limitar dentro de pantalla
    paleta_cpu_x = clamp(paleta_cpu_x, 0, ANCHO - ancho_paleta)

    # ---------------------------------------------------------
    #                 COLISIONES CON PALETAS
    # ---------------------------------------------------------

    # --- Paleta del jugador ---
    if pelota["dy"] > 0:  # pelota moviéndose hacia abajo
        if paleta_jugador_y <= pelota["y"] + pelota["r"] <= paleta_jugador_y + 20:
            if paleta_jugador_x <= pelota["x"] <= paleta_jugador_x + ancho_paleta:
                offset = (pelota["x"] - (paleta_jugador_x + ancho_paleta/2)) / (ancho_paleta/2)
                pelota["dx"] += offset * 2  # desviación horizontal
                pelota["dy"] *= -1
                if hit_sound: hit_sound.play()

    # --- Paleta CPU ---
    if pelota["dy"] < 0:  # pelota hacia arriba
        if paleta_cpu_y <= pelota["y"] - pelota["r"] <= paleta_cpu_y + alto_paleta:
            if paleta_cpu_x <= pelota["x"] <= paleta_cpu_x + ancho_paleta:
                offset = (pelota["x"] - (paleta_cpu_x + ancho_paleta/2)) / (ancho_paleta/2)
                pelota["dx"] += offset * 2
                pelota["dy"] *= -1
                if hit_sound: hit_sound.play()

    # ---------------------------------------------------------
    #                         PUNTAJE
    # ---------------------------------------------------------
    if pelota["y"] < 0:  # salió por arriba → punto jugador
        puntos_jugador += 1
        if score_sound: score_sound.play()
        reiniciar_pelota()

        if puntos_jugador >= 10:
            juego_terminado = True
            ganador = "¡GANASTE!"

    if pelota["y"] > ALTO:  # salió por abajo → punto CPU
        puntos_cpu += 1
        if score_sound: score_sound.play()
        reiniciar_pelota()

        if puntos_cpu >= 10:
            juego_terminado = True
            ganador = "PERDISTE"

    # ---------------------------------------------------------
    #                       DIBUJADO
    # ---------------------------------------------------------
    ventana.blit(fondos[nivel], (0, 0))

    # Paletas y pelota
    pygame.draw.rect(ventana, BLANCO, (int(paleta_jugador_x), paleta_jugador_y, ancho_paleta, alto_paleta), border_radius=8)
    pygame.draw.rect(ventana, BLANCO, (int(paleta_cpu_x), paleta_cpu_y, ancho_paleta, alto_paleta), border_radius=8)
    pygame.draw.circle(ventana, BLANCO, (int(pelota["x"]), int(pelota["y"])), pelota["r"])

    # Marcador
    fuente = pygame.font.SysFont(None, 40)
    marcador = fuente.render(f"{puntos_jugador} - {puntos_cpu}", True, BLANCO)
    ventana.blit(marcador, (ANCHO//2 - marcador.get_width()//2, 20))

    pygame.display.flip()
    reloj.tick(60)
