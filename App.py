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

# Colores y Configuración Base
BLANCO, NEGRO = (255, 255, 255), (0, 0, 0)
IRIS_NORMAL = (50, 100, 150)
COLOR_AMOR = (255, 100, 180) 
COLOR_DINERO_VERDE = (50, 200, 50) # Verde vibrante estilo billete

centro_x, centro_y = RES_VIRTUAL[0] // 2, RES_VIRTUAL[1] // 2
pupila_x, pupila_y = centro_x, centro_y
radio_pupila = 16 
angulo_logo = 0

# --- CARGA DE ASSETS ---
ruta_media = "media" 
frames_parpadeo = []
for i in range(5):
    ruta = os.path.join(ruta_media, f"Eye-{i}.png")
    try:
        img = pygame.image.load(ruta).convert_alpha()
        frames_parpadeo.append(pygame.transform.scale(img, RES_VIRTUAL))
    except: pass

try:
    img_especial = pygame.image.load(os.path.join(ruta_media, "Posdata-Logo.png")).convert_alpha()
except:
    img_especial = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(img_especial, (200, 0, 0), (50, 50), 45)

# --- FUNCIONES DE DIBUJO ---
def dibujar_corazon(superficie, color, pos, tam):
    puntos = []
    for t in [x * 0.1 for x in range(0, 63)]:
        x = 16 * math.sin(t)**3
        y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        puntos.append((pos[0] + x * (tam/15), pos[1] + y * (tam/15)))
    if len(puntos) > 2:
        pygame.draw.polygon(superficie, color, puntos)

def dibujar_pupila_peso(superficie, color, pos, tam):
    # Dibuja un '$' estilizado y grueso como forma poligonal (pupila negra)
    ancho = int(tam * 1.3)
    alto = int(tam * 1.8)
    x, y = int(pos[0]), int(pos[1])
    
    # Grosor de las barras del símbolo
    g = int(max(2, tam / 5)) 
    
    # --- Puntos para la forma 'S' gruesa ---
    # Top bar, curva superior, barra media, curva inferior, bottom bar
    anch_s = ancho // 2
    alt_s = alto // 2
    
    # Definimos la forma 'S' como un trazo grueso poligonal
    # Esbozo rápido de la forma 'S' gruesa
    puntos_s_forma = [
        (x + anch_s, y - alt_s + g),        # 1 Top-right interior
        (x + anch_s, y - alt_s),            # 2 Top-right exterior
        (x - anch_s, y - alt_s),            # 3 Top-left exterior
        (x - anch_s, y),                    # 4 Mid-left exterior
        (x + anch_s - g, y),                # 5 Mid-right interior S superior
        (x + anch_s - g, y - alt_s + g),    # 6 Top-right interior S superior
        # Volvemos para cerrar la parte superior
        (x - anch_s + g, y - alt_s + g),    # Cierre 1
        (x - anch_s + g, y - g),            # Cierre 2
        
        # Parte inferior de la S
        (x + anch_s, y - g),                # Mid-right exterior S inferior
        (x + anch_s, y + alt_s),            # Bottom-right exterior
        (x - anch_s, y + alt_s),            # Bottom-left exterior
        (x - anch_s, y + alt_s - g),        # Bottom-left interior
        (x + anch_s - g, y + alt_s - g),    # Bottom-right interior
        (x + anch_s - g, y + g),            # Mid-right interior S inferior
        
        # Cierre final de la forma S
        (x - anch_s, y + g),                # Cierre 3
        (x - anch_s, y),                    # Cierre 4 (conecta con mid-left anterior)
        (x - anch_s + g, y),                # Cierre 5
        (x - anch_s + g, y + alt_s - g),    # Cierre 6
    ]
    # En realidad dibujar una S poligonal gruesa es complejo.
    # Usaremos una aproximación más sencilla: dibujar la S con líneas MUY gruesas
    # Y luego la línea vertical.
    
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
    if dinero: 
        # Latido rítmico para la pupila $, oscila entre 22 y 28 (se ve el iris verde radio 32)
        latido = math.sin(tiempo_ahora * 0.01) * 3
        radio_target = 25 + latido
    elif especial: radio_target = 40
    elif amor: radio_target = 25
    elif glitch: radio_target = random.choice([10, 35, 5])
    elif drogado or teclas[pygame.K_KP_MINUS]: radio_target = 8
    elif teclas[pygame.K_KP_PLUS]: radio_target = 30
    else: radio_target = 16
    
    radio_pupila += (radio_target - radio_pupila) * 0.1

    # --- PARPADEOS ---
    if not animando and tiempo_ahora - timer_parpadeo > proximo_parpadeo:
        animando = True
        frame_actual = 0.0 if (especial or dinero or glitch or not (amor or drogado)) else (1.0 if amor else 2.0)
        timer_parpadeo = tiempo_ahora
        proximo_parpadeo = random.randint(2000, 6000)

    # --- DIBUJO ---
    lienzo.fill(NEGRO)
    pygame.draw.ellipse(lienzo, BLANCO, (centro_x - 70, centro_y - 45, 140, 90))

    capa_ojo.fill((0, 0, 0, 0))
    
    # Color Iris
    color_iris = COLOR_DINERO_VERDE if dinero else (random.choice([IRIS_NORMAL, (150, 150, 150)]) if glitch else (COLOR_AMOR if amor else IRIS_NORMAL))

    # Dibujo del Iris (fijo en radio 32)
    pygame.draw.circle(capa_ojo, color_iris, (int(pupila_x), int(pupila_y)), 32)
    
    # --- DIBUJO DE PUPILA (TRANSFORMACIÓN) ---
    if especial:
        pygame.draw.circle(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), int(radio_pupila))
        tam_logo = int(radio_pupila * 1.8)
        if tam_logo > 5:
            img_res = pygame.transform.scale(img_especial, (tam_logo, tam_logo))
            angulo_logo = (angulo_logo + 2) % 360
            img_rot = pygame.transform.rotate(img_res, angulo_logo)
            rect_rot = img_rot.get_rect(center=(int(pupila_x), int(pupila_y)))
            mask_circ = pygame.Surface(img_rot.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(mask_circ, (255,255,255,255), (img_rot.get_width()//2, img_rot.get_height()//2), int(radio_pupila))
            img_rot.blit(mask_circ, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
            capa_ojo.blit(img_rot, rect_rot)
    elif dinero:
        # --- NUEVA PUPILA $ (Transformación total de la forma negra) ---
        # Dibujamos la forma negra del $ directamente sobre el iris verde
        # Usamos líneas muy gruesas para simular la "masa" de la pupila transformándose
        dibujar_pupila_peso(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), int(radio_pupila))
    elif amor:
        # Pupila de Corazón NEGRA
        dibujar_corazon(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), radio_pupila)
    else:
        # Pupila normal NEGRA circular
        pygame.draw.circle(capa_ojo, NEGRO, (int(pupila_x), int(pupila_y)), int(radio_pupila))
    
    capa_ojo.blit(mascara_esclerotica, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    lienzo.blit(capa_ojo, (0, 0))

    # Capa Brillo
    capa_brillo.fill((0, 0, 0, 0))
    if not (especial or glitch):
        b_color = (255, 255, 255, 200) if (amor or dinero) else (255, 255, 255, 140)
        # Ajustamos el brillo para que quede bien sobre la forma del $
        b_offset = radio_pupila * 0.4 if dinero else radio_pupila * 0.3
        b_x, b_y = pupila_x - (b_offset), pupila_y - (b_offset)
        # El brillo debe cortarse con la esclerótica pero no con la pupila $
        pygame.draw.circle(capa_brillo, b_color, (int(b_x), int(b_y)), int(radio_pupila * 0.35))
    
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