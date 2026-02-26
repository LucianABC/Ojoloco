import pygame
import sys
import random
import os
import math

pygame.init()

# --- CONFIGURACIÓN PIXEL ART ---
RES_VIRTUAL = (160, 120) 
ANCHO_REAL, ALTO_REAL = 640, 480
pantalla = pygame.display.set_mode((ANCHO_REAL, ALTO_REAL))
lienzo = pygame.Surface(RES_VIRTUAL)

# Colores
BLANCO, NEGRO = (255, 255, 255), (0, 0, 0)
IRIS_NORMAL = (50, 100, 150)
COLOR_AMOR = (255, 100, 180) 

centro_x, centro_y = RES_VIRTUAL[0] // 2, RES_VIRTUAL[1] // 2
pupila_x, pupila_y = centro_x, centro_y
radio_pupila = 16 

# --- CARGA DE FRAMES ---
ruta_media = "media" 
frames_parpadeo = []
for i in range(5):
    ruta = os.path.join(ruta_media, f"Eye-{i}.png")
    try:
        img = pygame.image.load(ruta).convert_alpha()
        frames_parpadeo.append(pygame.transform.scale(img, RES_VIRTUAL))
    except: pass

def dibujar_corazon(superficie, color, pos, tam):
    puntos = []
    for t in [x * 0.1 for x in range(0, 63)]:
        x = 16 * math.sin(t)**3
        y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        puntos.append((pos[0] + x * (tam/15), pos[1] + y * (tam/15)))
    if len(puntos) > 2:
        pygame.draw.polygon(superficie, color, puntos)

# Animación y Capas
frame_actual = 0.0
velocidad_anim = 0.35
animando = False
timer_parpadeo = pygame.time.get_ticks()
proximo_parpadeo = random.randint(2000, 5000)

mascara = pygame.Surface(RES_VIRTUAL, pygame.SRCALPHA)
pygame.draw.ellipse(mascara, (255, 255, 255, 255), (centro_x - 70, centro_y - 45, 140, 90))
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

    # --- MOVIMIENTO DIAGONALES ---
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

    target_x, target_y = centro_x + dx, centro_y + dy
    pupila_x += (target_x - pupila_x) * 0.15
    pupila_y += (target_y - pupila_y) * 0.15

    # --- LÓGICA DE TAMAÑO (RESTAURADA Y PRIORIZADA) ---
    if amor:
        radio_target = 25
    elif drogado or teclas[pygame.K_KP_MINUS]:
        radio_target = 8
    elif teclas[pygame.K_KP_PLUS]:
        radio_target = 30
    else:
        radio_target = 16
    
    radio_pupila += (radio_target - radio_pupila) * 0.1

    # --- LÓGICA DE PARPADEOS ---
    if not animando and tiempo_ahora - timer_parpadeo > proximo_parpadeo:
        animando = True
        frame_actual = 1.0 if amor else (2.0 if drogado else 0.0)
        timer_parpadeo = tiempo_ahora
        proximo_parpadeo = random.randint(2000, 6000)

   # --- DIBUJO ---
    lienzo.fill(NEGRO)
    pygame.draw.ellipse(lienzo, BLANCO, (centro_x - 70, centro_y - 45, 140, 90))

    # Capa Ojo (Iris + Pupila)
    capa_ojo.fill((0, 0, 0, 0))
    color_iris = COLOR_AMOR if amor else IRIS_NORMAL
    pygame.draw.circle(capa_ojo, color_iris, (int(pupila_x), int(pupila_y)), 32)
    
    if amor:
        dibujar_corazon(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), radio_pupila)
    else:
        pygame.draw.circle(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), int(radio_pupila))
    
    capa_ojo.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    lienzo.blit(capa_ojo, (0, 0))

    # --- CAPA BRILLO (CORREGIDA PARA MODO AMOR) ---
    capa_brillo.fill((0, 0, 0, 0))
    if amor:
        # Brillo "coqueto" pero con transparencia (160 en vez de 220 para que se note el iris detrás)
        pygame.draw.circle(capa_brillo, (255, 255, 255, 160), (int(pupila_x-6), int(pupila_y-6)), 5)
    else:
        # Brillo normal transparente
        b_x, b_y = pupila_x - (radio_pupila * 0.3), pupila_y - (radio_pupila * 0.3)
        pygame.draw.circle(capa_brillo, (255, 255, 255, 140), (int(b_x), int(b_y)), int(radio_pupila * 0.35))
    
    # Aplicamos la máscara también al brillo para que no se salga del ojo en las esquinas
    capa_brillo.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
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