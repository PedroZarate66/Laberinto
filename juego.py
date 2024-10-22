import pygame
import sys
import time
import random

def colocar_monedas(laberinto, recompensas):
    # Encontrar las posiciones disponibles (celdas con valor 0)
    posiciones_disponibles = [(i, j) for i in range(len(laberinto)) for j in range(len(laberinto[0])) if laberinto[i][j] == 0]
    # Elegir posiciones aleatorias para las monedas
    posiciones_monedas = random.sample(posiciones_disponibles, recompensas)
    return posiciones_monedas  # Retornar las posiciones de las monedas para dibujarlas después


def colocar_enemigos(laberinto, enemigos):
    # Encontrar las posiciones disponibles (celdas con valor 0)
    posiciones_disponibles = [(i, j) for i in range(len(laberinto)) for j in range(len(laberinto[0])) if laberinto[i][j] == 0]
    # Elegir posiciones aleatorias para las monedas
    posiciones_enemigos = random.sample(posiciones_disponibles, enemigos)
    return posiciones_enemigos  # Retornar las posiciones de las monedas para dibujarlas después

def mostrar_menu_ganador(pantalla, fuente, score, tiempo_transcurrido):
    # Definir los colores
    BLANCO = (255, 255, 255)
    GRIS = (100, 100, 100)
    AMARILLO = (255, 183, 3)
    AZUL = (2, 48, 71)
    SKYBLUE = (33, 158, 188)
    NEGRO = (0, 0, 0)

    pantalla.fill(NEGRO)

   # Mostrar mensaje de victoria
    texto_ganador = fuente.render("¡Has ganado!", True, AMARILLO)
    pantalla.blit(texto_ganador, (300, 150)) 
    texto_puntaje = fuente.render(f"Puntaje: {score}", True, BLANCO)
    pantalla.blit(texto_puntaje, (300, 200))  

    # Mostrar el tiempo transcurrido
    minutos = int(tiempo_transcurrido // 60)
    segundos = int(tiempo_transcurrido % 60)
    texto_tiempo = fuente.render(f"Tiempo: {minutos:02}:{segundos:02}", True, BLANCO)
    pantalla.blit(texto_tiempo, (350, 600))

    # Definir los botones
    opciones = ["Reiniciar", "Menú", "Salir"]
    seleccion = 0  # Opción seleccionada

    # Bucle para el menú
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)  # Navegar hacia arriba
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)  # Navegar hacia abajo
                if evento.key == pygame.K_RETURN:  # Al presionar Enter
                    return opciones[seleccion].lower().replace(" ", "_")  # Devuelve la opción seleccionada en minúsculas

        # Dibujar los botones
        for i, opcion in enumerate(opciones):
            color = AZUL if i == seleccion else SKYBLUE
            boton_rect = pygame.Rect(350, 300 + i * 100, 200, 50)
            pygame.draw.rect(pantalla, color, boton_rect)
            texto_opcion = fuente.render(opcion, True, BLANCO)
            pantalla.blit(texto_opcion, (boton_rect.x + 50, boton_rect.y + 10))

        pygame.display.flip()

def ejecutar_laberinto(nivel, enemigos, recompensas, mejoras, pared):
    # Inicializar Pygame
    pygame.init()

    # Definir colores
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    ROJO = (255, 0, 0)
    AZUL = (0, 0, 255)

    # Fuente para el texto
    fuente = pygame.font.Font(None, 30)
    fuenteGanador = pygame.font.Font(None, 45)
    # Tamaño de cada celda del laberinto
    TAMANO_CELDA = 22

    # Configuración de la ventana
    ANCHO, ALTO = 925, 650
    pantalla = pygame.display.set_mode((ANCHO, ALTO))

    pygame.display.set_caption("Juego del Laberinto")

    # Posición inicial del jugador
    jugador_x = 1
    jugador_y = 1

    # Definir la posición de la meta
    meta_x = len(laberinto[0]) - 2
    meta_y = len(laberinto) - 2

    img_clock = pygame.image.load('./img/clock.png')
    img_clock = pygame.transform.scale(img_clock, (40, 40))
    img_recompensas = pygame.image.load('./img/puntaje.png')
    img_recompensas = pygame.transform.scale(img_recompensas, (40, 40))
    img_moneda= pygame.image.load('./img/moneda.png')
    img_moneda = pygame.transform.scale(img_moneda, (20, 20))
    img_meta= pygame.image.load('./img/meta_castillo.png')
    img_meta = pygame.transform.scale(img_meta, (50, 60))

    img_enemigo = pygame.image.load('./img/enemigo.jpg')
    img_enemigo = pygame.transform.scale(img_enemigo, (20, 20))
    
     # Colocar monedas en el laberinto (solo una vez)
    posiciones_monedas = colocar_monedas(laberinto, recompensas)

    # Colocar enemigos en el laberinto (solo una vez)
    posiciones_enemigos = colocar_enemigos(laberinto, enemigos)


    # Variable de puntaje
    score = 0

    tiempo_inicio = time.time() 

    # Ciclo principal del juego
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detectar teclas presionadas para mover al jugador
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    if laberinto[jugador_y][jugador_x - 1] == 0:
                        jugador_x -= 1
                if evento.key == pygame.K_RIGHT:
                    if laberinto[jugador_y][jugador_x + 1] == 0:
                        jugador_x += 1
                if evento.key == pygame.K_UP:
                    if laberinto[jugador_y - 1][jugador_x] == 0:
                        jugador_y -= 1
                if evento.key == pygame.K_DOWN:
                    if laberinto[jugador_y + 1][jugador_x] == 0:
                        jugador_y += 1

        
        # Comprobar si el jugador ha alcanzado la meta
        if jugador_x == meta_x and jugador_y == meta_y:
            tiempo_transcurrido = time.time() - tiempo_inicio  # Calcula el tiempo transcurrido
            opcion = mostrar_menu_ganador(pantalla, fuenteGanador, score, tiempo_transcurrido)
            return opcion

        # Detectar colisiones con las monedas
        enemigos_restantes = []
        for (enemigos_x, enemigos_y) in posiciones_enemigos:
            if jugador_x == enemigos_y and jugador_y == enemigos_x:
                 score = score  # Aumenta el puntaje cuando el jugador recoge una moneda
            else:
                enemigos_restantes.append((enemigos_x, enemigos_y))  # Moneda no recolectada

        posiciones_enemigos = enemigos_restantes

            #posiciones enemigos
        monedas_restantes = []
        for (moneda_x, moneda_y) in posiciones_monedas:
            if jugador_x == moneda_y and jugador_y == moneda_x:
                score += 1  # Aumenta el puntaje cuando el jugador recoge una moneda
            else:
                monedas_restantes.append((moneda_x, moneda_y))  # Moneda no recolectada

        posiciones_monedas = monedas_restantes

        # Dibujar el laberinto
        pantalla.fill(NEGRO)
        for fila in range(len(laberinto)):
            for col in range(len(laberinto[fila])):
                if laberinto[fila][col] == 1:  # Si es una pared
                    pantalla.blit(pared, (col * TAMANO_CELDA, fila * TAMANO_CELDA))
                elif laberinto[fila][col] == 0:
                    pygame.draw.rect(pantalla, BLANCO, (col * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
        
        # Dibujar las monedas
        for (x, y) in posiciones_monedas:
            pantalla.blit(img_moneda, (y * TAMANO_CELDA, x * TAMANO_CELDA))

        # # Dibujar enemigos
        for (x, y) in posiciones_enemigos:
            pantalla.blit(img_enemigo, (y * TAMANO_CELDA, x * TAMANO_CELDA))

        # Dibujar al jugador
        pygame.draw.rect(pantalla, ROJO, (jugador_x * TAMANO_CELDA, jugador_y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

        # Dibujar la meta
        pantalla.blit(img_meta, (meta_x * TAMANO_CELDA, meta_y * TAMANO_CELDA))

        # Actualizar el tiempo transcurrido
        tiempo_transcurrido = time.time() - tiempo_inicio
        minutos = int(tiempo_transcurrido // 60)  
        segundos = int(tiempo_transcurrido % 60)
        texto_tiempo = fuente.render(f"{minutos:02}:{segundos:02}", True, (255, 255, 0))

        # Mostrar los parámetros horizontalmente
        pantalla.blit(texto_tiempo, (50, ALTO - 50))
        pantalla.blit(img_clock, (10, ALTO - 60))  
        pantalla.blit(fuente.render(f"Nivel: {nivel}", True, BLANCO), (140, ALTO - 50))
        pantalla.blit(img_recompensas, (300, ALTO - 60))
        pantalla.blit(fuente.render(f"{score}", True, BLANCO), (350, ALTO - 50))
        pantalla.blit(fuente.render(f"Mejoras: {mejoras}", True, BLANCO), (400, ALTO - 50))
        pantalla.blit(fuente.render(f"Enemigos: {enemigos}", True, BLANCO), (550, ALTO - 50))


        # Actualizar la pantalla
        pygame.display.flip()

# Definir la matriz del laberinto
laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]

]

# Llamar a la función para ejecutar el juego
if __name__ == "__main__":
    ejecutar_laberinto()
