import pygame
import random
import math

#iniciar la pantalla
pygame.init()

#color y tamaño de la pantalla
ANCHO_VENTANA = 800
ALTO_VENTANA = 800
COLOR_AMARILLO = (255, 255, 0)
COLOR_CELESTE = (0, 0, 128)
COLOR_VERDE = (0, 255, 0)
COLOR_ROJO = (255, 0, 0)
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)

#crear la pantalla
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

#titulo en la pantalla (arriba)
pygame.display.set_caption("GREEN BALLS")

#posicion y radio del círculo controlado por el jugador (AMARILLO)
posicion_circulo = [100, 100]
radio_circulo = 20  # El jugador comienza con un radio de 20


#numero de círculos pequeños y su tamaño (comida)
num_circulos_pequeños = 55
radio_circulos_pequeños = 7
circulos_pequeños = []

#función para generar un círculo pequeño en una posición aleatoria
def generar_circulo_pequeño():
    x = random.randint(radio_circulos_pequeños, ANCHO_VENTANA - radio_circulos_pequeños)
    y = random.randint(radio_circulos_pequeños, ALTO_VENTANA - radio_circulos_pequeños)
    return [x, y]

#generar posiciones aleatorias para los círculos pequeños
for _ in range(num_circulos_pequeños):
    circulos_pequeños.append(generar_circulo_pequeño())

#posición, tamaño y velocidad del círculo enemigo (rojo)
posicion_enemigo = [random.randint(50, ANCHO_VENTANA - 50), random.randint(50, ALTO_VENTANA - 50)]
radio_enemigo = 85
enemigo_velocidad = [random.uniform(0, 0.4), random.uniform(0, 0.4)]  

#texto cuando perdes
fuente = pygame.font.Font(None, 40)

#variable para controlar el estado del juego
perdio = False
ganaste = False  #variable para controlar si el jugador gano

#función para verificar colisiones
def hay_colision(x1, y1, r1, x2, y2, r2):
    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distancia < r1 + r2

#juego
flag_correr = True
enemigo_vivo = True

while flag_correr:
    
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag_correr = False

    #salgo del for para ver que teclas están presionadas, se lee todo el tiempo
    #funciona mientras las teclas están presionadas
    lista_teclas = pygame.key.get_pressed()

    #movimiento del círculo controlado por el jugador
    if not perdio and not ganaste:  # Solo mover el jugador si no ha perdido ni ha ganado
        if lista_teclas[pygame.K_RIGHT] and posicion_circulo[0] + radio_circulo < ANCHO_VENTANA:
            posicion_circulo[0] += 0.13 #se mueve 0.13 pixel siempre que la tecla está presionada
        if lista_teclas[pygame.K_LEFT] and posicion_circulo[0] - radio_circulo > 0:
            posicion_circulo[0] -= 0.13
        if lista_teclas[pygame.K_UP] and posicion_circulo[1] - radio_circulo > 0:
            posicion_circulo[1] -= 0.13
        if lista_teclas[pygame.K_DOWN] and posicion_circulo[1] + radio_circulo < ALTO_VENTANA:
            posicion_circulo[1] += 0.13

    #limpiar la pantalla con color de fondo
    if perdio:
        pantalla.fill(COLOR_NEGRO)  #pantalla negra si perdio
    else:
        pantalla.fill(COLOR_CELESTE)

    #dibujar el círculo controlado por el jugador solo si no ha perdido ni ganado
    if not perdio and not ganaste:
        pygame.draw.circle(pantalla, COLOR_AMARILLO, (int(posicion_circulo[0]), int(posicion_circulo[1])), int(radio_circulo))

    #movimiento aleatorio del enemigo (ROJO)
    if enemigo_vivo and not perdio and not ganaste:
        #actualizar la posición del enemigo
        posicion_enemigo[0] += enemigo_velocidad[0]
        posicion_enemigo[1] += enemigo_velocidad[1]

        #verificar si el enemigo choca con los bordes de la pantalla y cambia la dirección
        if posicion_enemigo[0] - radio_enemigo < 0 or posicion_enemigo[0] + radio_enemigo > ANCHO_VENTANA:
            enemigo_velocidad[0] *= -1
        if posicion_enemigo[1] - radio_enemigo < 0 or posicion_enemigo[1] + radio_enemigo > ALTO_VENTANA:
            enemigo_velocidad[1] *= -1

        #dibujar el círculo enemigo (ROJO)
        pygame.draw.circle(pantalla, COLOR_ROJO, (int(posicion_enemigo[0]), int(posicion_enemigo[1])), radio_enemigo)

        #verificar colisión con el círculo enemigo
        if hay_colision(posicion_circulo[0], posicion_circulo[1], radio_circulo, posicion_enemigo[0], posicion_enemigo[1], radio_enemigo):
            if radio_circulo > radio_enemigo:
                enemigo_vivo = False  #eliminar al enemigo
                radio_circulo += 4  #aumentar el tamaño del jugador

                #se verifica si el jugador gano
                if radio_circulo >= 100:  
                    ganaste = True  
            else:
                #el jugador pierde si el enemigo es más grande y  se lo come
                perdio = True  #cambiar el estado a perdido

    #dibujar y verificar colisiones con los círculos pequeños
    for circulo in circulos_pequeños[:]:
        pygame.draw.circle(pantalla, COLOR_VERDE, (int(circulo[0]), int(circulo[1])), radio_circulos_pequeños)
        
        #verificar si el círculo del jugador colisiona con un círculo pequeño
        if not perdio and not ganaste and hay_colision(posicion_circulo[0], posicion_circulo[1], radio_circulo, circulo[0], circulo[1], radio_circulos_pequeños):
            circulos_pequeños.remove(circulo)  #eliminar el círculo pequeño
            radio_circulo += 1.5  # incrementar el radio del círculo del jugador

            #generar un nuevo circulo pequeño (verde)
            circulos_pequeños.append(generar_circulo_pequeño())

    #si el jugador perdio, mostrar el mensaje!!!
    if perdio:
        texto = fuente.render("PERDISTE - Presiona espacio para intentarlo de nuevo!", True, COLOR_BLANCO)
        rect_texto = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        pantalla.blit(texto, rect_texto)  #dibujar el texto en la pantalla

        #eperar a que el jugador apriete la tecla para reiniciar
        if lista_teclas[pygame.K_SPACE]:  #reiniciar al apretar la barra espaciadora
            #reiniciar el juego
            perdio = False
            ganaste = False  #reiniciar el estado de ganado
            posicion_circulo = [100, 100]
            radio_circulo = 20
            circulos_pequeños.clear()  #limpiar los círculos pequeños
            for _ in range(num_circulos_pequeños):
                circulos_pequeños.append(generar_circulo_pequeño())
            enemigo_vivo = True
            posicion_enemigo = [random.randint(50, ANCHO_VENTANA - 50), random.randint(50, ALTO_VENTANA - 50)]
            enemigo_velocidad = [random.uniform(0, 0.4), random.uniform(0, 0.4)]  #reiniciar la velocidad del enemigo

    #si el jugador gano, mostrar el mensaje!!! =)
    if ganaste:
        texto = fuente.render("¡GANASTE!", True, COLOR_BLANCO)
        rect_texto = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        pantalla.blit(texto, rect_texto)  #dibujar el texto en la pantalla

        #esperar a que el jugador presione una tecla para reiniciar
        if lista_teclas[pygame.K_SPACE]:  #reiniciar al apretar la barra espaciadora
            # Reiniciar el juego
            perdio = False
            ganaste = False  #reiniciar el estado de ganado
            posicion_circulo = [100, 100]
            radio_circulo = 20
            circulos_pequeños.clear()  #limpiar los círculos pequeños
            for _ in range(num_circulos_pequeños):
                circulos_pequeños.append(generar_circulo_pequeño())
            enemigo_vivo = True
            posicion_enemigo = [random.randint(50, ANCHO_VENTANA - 50), random.randint(50, ALTO_VENTANA - 50)]
            enemigo_velocidad = [random.uniform(0, 0.4), random.uniform(0, 0.4)]  #reiniciar la velocidad del enemigo

    #actualizar la pantalla
    pygame.display.flip()

#cerrar pygame
pygame.quit()

