import pygame
import sys
import random
import os
import math
from constants import BLANCO, NEGRO, IRIS_NORMAL, ROSA_AMOR, VERDE_DINERO, RADIO_PUPILA, ANGULO_LOGO, CANTIDAD_FRAMES
from utils import dibujar_pupila_corazon, dibujar_pupila_peso

pygame.init()

# --- CONFIGURACIÓN PIXEL ART ---
RES_VIRTUAL = (160, 120) 
ANCHO_REAL, ALTO_REAL = 640, 480
pantalla = pygame.display.set_mode((ANCHO_REAL, ALTO_REAL))
lienzo = pygame.Surface(RES_VIRTUAL)

centro_x, centro_y = RES_VIRTUAL[0] // 2, RES_VIRTUAL[1] // 2
pupila_x, pupila_y = centro_x, centro_y

# Assets Overlay Párpado
frames_parpadeo = []

for i in range(CANTIDAD_FRAMES):
    ruta = os.path.join("media", f"Eye-{i}.png")
    try:
        img = pygame.image.load(ruta).convert_alpha()
        frames_parpadeo.append(pygame.transform.scale(img, RES_VIRTUAL))
    except: pass

try:
    logo_posdata = pygame.image.load(os.path.join("media", "Posdata-Logo.png")).convert_alpha()
except:
    logo_posdata = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(logo_posdata, (200, 0, 0), (50, 50), 45)

# Animación y Capas
frame_actual = 0.0
velocidad_anim = 0.35
animando = False
timer_parpadeo = pygame.time.get_ticks()
proximo_parpadeo = random.randint(2000, 5000)

mascara_esclerotica = pygame.Surface(RES_VIRTUAL, pygame.SRCALPHA)
pygame.draw.ellipse(mascara_esclerotica, (255, 255, 255, 255), (centro_x - 70, centro_y - 45, 140, 90))
capa_ojo = pygame.Surface(RES_VIRTUAL, pygame.SRCALPHA)
capa_brillo = pygame.Surface(RES_VIRTUAL, pygame.SRCALPHA)

running = True
clock = pygame.time.Clock()

while running:
    tiempo_ahora = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    teclas = pygame.key.get_pressed()
    drogado = teclas[pygame.K_d]
    amor = teclas[pygame.K_h]
    especial = teclas[pygame.K_p]
    glitch = teclas[pygame.K_g]  
    dinero = teclas[pygame.K_m] # MODO DINERO

    # --- MOVIMIENTO ---
    dist = 30
    dx, dy = 0, 0
    if teclas[pygame.K_UP] or teclas[pygame.K_KP8]:    dy -= dist
    if teclas[pygame.K_DOWN] or teclas[pygame.K_KP2]:  dy += dist
    if teclas[pygame.K_LEFT] or teclas[pygame.K_KP4]:  dx -= dist
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_KP6]: dx += dist
    
    if teclas[pygame.K_KP7]: dx -= dist; dy -= dist
    if teclas[pygame.K_KP9]: dx += dist; dy -= dist
    if teclas[pygame.K_KP1]: dx -= dist; dy += dist
    if teclas[pygame.K_KP3]: dx += dist; dy += dist

    off_glitch_x = random.randint(-8, 8) if glitch else 0
    off_glitch_y = random.randint(-8, 8) if glitch else 0
    target_x, target_y = centro_x + dx + off_glitch_x, centro_y + dy + off_glitch_y

    pupila_x += (target_x - pupila_x) * 0.15
    pupila_y += (target_y - pupila_y) * 0.15

    # --- TAMAÑO Y LATIDO ---
   

    # Parpadeos
    if not animando and tiempo_ahora - timer_parpadeo > proximo_parpadeo:
        animando = True
        frame_actual = 0.0 if (especial or dinero or glitch or not (amor or drogado)) else (1.0 if amor else 2.0)
        timer_parpadeo = tiempo_ahora
        proximo_parpadeo = random.randint(2000, 6000)

    # --- DIBUJO ---
    lienzo.fill(NEGRO)
    pygame.draw.ellipse(lienzo, BLANCO, (centro_x - 70, centro_y - 45, 140, 90))

    capa_ojo.fill((0, 0, 0, 0))
    
    # Iris
    color_iris = VERDE_DINERO if dinero else (random.choice([IRIS_NORMAL, (150, 150, 150)]) if glitch else (ROSA_AMOR if amor else IRIS_NORMAL))

    pygame.draw.circle(capa_ojo, color_iris, (int(pupila_x), int(pupila_y)), 32)
    
    # Pupila
    if dinero: 
        latido = math.sin(tiempo_ahora * 0.01) * 3
        radio_target = 25 + latido
    elif especial: radio_target = 40
    elif amor: 
        latido = (math.sin(tiempo_ahora * 0.01) + math.sin(tiempo_ahora * 0.02) * 0.5) * 3
        radio_target = 24 + latido
    elif glitch: radio_target = random.choice([10, 35, 5])
    elif drogado or teclas[pygame.K_KP_MINUS]: radio_target = 8
    elif teclas[pygame.K_KP_PLUS]: radio_target = 30
    else: radio_target = 16
    
    RADIO_PUPILA += (radio_target - RADIO_PUPILA) * 0.1

    if especial:
        # Pupila con logo Posdata 
        pygame.draw.circle(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), int(RADIO_PUPILA))
        tam_logo = int(RADIO_PUPILA * 1.8)
        if tam_logo > 5:
            img_res = pygame.transform.scale(logo_posdata, (tam_logo, tam_logo))
            ANGULO_LOGO = (ANGULO_LOGO + 2) % 360
            img_rot = pygame.transform.rotate(img_res, ANGULO_LOGO)
            rect_rot = img_rot.get_rect(center=(int(pupila_x), int(pupila_y)))
            mask_circ = pygame.Surface(img_rot.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(mask_circ, (255,255,255,255), (img_rot.get_width()//2, img_rot.get_height()//2), int(RADIO_PUPILA))
            img_rot.blit(mask_circ, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
            capa_ojo.blit(img_rot, rect_rot)
    elif dinero:
        # Pupila de $ negra
        dibujar_pupila_peso(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), int(RADIO_PUPILA))
    elif amor:
        # Pupila de Corazón 
        dibujar_pupila_corazon(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), RADIO_PUPILA)
    else:
        # Pupila normal
        pygame.draw.circle(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), int(RADIO_PUPILA))
    
    capa_ojo.blit(mascara_esclerotica, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    lienzo.blit(capa_ojo, (0, 0))

    # Capa Brillo
    capa_brillo.fill((0, 0, 0, 0))
    if not (especial or glitch):
        b_color = (255, 255, 255, 200) if (amor or dinero) else (255, 255, 255, 140)
        # Ajustamos el brillo para que quede bien sobre la forma del $
        b_offset = RADIO_PUPILA * 0.4 if dinero else RADIO_PUPILA * 0.3
        b_x, b_y = pupila_x - (b_offset), pupila_y - (b_offset)
        # El brillo debe cortarse con la esclerótica pero no con la pupila $
        pygame.draw.circle(capa_brillo, b_color, (int(b_x), int(b_y)), int(RADIO_PUPILA * 0.35))
    
    capa_brillo.blit(mascara_esclerotica, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    lienzo.blit(capa_brillo, (0, 0))

    # Capa Párpados
    if frames_parpadeo:
        if animando:
            lienzo.blit(frames_parpadeo[int(frame_actual)], (0, 0))
            frame_actual += velocidad_anim
            if frame_actual >= len(frames_parpadeo):
                animando = False
                frame_actual = 1.0 if amor else (2.0 if drogado else 0.0)
        else:
            f_idle = 1 if amor else (2 if drogado else 0)
            lienzo.blit(frames_parpadeo[f_idle], (0, 0))

    pantalla.blit(pygame.transform.scale(lienzo, (ANCHO_REAL, ALTO_REAL)), (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()