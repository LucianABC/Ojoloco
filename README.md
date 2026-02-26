=====================================================
      MANUAL DE USUARIO - OJO ANIMADO PIXEL ART
=====================================================

Este programa simula un ojo interactivo con múltiples 
expresiones, control de pupila y movimiento suave.

-----------------------------------------------------
CONTROLES Y ESTADOS
-----------------------------------------------------
El ojo parpadea solo de forma aleatoria cada 2 a 6 segundos.

* Flechas y Teclado Numérico (Numpad): Dirección de la pupila
    - [8]: Arriba          - [2]: Abajo
    - [4]: Izquierda       - [6]: Derecha
    - [7, 9, 1, 3]: Diagonales (Esquinas)

* [+]: Dilatar (Pupila grande)
* [-]: Contraer (Pupila pequeña)
* [D] - MODO DROGADO/CANSADO:
    - Párpado entrecerrado (Frame 2).
    - Pupila contraída automáticamente.
    - El parpadeo automático vuelve al estado entrecerrado.

* [H] - MODO AMOR:
    - El Iris cambia a color ROSADO.
    - La Pupila se transforma en un CORAZÓN.
    - Párpado levemente entrecerrado (Frame 1).
    - Brillo especial transparente sobre el corazón.

-----------------------------------------------------
NOTAS TÉCNICAS
-----------------------------------------------------
* Archivos requeridos: /media/Eye-0.png hasta Eye-4.png
* Resolución Virtual: 160x120 (Escalado a 640x480)
* El brillo posee transparencia (Alpha 140-160) y está
  sujeto a la máscara de la esclerótica.