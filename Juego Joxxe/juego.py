import pygame
import random
import sys

pygame.init()
# init mixer with safe fallback
try:
    pygame.mixer.init()
except Exception:
    print("Advertencia: pygame.mixer no pudo inicializarse. El sonido estará deshabilitado.")

# ------------------ MÚSICA Y SONIDOS ------------------
def safe_load_music(path):
    try:
        pygame.mixer.music.load(path)
        return True
    except Exception as e:
        print(f"No se pudo cargar música '{path}': {e}")
        return False

def safe_load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        print(f"No se pudo cargar sonido '{path}'.")
        return None

# Cargar efectos (opcional)
hit_sound = safe_load_sound("hit.wav")
score_sound = safe_load_sound("score.wav")

def stop_music():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass

def musica_menu():
    stop_music()
    if safe_load_music("menu_music.wav"):
        try:
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

def musica_nivel1():
    stop_music()
    if safe_load_music("nivel1_music.wav"):
        try:
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

def musica_nivel2():
    stop_music()
    if safe_load_music("nivel2_music.wav"):
        try:
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

# ------------------ VENTANA ------------------
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))  # Crear ventana
pygame.display.set_caption("Ping Pong Vertical")

reloj = pygame.time.Clock()  # Controlar FPS

# ------------------ FONDOS (cargar con try/except para no romper si faltan) ------------------
def safe_load_image(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except Exception:
        # crear superficie neutral si no existe la imagen
        s = pygame.Surface(size)
        s.fill((20, 20, 40))
        return s

menu_bg = safe_load_image("menu_bg.png", (ANCHO, ALTO))
nivel1_bg = safe_load_image("nivel1_bg.png", (ANCHO, ALTO))
nivel2_bg = safe_load_image("nivel2_bg.png", (ANCHO, ALTO))

# ------------------ COLORES ------------------
BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
GRIS_OSCURO = (80, 80, 80)
FONDO_FINAL = (15, 10, 25)

# ------------------ PALETAS (JUGADOR Y CPU) ------------------
ancho_paleta = 140
alto_paleta = 15
velocidad_jugador = 8
velocidad_cpu_base = 6  # base, puede cambiar por nivel

# Posiciones iniciales de paletas
paleta_jugador_x = ANCHO // 2 - ancho_paleta // 2
paleta_jugador_y = ALTO - 60
paleta_cpu_x = ANCHO // 2 - ancho_paleta // 2
paleta_cpu_y = 80

# ------------------ PELOTA ------------------
pelota_x = ANCHO // 2
pelota_y = ALTO // 2
pelota_radio = 12
pelota_dx = 6   # Velocidad horizontal
pelota_dy = 6   # Velocidad vertical

# ------------------ PUNTOS Y NIVELES ------------------
puntos_jugador = 0
puntos_cpu = 0
nivel = 1

# Variables que controlan en qué pantalla estamos
menu = True
juego_terminado = False
ganador = ""
pausa = False

# ------------------ UTILS ------------------
def clamp(value, minv, maxv):
    return max(minv, min(value, maxv))

# Reinicia la posición de la pelota después de un punto
def reiniciar_pelota(keep_direction=False):
    global pelota_x, pelota_y, pelota_dx, pelota_dy
    pelota_x = ANCHO // 2
    pelota_y = ALTO // 2
    if not keep_direction:
        # invertir vertical para cambiar quien sirve
        pelota_dy = -abs(pelota_dy) if random.choice([True, False]) else abs(pelota_dy)
    else:
        pelota_dy *= -1

# Reset completo (paletas y pelota)
def reset_juego():
    global paleta_jugador_x, paleta_cpu_x, pelota_x, pelota_y, pelota_dx, pelota_dy
    paleta_jugador_x = ANCHO//2 - ancho_paleta//2
    paleta_cpu_x = ANCHO//2 - ancho_paleta//2
    pelota_x = ANCHO//2
    pelota_y = ALTO//2
    # restablecer velocidades a valores por nivel
    if nivel == 1:
        pelota_dx = 5
        pelota_dy = 5
    else:
        pelota_dx = 7
        pelota_dy = 7

# Ajusta velocidades para Nivel 1
def activar_nivel_1():
    global nivel, pelota_dx, pelota_dy, velocidad_cpu
    nivel = 1
    pelota_dx = 5
    pelota_dy = 5
    velocidad_cpu = velocidad_cpu_base
    reset_juego()

# Ajusta velocidades para Nivel 2
def activar_nivel_2():
    global nivel, pelota_dx, pelota_dy, velocidad_cpu
    nivel = 2
    pelota_dx = 7
    pelota_dy = 7
    velocidad_cpu = velocidad_cpu_base + 3
    reset_juego()

# Música inicial (menú)
musica_menu()

# ------------------ LOOP PRINCIPAL ------------------
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Clic en los botones del menú
        if menu and evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Botón Nivel 1
            if 250 <= mx <= 550 and 230 <= my <= 300:
                activar_nivel_1()
                musica_nivel1()
                menu = False

            # Botón Nivel 2
            if 250 <= mx <= 550 and 330 <= my <= 400:
                activar_nivel_2()
                musica_nivel2()
                menu = False

        # Clic para volver al menú tras terminar la partida
        if juego_terminado and evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            boton_x = ANCHO//2 - 150
            boton_y = 360
            boton_ancho = 300
            boton_alto = 70
            if boton_x <= mx <= boton_x + boton_ancho and boton_y <= my <= boton_y + boton_alto:
                puntos_jugador = 0
                puntos_cpu = 0
                juego_terminado = False
                menu = True
                musica_menu()

        # Toggle pausa con P (también escuchar KEYDOWN fuera del while pausa)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_p and not menu and not juego_terminado:
                pausa = not pausa

    # ------------------ PANTALLA DE MENÚ ------------------
    if menu:
        ventana.blit(menu_bg, (0, 0))  # Fondo del menú

        fuente = pygame.font.SysFont(None, 60)
        ventana.blit(fuente.render("Ping - Pong", True, BLANCO), (ANCHO//2 - 200, 120))

        mx, my = pygame.mouse.get_pos()

        # Botón Nivel 1 (cambia color si el mouse está encima)
        color1 = GRIS if 250 <= mx <= 550 and 230 <= my <= 300 else GRIS_OSCURO
        pygame.draw.rect(ventana, color1, (250, 230, 300, 70), border_radius=18)
        fuente2 = pygame.font.SysFont(None, 40)
        ventana.blit(fuente2.render("Nivel 1", True, BLANCO), (ANCHO//2 - 55, 252))

        # Botón Nivel 2
        color2 = GRIS if 250 <= mx <= 550 and 330 <= my <= 400 else GRIS_OSCURO
        pygame.draw.rect(ventana, color2, (250, 330, 300, 70), border_radius=18)
        ventana.blit(fuente2.render("Nivel 2", True, BLANCO), (ANCHO//2 - 55, 352))

        pygame.display.flip()
        reloj.tick(60)
        continue

    # ------------------ PANTALLA FINAL (GANASTE/PERDISTE) ------------------
    if juego_terminado:
        ventana.fill(FONDO_FINAL)  # Fondo más elegante

        # Texto principal (GANASTE / PERDISTE)
        fuente = pygame.font.SysFont(None, 100)
        texto_ganador = fuente.render(ganador, True, BLANCO)
        ventana.blit(texto_ganador, (ANCHO//2 - texto_ganador.get_width()//2, 200))

        # Configurar botón
        boton_x = ANCHO//2 - 150
        boton_y = 360
        boton_ancho = 300
        boton_alto = 70  # corregido: antes era 7

        mx, my = pygame.mouse.get_pos()

        # Hover (cambiar color si pasa el mouse encima)
        if boton_x <= mx <= boton_x + boton_ancho and boton_y <= my <= boton_y + boton_alto:
            color_boton = (230, 230, 255)  # claro
            color_texto = (40, 40, 70)
        else:
            color_boton = (70, 70, 120)  # base
            color_texto = (255, 255, 255)

        # Dibujar botón
        pygame.draw.rect(ventana, color_boton, (boton_x, boton_y, boton_ancho, boton_alto), border_radius=18)

        # Texto del botón
        fuente2 = pygame.font.SysFont(None, 45)
        texto_volver = fuente2.render("VOLVER AL MENÚ", True, color_texto)
        ventana.blit(texto_volver, (ANCHO//2 - texto_volver.get_width()//2, boton_y + 18))

        pygame.display.flip()
        reloj.tick(60)
        continue

    # Si estamos en pausa, mostrar overlay y saltar lógica de juego
    if pausa:
        # dibujar escena estática (fondo + paletas + pelota)
        ventana.blit(nivel2_bg if nivel == 2 else nivel1_bg, (0, 0))
        pygame.draw.rect(ventana, BLANCO, (int(paleta_jugador_x), paleta_jugador_y, ancho_paleta, alto_paleta), border_radius=8)
        pygame.draw.rect(ventana, BLANCO, (int(paleta_cpu_x), paleta_cpu_y, ancho_paleta, alto_paleta), border_radius=8)
        pygame.draw.circle(ventana, (255,240,240), (int(pelota_x), int(pelota_y)), pelota_radio)
        # overlay de pausa
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((10, 10, 10, 180))
        ventana.blit(s, (0, 0))
        fuente_p = pygame.font.SysFont(None, 80)
        ventana.blit(fuente_p.render("PAUSA", True, BLANCO), (ANCHO//2 - 120, ALTO//2 - 40))
        fuente_m = pygame.font.SysFont(None, 28)
        ventana.blit(fuente_m.render("Presiona P para continuar", True, BLANCO), (ANCHO//2 - 140, ALTO//2 + 40))
        pygame.display.flip()
        reloj.tick(60)
        continue

    # ------------------ CONTROLES JUGADOR ------------------
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and paleta_jugador_x > 0:
        paleta_jugador_x -= velocidad_jugador
    if teclas[pygame.K_RIGHT] and paleta_jugador_x < ANCHO - ancho_paleta:
        paleta_jugador_x += velocidad_jugador

    # ------------------ MOVIMIENTO DE PELOTA ------------------
    pelota_x += pelota_dx
    pelota_y += pelota_dy

    # Rebote contra paredes laterales
    if pelota_x - pelota_radio <= 0:
        pelota_x = pelota_radio
        pelota_dx *= -1
    elif pelota_x + pelota_radio >= ANCHO:
        pelota_x = ANCHO - pelota_radio
        pelota_dx *= -1

    # ------------------ IA DE LA CPU (SUAVIZADA Y CON LÍMITES) ------------------
    # Probabilidad de error (mientras más alto, más se equivoca)
    # Ajustable por dificultad; mantener variable para fines de testing
    error_probabilidad = 12 if nivel == 1 else 6  # nivel 2 menos error (más hábil)

    # Solo a veces la CPU sigue la pelota correctamente
    if random.randint(0, error_probabilidad) != 0:
        # objetivo centrado en la paleta (centro)
        objetivo_x = pelota_x - ancho_paleta // 2
        # suavizar movimiento (factor entre 0.03 y 0.12)
        suavizado = 0.07 if nivel == 1 else 0.12
        paleta_cpu_x += (objetivo_x - paleta_cpu_x) * suavizado

    # asegurarse que la paleta CPU no escape de la pantalla
    paleta_cpu_x = clamp(paleta_cpu_x, 0, ANCHO - ancho_paleta)

    # ------------------ REBOTE CON PALETAS (MEJORADA) ------------------
    # Rebote con paleta del jugador (abajo)
    if pelota_dy > 0:  # solo si la pelota va hacia abajo
        if (pelota_y + pelota_radio >= paleta_jugador_y and
            paleta_jugador_x <= pelota_x <= paleta_jugador_x + ancho_paleta):
            # ajustar dx según el punto de impacto (offset -1..1)
            offset = (pelota_x - (paleta_jugador_x + ancho_paleta/2)) / (ancho_paleta/2)
            pelota_dx += offset * 2  # cambia horizontal
            pelota_dy *= -1
            pelota_y = paleta_jugador_y - pelota_radio - 1  # desplazar para evitar rebotes dobles
            if hit_sound:
                hit_sound.play()

    # Rebote con paleta de la CPU (arriba)
    if pelota_dy < 0:  # solo si la pelota va hacia arriba
        if (pelota_y - pelota_radio <= paleta_cpu_y + alto_paleta and
            paleta_cpu_x <= pelota_x <= paleta_cpu_x + ancho_paleta):
            offset = (pelota_x - (paleta_cpu_x + ancho_paleta/2)) / (ancho_paleta/2)
            pelota_dx += offset * 2
            pelota_dy *= -1
            pelota_y = paleta_cpu_y + alto_paleta + pelota_radio + 1
            if hit_sound:
                hit_sound.play()

    # limita la velocidad horizontal para que no crezca sin control
    max_dx = 12
    pelota_dx = clamp(pelota_dx, -max_dx, max_dx)
    # asegurarse velocidad vertical mínima para no quedarse pegado horizontalmente
    min_dy = 3
    pelota_dy = clamp(pelota_dy, -15, 15)
    if 0 < abs(pelota_dy) < min_dy:
        pelota_dy = min_dy if pelota_dy > 0 else -min_dy

    # ------------------ PUNTAJE ------------------
    if pelota_y - pelota_radio < 0:
        # la pelota salió por arriba -> punto jugador (player at bottom)
        puntos_jugador += 1
        if score_sound:
            score_sound.play()
        reiniciar_pelota(keep_direction=False)
        # restablecer un poco la velocidad para evitar acumulaciones
        if nivel == 1:
            pelota_dx = 5
            pelota_dy = 5
        else:
            pelota_dx = 7
            pelota_dy = 7

        if puntos_jugador >= 10:
            juego_terminado = True
            ganador = "¡GANASTE!"

    elif pelota_y + pelota_radio > ALTO:
        # la pelota salió por abajo -> punto CPU
        puntos_cpu += 1
        if score_sound:
            score_sound.play()
        reiniciar_pelota(keep_direction=False)
        if nivel == 1:
            pelota_dx = 5
            pelota_dy = 5
        else:
            pelota_dx = 7
            pelota_dy = 7

        if puntos_cpu >= 10:
            juego_terminado = True
            ganador = "PERDISTE"

    # ------------------ DIBUJAR ESCENA ------------------
    # Fondo cambia con el nivel
    ventana.blit(nivel2_bg if nivel == 2 else nivel1_bg, (0, 0))

    # Dibujar paletas y pelota (convertir x a int al dibujar)
    pygame.draw.rect(ventana, BLANCO, (int(paleta_jugador_x), paleta_jugador_y, ancho_paleta, alto_paleta), border_radius=8)
    pygame.draw.rect(ventana, BLANCO, (int(paleta_cpu_x), paleta_cpu_y, ancho_paleta, alto_paleta), border_radius=8)
    pygame.draw.circle(ventana, (255,240,240), (int(pelota_x), int(pelota_y)), pelota_radio)

    # Mostrar marcador
    fuente = pygame.font.SysFont(None, 40)
    marcador = fuente.render(f"{puntos_jugador} - {puntos_cpu}", True, BLANCO)
    ventana.blit(marcador, (ANCHO//2 - marcador.get_width()//2, 20))

    # Indicador breve de controles
    fuente_peq = pygame.font.SysFont(None, 20)
    ventana.blit(fuente_peq.render("Izquierda/Derecha para mover. P para pausar.", True, BLANCO), (10, ALTO - 26))

    pygame.display.flip()
    reloj.tick(60)
