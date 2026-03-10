
import math
import pygame

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
