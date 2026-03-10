import math
import os
import random
import sys

import pygame

from constants import (
    RADIO_PUPILA_BASE,
    RES_VIRTUAL,
    ANCHO_REAL,
    ALTO_REAL,
    ANGULO_LOGO,
    FPS_OBJETIVO,
    DISTANCIA_MOVIMIENTO,
    DEADZONE_JOYSTICK,
    BTN_AMOR,
    BTN_DINERO,
    BTN_LOGO,
    BTN_DROGADO,
    BTN_GLITCH,
    BTN_MAS,
    BTN_MENOS,
    MODO_FULLSCREEN,
    MOSTRAR_CURSOR,
    JOYSTICK_RESCAN_INTERVAL_MS,
    JOYSTICK_RECOVERY_COOLDOWN_MS,
    LOG_INPUT_HEARTBEAT_MS,
)
from utils import  (toggle_fullscreen, log, proximo_parpadeo_natural, refrescar_joysticks, cargar_frames_parpadeo, cargar_imagen, crear_mascara_esclerotica, renderizar, actualizar_diagnostico_input, actualizar_estado)

# =========================
# CACHE
# =========================
class LogoCache:
    def __init__(self, logo_surface):
        self.logo_surface = logo_surface
        self.cache_rotaciones = {}
        self.cache_escalados = {}

    def obtener_escalado(self, size):
        size = max(1, int(size))
        if size not in self.cache_escalados:
            self.cache_escalados[size] = pygame.transform.scale(
                self.logo_surface, (size, size)
            )
        return self.cache_escalados[size]

    def obtener_rotado(self, size, angle):
        size = max(1, int(size))
        angle = int(angle) % 360
        key = (size, angle)

        if key not in self.cache_rotaciones:
            img = self.obtener_escalado(size)
            self.cache_rotaciones[key] = pygame.transform.rotate(img, angle)

        return self.cache_rotaciones[key]


class MascaraCircularCache:
    def __init__(self):
        self.cache = {}

    def obtener(self, width, height, radius):
        width = max(1, int(width))
        height = max(1, int(height))
        radius = max(1, int(radius))
        key = (width, height, radius)

        if key not in self.cache:
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                (255, 255, 255, 255),
                (width // 2, height // 2),
                radius,
            )
            self.cache[key] = surf

        return self.cache[key]


# =========================
# INPUT
# =========================
def leer_entradas(teclas, joysticks, diag):
    entradas = {
        "amor": False,
        "dinero": False,
        "logo": False,
        "glitch": False,
        "drogado": False,
        "mas": False,
        "menos": False,
        "dx": 0,
        "dy": 0,
        "hubo_input": False,
        "fuente_input": "ninguna",
    }

    entradas["amor"] = teclas[pygame.K_a]
    entradas["dinero"] = teclas[pygame.K_m]
    entradas["logo"] = teclas[pygame.K_p]
    entradas["glitch"] = teclas[pygame.K_g]
    entradas["drogado"] = teclas[pygame.K_d]
    entradas["mas"] = diag.tecla_mas_activa or teclas[pygame.K_KP_PLUS]
    entradas["menos"] = (
        diag.tecla_menos_activa
        or teclas[pygame.K_KP_MINUS]
        or teclas[pygame.K_MINUS]
    )

    dx = 0
    dy = 0

    if teclas[pygame.K_UP] or teclas[pygame.K_KP8]:
        dy -= DISTANCIA_MOVIMIENTO
    if teclas[pygame.K_DOWN] or teclas[pygame.K_KP2]:
        dy += DISTANCIA_MOVIMIENTO
    if teclas[pygame.K_LEFT] or teclas[pygame.K_KP4]:
        dx -= DISTANCIA_MOVIMIENTO
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_KP6]:
        dx += DISTANCIA_MOVIMIENTO

    if teclas[pygame.K_KP7]:
        dx -= DISTANCIA_MOVIMIENTO
        dy -= DISTANCIA_MOVIMIENTO
    if teclas[pygame.K_KP9]:
        dx += DISTANCIA_MOVIMIENTO
        dy -= DISTANCIA_MOVIMIENTO
    if teclas[pygame.K_KP1]:
        dx -= DISTANCIA_MOVIMIENTO
        dy += DISTANCIA_MOVIMIENTO
    if teclas[pygame.K_KP3]:
        dx += DISTANCIA_MOVIMIENTO
        dy += DISTANCIA_MOVIMIENTO

    entradas["dx"] = dx
    entradas["dy"] = dy

    if (
        entradas["amor"] or entradas["dinero"] or entradas["logo"] or
        entradas["glitch"] or entradas["drogado"] or entradas["mas"] or
        entradas["menos"] or dx != 0 or dy != 0
    ):
        entradas["hubo_input"] = True
        entradas["fuente_input"] = "teclado"

    for joy in joysticks:
        try:
            if joy.get_button(BTN_AMOR):
                entradas["amor"] = True
                entradas["hubo_input"] = True
                entradas["fuente_input"] = "joystick"

            if joy.get_button(BTN_DINERO):
                entradas["dinero"] = True
                entradas["hubo_input"] = True
                entradas["fuente_input"] = "joystick"

            if joy.get_button(BTN_LOGO):
                entradas["logo"] = True
                entradas["hubo_input"] = True
                entradas["fuente_input"] = "joystick"

            if joy.get_button(BTN_DROGADO):
                entradas["drogado"] = True
                entradas["hubo_input"] = True
                entradas["fuente_input"] = "joystick"

            if joy.get_button(BTN_GLITCH):
                entradas["glitch"] = True
                entradas["hubo_input"] = True
                entradas["fuente_input"] = "joystick"

            if joy.get_button(BTN_MAS):
                entradas["mas"] = True
                entradas["hubo_input"] = True
                entradas["fuente_input"] = "joystick"

            if joy.get_button(BTN_MENOS):
                entradas["menos"] = True
                entradas["hubo_input"] = True
                entradas["fuente_input"] = "joystick"

            if entradas["dx"] == 0 and entradas["dy"] == 0:
                ex = joy.get_axis(0) if joy.get_numaxes() > 0 else 0.0
                ey = joy.get_axis(1) if joy.get_numaxes() > 1 else 0.0

                if abs(ex) > DEADZONE_JOYSTICK:
                    entradas["dx"] = DISTANCIA_MOVIMIENTO if ex > 0 else -DISTANCIA_MOVIMIENTO
                    entradas["hubo_input"] = True
                    entradas["fuente_input"] = "joystick"

                if abs(ey) > DEADZONE_JOYSTICK:
                    entradas["dy"] = DISTANCIA_MOVIMIENTO if ey > 0 else -DISTANCIA_MOVIMIENTO
                    entradas["hubo_input"] = True
                    entradas["fuente_input"] = "joystick"

                if entradas["dx"] == 0 and entradas["dy"] == 0 and joy.get_numhats() > 0:
                    hat = joy.get_hat(0)
                    if hat[0] != 0:
                        entradas["dx"] = hat[0] * DISTANCIA_MOVIMIENTO
                        entradas["hubo_input"] = True
                        entradas["fuente_input"] = "joystick"
                    if hat[1] != 0:
                        entradas["dy"] = -hat[1] * DISTANCIA_MOVIMIENTO
                        entradas["hubo_input"] = True
                        entradas["fuente_input"] = "joystick"

        except pygame.error as e:
            log(f"[WARN] Error leyendo joystick: {e}")

    return entradas


def resolver_modo(entradas):
    if entradas["dinero"]:
        return "dinero"
    if entradas["logo"]:
        return "logo"
    if entradas["amor"]:
        return "amor"
    if entradas["glitch"]:
        return "glitch"
    if entradas["mas"]:
        return "mas"
    if entradas["menos"]:
        return "menos"
    if entradas["drogado"]:
        return "drogado"
    return "normal"


# =========================
# ESTADO
# =========================
class EstadoOjo:
    def __init__(self, centro_x, centro_y):
        self.centro_x = centro_x
        self.centro_y = centro_y

        self.pupila_x = float(centro_x)
        self.pupila_y = float(centro_y)

        self.radio_actual = float(RADIO_PUPILA_BASE)
        self.angulo_actual_logo = float(ANGULO_LOGO)

        self.animando = False
        self.frame_actual_anim = 0.0
        self.velocidad_anim_fps = 12.0

        self.timer_parpadeo = pygame.time.get_ticks()
        self.proximo_parpadeo = proximo_parpadeo_natural()

        self.glitch_offset_x = 0
        self.glitch_offset_y = 0
        self.glitch_radio = RADIO_PUPILA_BASE
        self.proximo_glitch_update = 0


class EstadoDiagnosticoInput:
    def __init__(self):
        ahora = pygame.time.get_ticks()
        self.ultimo_input_ms = ahora
        self.ultimo_input_fuente = "ninguna"
        self.ultimo_rescan_ms = ahora
        self.ultimo_recovery_ms = 0
        self.ultimo_log_heartbeat_ms = 0
        self.input_congelado = False
        self.cantidad_recoveries = 0

        self.tecla_mas_activa = False
        self.tecla_menos_activa = False

        self.mostrar_overlay_debug = False


# =========================
# MAIN
# =========================
def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    pygame.init()
    pygame.joystick.init()
    fullscreen = MODO_FULLSCREEN

    flags = pygame.DOUBLEBUF
    if fullscreen:
        flags |= pygame.FULLSCREEN

    pantalla = pygame.display.set_mode((ANCHO_REAL, ALTO_REAL), flags)
    pygame.mouse.set_visible(MOSTRAR_CURSOR)

    fuente_debug = pygame.font.SysFont(None, 16)

    lienzo = pygame.Surface(RES_VIRTUAL)

    centro_x = RES_VIRTUAL[0] // 2
    centro_y = RES_VIRTUAL[1] // 2

    joysticks = refrescar_joysticks()

    frames_parpadeo = cargar_frames_parpadeo()

    logo_surface = cargar_imagen(
        os.path.join("media", "Posdata-Logo.png"),
        alpha=True,
        fallback_size=(100, 100),
    )

    logo_cache = LogoCache(logo_surface)
    mascara_circular_cache = MascaraCircularCache()

    mascara_esclerotica = crear_mascara_esclerotica(centro_x, centro_y)
    capa_ojo = pygame.Surface(RES_VIRTUAL, pygame.SRCALPHA)
    capa_brillo = pygame.Surface(RES_VIRTUAL, pygame.SRCALPHA)

    estado = EstadoOjo(centro_x, centro_y)
    diag = EstadoDiagnosticoInput()

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(FPS_OBJETIVO) / 1000.0
        tiempo_ahora = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F11:
                    pantalla, fullscreen = toggle_fullscreen(fullscreen)
                elif event.key == pygame.K_F1:
                    diag.mostrar_overlay_debug = not diag.mostrar_overlay_debug
                    log(f"[INFO] Overlay debug: {'ON' if diag.mostrar_overlay_debug else 'OFF'}")
                elif event.key == pygame.K_KP_PLUS:
                    diag.tecla_mas_activa = True
                elif event.key == pygame.K_KP_MINUS:
                    diag.tecla_menos_activa = True
                elif event.key == pygame.K_MINUS:
                    diag.tecla_menos_activa = True
                elif event.key == pygame.K_EQUALS and (event.mod & pygame.KMOD_SHIFT):
                    diag.tecla_mas_activa = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_KP_PLUS:
                    diag.tecla_mas_activa = False
                elif event.key == pygame.K_KP_MINUS:
                    diag.tecla_menos_activa = False
                elif event.key == pygame.K_MINUS:
                    diag.tecla_menos_activa = False
                elif event.key == pygame.K_EQUALS:
                    diag.tecla_mas_activa = False

            elif event.type == pygame.JOYDEVICEADDED:
                log("[EVENT] JOYDEVICEADDED")
                joysticks = refrescar_joysticks()

            elif event.type == pygame.JOYDEVICEREMOVED:
                log("[EVENT] JOYDEVICEREMOVED")
                joysticks = refrescar_joysticks()

        if tiempo_ahora - diag.ultimo_rescan_ms >= JOYSTICK_RESCAN_INTERVAL_MS:
            joysticks = refrescar_joysticks()
            diag.ultimo_rescan_ms = tiempo_ahora

        teclas = pygame.key.get_pressed()
        entradas = leer_entradas(teclas, joysticks, diag)

        actualizar_diagnostico_input(diag, entradas, tiempo_ahora)

        if tiempo_ahora - diag.ultimo_log_heartbeat_ms >= LOG_INPUT_HEARTBEAT_MS:
            sin_input_ms = tiempo_ahora - diag.ultimo_input_ms
            log(
                f"[HEARTBEAT] joysticks={len(joysticks)} "
                f"ultimo_input={diag.ultimo_input_fuente} "
                f"sin_input={sin_input_ms}ms "
                f"watchdog={'ON' if diag.input_congelado else 'OK'}"
            )
            diag.ultimo_log_heartbeat_ms = tiempo_ahora

        if diag.input_congelado:
            if tiempo_ahora - diag.ultimo_recovery_ms >= JOYSTICK_RECOVERY_COOLDOWN_MS:
                log("[RECOVERY] Sin input por demasiado tiempo. Intentando recuperar joysticks.")
                joysticks = refrescar_joysticks(forzar_reinit=True)
                diag.ultimo_recovery_ms = tiempo_ahora
                diag.cantidad_recoveries += 1

        modo = resolver_modo(entradas)

        actualizar_estado(estado, entradas, modo, tiempo_ahora, dt)

        renderizar(
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
        )

        frame_escalado = pygame.transform.scale(lienzo, (ANCHO_REAL, ALTO_REAL))
        pantalla.blit(frame_escalado, (0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()