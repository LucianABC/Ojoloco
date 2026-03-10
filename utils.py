
import math
import pygame
import time
import os
import sys
import random
from constants import (ANCHO_REAL, INPUT_WATCHDOG_MS, ALTO_REAL, CANTIDAD_FRAMES, RES_VIRTUAL, BLANCO, NEGRO, IRIS_NORMAL, ROSA_AMOR, VERDE_DINERO, RADIO_PUPILA_BASE, RADIO_PUPILA_AMOR, RADIO_PUPILA_DINERO, RADIO_PUPILA_LOGO, RADIO_PUPILA_DROGADO, RADIO_PUPILA_MAS, RADIO_PUPILA_MENOS, GLITCH_INTERVAL_MS)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media")

def dibujar_pupila_corazon(superficie, color, pos, tam):
    puntos = []
    for t in [x * 0.1 for x in range(0, 63)]:
        x = 16 * math.sin(t)**3
        y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        puntos.append((pos[0] + x * (tam/15), pos[1] + y * (tam/15)))
    if len(puntos) > 2:
        pygame.draw.polygon(superficie, color, puntos)

def dibujar_pupila_peso(superficie, color, pos, tam):
    ancho = int(tam * 1.3)
    alto = int(tam * 1.8)
    x, y = int(pos[0]), int(pos[1])
        
    # --- Puntos para la forma 'S' gruesa ---
    # Top bar, curva superior, barra media, curva inferior, bottom bar
    anch_s = ancho // 2
    alt_s = alto // 2
    
    grosor_linea = int(tam / 3)
    puntos_s_linea = [
        (x + anch_s, y - alt_s + grosor_linea//2), # Inicio top derecho
        (x - anch_s, y - alt_s + grosor_linea//2), # Top izquierdo
        (x - anch_s, y),                         # Medio izquierdo
        (x + anch_s, y),                         # Medio derecho
        (x + anch_s, y + alt_s - grosor_linea//2), # Bottom derecho
        (x - anch_s, y + alt_s - grosor_linea//2)  # Final bottom izquierdo
    ]
    if len(puntos_s_linea) > 1:
        pygame.draw.lines(superficie, color, False, puntos_s_linea, grosor_linea)
    
    # Línea vertical central, también MUY gruesa
    grosor_vertical = int(tam / 4)
    pygame.draw.line(superficie, color, (x, y - alt_s - grosor_vertical//2), (x, y + alt_s + grosor_vertical//2), grosor_vertical)

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


def toggle_fullscreen(estado_actual):
    nuevo_estado = not estado_actual

    flags = pygame.DOUBLEBUF
    if nuevo_estado:
        flags |= pygame.FULLSCREEN

    pantalla = pygame.display.set_mode((ANCHO_REAL, ALTO_REAL), flags)

    log(f"[INFO] Fullscreen: {'ON' if nuevo_estado else 'OFF'}")

    return pantalla, nuevo_estado


def cargar_imagen(ruta, size=None, alpha=True, fallback_size=(64, 64)):
    try:
        img = pygame.image.load(ruta)
        img = img.convert_alpha() if alpha else img.convert()
        if size is not None:
            img = pygame.transform.scale(img, size)
        return img
    except (pygame.error, FileNotFoundError) as e:
        log(f"[WARN] No se pudo cargar '{ruta}': {e}")
        return pygame.Surface(fallback_size, pygame.SRCALPHA)


def cargar_frames_parpadeo():
    frames = []
    for i in range(CANTIDAD_FRAMES):
        ruta = os.path.join(MEDIA_DIR, f"Eye-{i}.png")
        try:
            img = pygame.image.load(ruta).convert_alpha()
            img = pygame.transform.scale(img, RES_VIRTUAL)
            frames.append(img)
        except (pygame.error, FileNotFoundError) as e:
            log(f"[WARN] Error cargando frame de parpadeo '{ruta}': {e}")
    return frames


def obtener_joysticks():
    joysticks = []
    count = pygame.joystick.get_count()

    for i in range(count):
        try:
            joy = pygame.joystick.Joystick(i)
            joy.init()
            joysticks.append(joy)
        except pygame.error as e:
            log(f"[WARN] No se pudo inicializar joystick {i}: {e}")

    return joysticks


def describir_joysticks(joysticks):
    partes = []
    for i, joy in enumerate(joysticks):
        try:
            nombre = joy.get_name()
        except pygame.error:
            nombre = "desconocido"
        partes.append(f"{i}:{nombre}")
    return ", ".join(partes) if partes else "ninguno"


def refrescar_joysticks(forzar_reinit=False):
    if forzar_reinit:
        try:
            pygame.joystick.quit()
            pygame.joystick.init()
            log("[INFO] Subsistema joystick reinicializado")
        except pygame.error as e:
            log(f"[WARN] No se pudo reinicializar subsistema joystick: {e}")

    joysticks = obtener_joysticks()
    log(f"[INFO] Joysticks activos: {len(joysticks)} -> {describir_joysticks(joysticks)}")
    return joysticks


def clamp(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def suavizado_factor(velocidad, dt):
    return 1.0 - math.exp(-velocidad * dt)


def limitar_a_elipse(x, y, cx, cy, rx, ry):
    dx = x - cx
    dy = y - cy

    if rx <= 0 or ry <= 0:
        return cx, cy

    normalizado = (dx * dx) / (rx * rx) + (dy * dy) / (ry * ry)
    if normalizado <= 1.0:
        return x, y

    angulo = math.atan2(dy, dx)
    return (
        cx + math.cos(angulo) * rx,
        cy + math.sin(angulo) * ry,
    )


def proximo_parpadeo_natural():
    valor = int(random.gauss(4000, 1200))
    return clamp(valor, 1500, 8000)


def crear_mascara_esclerotica(centro_x, centro_y):
    mascara = pygame.Surface(RES_VIRTUAL, pygame.SRCALPHA)
    pygame.draw.ellipse(
        mascara,
        (255, 255, 255, 255),
        (centro_x - 70, centro_y - 45, 140, 90),
    )
    return mascara


def obtener_frame_idle(modo, frames_parpadeo):
    if not frames_parpadeo:
        return None

    if modo == "amor":
        f_idle = 1
    elif modo == "drogado":
        f_idle = 2
    else:
        f_idle = 0

    return clamp(f_idle, 0, len(frames_parpadeo) - 1)

# =========================
# UPDATE
# =========================
def actualizar_estado(estado, entradas, modo, tiempo_ahora, dt):
    if modo == "glitch":
        if tiempo_ahora >= estado.proximo_glitch_update:
            estado.glitch_offset_x = random.randint(-8, 8)
            estado.glitch_offset_y = random.randint(-8, 8)
            estado.glitch_radio = random.choice([5, 10, 35])
            estado.proximo_glitch_update = tiempo_ahora + GLITCH_INTERVAL_MS
    else:
        estado.glitch_offset_x = 0
        estado.glitch_offset_y = 0
        estado.glitch_radio = RADIO_PUPILA_BASE

    target_x = estado.centro_x + entradas["dx"] + estado.glitch_offset_x
    target_y = estado.centro_y + entradas["dy"] + estado.glitch_offset_y

    factor_pos = suavizado_factor(10.0, dt)
    estado.pupila_x += (target_x - estado.pupila_x) * factor_pos
    estado.pupila_y += (target_y - estado.pupila_y) * factor_pos

    if modo == "dinero":
        latido = math.sin(tiempo_ahora * 0.01) * 3
        radio_target = RADIO_PUPILA_DINERO + latido
    elif modo == "logo":
        radio_target = RADIO_PUPILA_LOGO
    elif modo == "amor":
        latido = (math.sin(tiempo_ahora * 0.01) + math.sin(tiempo_ahora * 0.02) * 0.5) * 3
        radio_target = RADIO_PUPILA_AMOR + latido
    elif modo == "glitch":
        radio_target = estado.glitch_radio
    elif modo == "mas":
        radio_target = 30
    elif modo == "menos":
        radio_target = 8
    elif modo == "drogado":
        radio_target = RADIO_PUPILA_DROGADO
    else:
        radio_target = RADIO_PUPILA_BASE

    factor_radio = suavizado_factor(8.0, dt)
    estado.radio_actual += (radio_target - estado.radio_actual) * factor_radio

    if modo == "logo":
        estado.angulo_actual_logo = (estado.angulo_actual_logo + 120.0 * dt) % 360.0

    if not estado.animando and (tiempo_ahora - estado.timer_parpadeo > estado.proximo_parpadeo):
        estado.animando = True
        estado.frame_actual_anim = 0.0
        estado.timer_parpadeo = tiempo_ahora
        estado.proximo_parpadeo = proximo_parpadeo_natural()

    if estado.animando:
        estado.frame_actual_anim += estado.velocidad_anim_fps * dt


def actualizar_diagnostico_input(diag, entradas, tiempo_ahora):
    if entradas["hubo_input"]:
        diag.ultimo_input_ms = tiempo_ahora
        diag.ultimo_input_fuente = entradas["fuente_input"]
        diag.input_congelado = False

    if tiempo_ahora - diag.ultimo_input_ms > INPUT_WATCHDOG_MS:
        diag.input_congelado = True


# =========================
# RENDER
# =========================
def renderizar_overlay_debug(lienzo, fuente, diag, joysticks, modo, tiempo_ahora):
    if not diag.mostrar_overlay_debug:
        return

    tiempo_sin_input = (tiempo_ahora - diag.ultimo_input_ms) / 1000.0
    lineas = [
        f"modo: {modo}",
        f"joysticks: {len(joysticks)}",
        f"ultimo input: {diag.ultimo_input_fuente}",
        f"sin input: {tiempo_sin_input:.1f}s",
        f"watchdog: {'ON' if diag.input_congelado else 'OK'}",
        f"recoveries: {diag.cantidad_recoveries}",
    ]

    y = 6
    for linea in lineas:
        txt = fuente.render(linea, True, NEGRO)
        fondo = pygame.Surface((txt.get_width() + 6, txt.get_height() + 2), pygame.SRCALPHA)
        fondo.fill((255, 255, 255, 170))
        lienzo.blit(fondo, (4, y - 1))
        lienzo.blit(txt, (7, y))
        y += txt.get_height() + 4


def renderizar(
    lienzo,
    capa_ojo,
    capa_brillo,
    mascara_esclerotica,
    estado,
    modo,
    frames_parpadeo,
    logo_cache,
    mascara_circular_cache,
    fuente_debug,
    diag,
    joysticks,
    tiempo_ahora,
):
    lienzo.fill(BLANCO)
    capa_ojo.fill((0, 0, 0, 0))
    capa_brillo.fill((0, 0, 0, 0))

    pupila_pos = (int(estado.pupila_x), int(estado.pupila_y))
    radio_actual_int = max(1, int(estado.radio_actual))

    if modo == "dinero":
        color_iris = VERDE_DINERO
    elif modo == "amor":
        color_iris = ROSA_AMOR
    elif modo == "glitch":
        color_iris = random.choice([IRIS_NORMAL, (150, 150, 150)])
    else:
        color_iris = IRIS_NORMAL

    pygame.draw.circle(capa_ojo, color_iris, pupila_pos, 32)

    if modo == "logo":
        pygame.draw.circle(capa_ojo, NEGRO, pupila_pos, radio_actual_int)

        tam_logo = int(estado.radio_actual * 1.8)
        if tam_logo > 5:
            img_rot = logo_cache.obtener_rotado(tam_logo, estado.angulo_actual_logo)
            rect_rot = img_rot.get_rect(center=pupila_pos)
            img_final = img_rot.copy()

            mask_circ = mascara_circular_cache.obtener(
                img_rot.get_width(),
                img_rot.get_height(),
                radio_actual_int,
            )
            img_final.blit(mask_circ, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            capa_ojo.blit(img_final, rect_rot)

    elif modo == "dinero":
        dibujar_pupila_peso(capa_ojo, NEGRO, pupila_pos, radio_actual_int)

    elif modo == "amor":
        dibujar_pupila_corazon(capa_ojo, NEGRO, pupila_pos, estado.radio_actual)

    else:
        pygame.draw.circle(capa_ojo, NEGRO, pupila_pos, radio_actual_int)

    capa_ojo.blit(mascara_esclerotica, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    lienzo.blit(capa_ojo, (0, 0))

    if modo not in ("logo", "glitch"):
        b_color = (255, 255, 255, 200) if modo in ("amor", "dinero") else (255, 255, 255, 140)
        b_offset = estado.radio_actual * (0.4 if modo == "dinero" else 0.3)
        b_x = int(estado.pupila_x - b_offset)
        b_y = int(estado.pupila_y - b_offset)
        b_r = max(1, int(estado.radio_actual * 0.35))
        pygame.draw.circle(capa_brillo, b_color, (b_x, b_y), b_r)

    capa_brillo.blit(mascara_esclerotica, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    lienzo.blit(capa_brillo, (0, 0))

    if frames_parpadeo:
        if estado.animando:
            idx = int(estado.frame_actual_anim)

            if idx >= len(frames_parpadeo):
                estado.animando = False
                estado.frame_actual_anim = 0.0

                f_idle = obtener_frame_idle(modo, frames_parpadeo)
                if f_idle is not None:
                    lienzo.blit(frames_parpadeo[f_idle], (0, 0))
            else:
                lienzo.blit(frames_parpadeo[idx], (0, 0))
        else:
            f_idle = obtener_frame_idle(modo, frames_parpadeo)
            if f_idle is not None:
                lienzo.blit(frames_parpadeo[f_idle], (0, 0))

    renderizar_overlay_debug(lienzo, fuente_debug, diag, joysticks, modo, tiempo_ahora)
def toggle_fullscreen(estado_actual):
    nuevo_estado = not estado_actual

    flags = pygame.DOUBLEBUF
    if nuevo_estado:
        flags |= pygame.FULLSCREEN

    pantalla = pygame.display.set_mode((ANCHO_REAL, ALTO_REAL), flags)

    log(f"[INFO] Fullscreen: {'ON' if nuevo_estado else 'OFF'}")

    return pantalla, nuevo_estado

def reiniciar_app():
    log("[INFO] Reiniciando aplicación...")
    pygame.quit()
    sys.exit(0)