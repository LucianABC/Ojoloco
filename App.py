import pygame
import sys
import random
import os
import math
from constants import (
    BLANCO, NEGRO, IRIS_NORMAL, ROSA_AMOR, VERDE_DINERO, 
    RADIO_PUPILA_BASE, RADIO_PUPILA_AMOR, RADIO_PUPILA_DINERO, 
    RADIO_PUPILA_DROGADO, RADIO_PUPILA_LOGO, RES_VIRTUAL,
    ANCHO_REAL, ALTO_REAL, ANGULO_LOGO, CANTIDAD_FRAMES
)
from utils import dibujar_pupila_corazon, dibujar_pupila_peso

# --- INICIALIZACIÓN ---
pygame.init()
pygame.joystick.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

joysticks = []
for i in range(pygame.joystick.get_count()):
    j = pygame.joystick.Joystick(i)
    j.init()
    joysticks.append(j)

pygame.display.set_caption("V.I.G.I.L.A. v1.0")
pantalla = pygame.display.set_mode((ANCHO_REAL, ALTO_REAL), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.mouse.set_visible(False)
lienzo = pygame.Surface(RES_VIRTUAL)

centro_x, centro_y = RES_VIRTUAL[0] // 2, RES_VIRTUAL[1] // 2
pupila_x, pupila_y = centro_x, centro_y
radio_actual = RADIO_PUPILA_BASE 
angulo_actual_logo = ANGULO_LOGO

# --- CARGA DE ASSETS ---
frames_parpadeo = []
for i in range(CANTIDAD_FRAMES):
    ruta = os.path.join("media", f"Eye-{i}.png")
    try:
        img = pygame.image.load(ruta).convert_alpha()
        frames_parpadeo.append(pygame.transform.scale(img, RES_VIRTUAL))
    except:
        print(f"Error cargando: {ruta}")

try:
    logo_posdata = pygame.image.load(os.path.join("media", "Posdata-Logo.png")).convert_alpha()
except:
    logo_posdata = pygame.Surface((100, 100), pygame.SRCALPHA)

# --- VARIABLES DE ANIMACIÓN ---
frame_actual_anim = 0.0
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
    pygame.event.pump()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- LECTURA DE ENTRADAS ---
    teclas = pygame.key.get_pressed()
    
    # Estados acumulativos
    amor = teclas[pygame.K_a]
    dinero = teclas[pygame.K_m]
    logo_animado = teclas[pygame.K_p]
    glitch = teclas[pygame.K_g]
    drogado = teclas[pygame.K_d]
    btn_mas = teclas[pygame.K_KP_PLUS] or teclas[pygame.K_PLUS]
    btn_menos = teclas[pygame.K_KP_MINUS] or teclas[pygame.K_MINUS]

    for joy in joysticks:
        if joy.get_button(0): amor = True
        if joy.get_button(1): dinero = True
        if joy.get_button(2): logo_animado = True
        if joy.get_button(3): drogado = True
        if joy.get_button(4): glitch = True
        if joy.get_button(5): btn_mas = True
        if joy.get_button(6): btn_menos = True

    # Movimiento
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

    if dx == 0 and dy == 0:
        for joy in joysticks:
            ex, ey = joy.get_axis(0), joy.get_axis(1)
            if abs(ex) > 0.3: dx = dist if ex > 0 else -dist
            if abs(ey) > 0.3: dy = dist if ey > 0 else -dist
            if dx == 0 and dy == 0 and joy.get_numhats() > 0:
                hat = joy.get_hat(0)
                if hat[0] != 0: dx = hat[0] * dist
                if hat[1] != 0: dy = -hat[1] * dist
                
    off_glitch_x = random.randint(-8, 8) if glitch else 0
    off_glitch_y = random.randint(-8, 8) if glitch else 0
    
    target_x = centro_x + dx + off_glitch_x
    target_y = centro_y + dy + off_glitch_y

    pupila_x += (target_x - pupila_x) * 0.15
    pupila_y += (target_y - pupila_y) * 0.15
    

    # --- LÓGICA DE TAMAÑO ---
    if dinero: 
        latido = math.sin(tiempo_ahora * 0.01) * 3
        radio_target = RADIO_PUPILA_DINERO + latido
    elif logo_animado: 
        radio_target = RADIO_PUPILA_LOGO
    elif amor: 
        latido = (math.sin(tiempo_ahora * 0.01) + math.sin(tiempo_ahora * 0.02) * 0.5) * 3
        radio_target = RADIO_PUPILA_AMOR + latido
    elif glitch: 
        radio_target = random.choice([10, 35, 5])
    elif btn_mas:
        radio_target = 30
    elif btn_menos or drogado:
        radio_target = RADIO_PUPILA_DROGADO
    else: 
        radio_target = RADIO_PUPILA_BASE
    
    radio_actual += (radio_target - radio_actual) * 0.1
    
    lienzo.fill(BLANCO)
    capa_ojo.fill(BLANCO)
    
    # Iris
    color_iris = IRIS_NORMAL
    if dinero:
        color_iris = VERDE_DINERO
    elif amor:
        color_iris = ROSA_AMOR
    elif glitch:
        color_iris = random.choice([IRIS_NORMAL, (150, 150, 150)])
    else:
        color_iris = IRIS_NORMAL
        
    pygame.draw.circle(capa_ojo, color_iris, (int(pupila_x), int(pupila_y)), 32)
    
    if logo_animado:
        pygame.draw.circle(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), int(radio_actual))
        tam_logo = int(radio_actual * 1.8)
        if tam_logo > 5:
            img_res = pygame.transform.scale(logo_posdata, (tam_logo, tam_logo))
            angulo_actual_logo = (angulo_actual_logo + 2) % 360 # Ahora sí rota
            img_rot = pygame.transform.rotate(img_res, angulo_actual_logo)
            rect_rot = img_rot.get_rect(center=(int(pupila_x), int(pupila_y)))
            
            # Máscara circular para el logo
            mask_circ = pygame.Surface(img_rot.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(mask_circ, (255,255,255,255), (img_rot.get_width()//2, img_rot.get_height()//2), int(radio_actual))
            img_rot.blit(mask_circ, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
            capa_ojo.blit(img_rot, rect_rot)
    elif dinero:
        dibujar_pupila_peso(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), int(radio_actual))
    elif amor:
        dibujar_pupila_corazon(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), radio_actual)
    else:
        # Pupila normal
        pygame.draw.circle(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), int(radio_actual))
    
    capa_ojo.blit(mascara_esclerotica, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    lienzo.blit(capa_ojo, (0, 0))

    # Brillo
    capa_brillo.fill((0, 0, 0, 0))
    if not (logo_animado or glitch):
        b_color = (255, 255, 255, 200) if (amor or dinero) else (255, 255, 255, 140)
        b_offset = radio_actual * 0.4 if dinero else radio_actual * 0.3
        b_x, b_y = pupila_x - b_offset, pupila_y - b_offset
        pygame.draw.circle(capa_brillo, b_color, (int(b_x), int(b_y)), int(radio_actual * 0.35))
    
    capa_brillo.blit(mascara_esclerotica, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    lienzo.blit(capa_brillo, (0, 0))

    # Párpados
    if not animando and tiempo_ahora - timer_parpadeo > proximo_parpadeo:
        animando = True
        frame_actual_anim = 0.0
        timer_parpadeo = tiempo_ahora
        proximo_parpadeo = random.randint(2000, 6000)

    if frames_parpadeo:
        if animando:
            lienzo.blit(frames_parpadeo[int(frame_actual_anim)], (0, 0))
            frame_actual_anim += velocidad_anim
            if frame_actual_anim >= len(frames_parpadeo):
                animando = False
        else:
            # Frame de reposo (0: Normal, 1: Amor, 2: Drogado)
            f_idle = 1 if amor else (2 if drogado else 0)
            lienzo.blit(frames_parpadeo[f_idle], (0, 0))

    pantalla.blit(pygame.transform.scale(lienzo, (ANCHO_REAL, ALTO_REAL)), (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
