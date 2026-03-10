import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No se detectó ningún control arcade. Revisa el USB.")
    quit()

# Usar el primer control detectado
control = pygame.joystick.Joystick(0)
control.init()

print(f"Control detectado: {control.get_name()}")
print("Presiona botones o mueve la palanca para ver los índices...")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Detectar Botones
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"BOTÓN presionado: {event.button}")
            
        # Detectar Palanca (Ejes)
        if event.type == pygame.JOYAXISMOTION:
            if abs(event.value) > 0.5: # Filtro de sensibilidad
                print(f"EJE {event.axis} movido a {event.value}")

        # Detectar la palanca si se comporta como un HAT (común en kits arcade)
        if event.type == pygame.JOYHATMOTION:
            print(f"HAT (Palanca) movido a: {event.value}")

pygame.quit()