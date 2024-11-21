import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Reloj para controlar FPS
reloj = pygame.time.Clock()

# Tamaño de los bloques
BLOQUE_SIZE = 40

# Clase Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOQUE_SIZE, BLOQUE_SIZE))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 5

    def update(self, teclas):
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad

# Clase Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOQUE_SIZE, BLOQUE_SIZE))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = random.choice([-3, 3])

    def update(self):
        self.rect.x += self.velocidad
        if self.rect.x <= 0 or self.rect.x >= ANCHO - BLOQUE_SIZE:
            self.velocidad *= -1

# Clase Moneda
class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOQUE_SIZE // 2, BLOQUE_SIZE // 2))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Clase Pared
class Pared(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOQUE_SIZE, BLOQUE_SIZE))
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Crear laberinto
def crear_laberinto():
    paredes = pygame.sprite.Group()
    layout = [
        "WWWWWWWWWWWWWWWWWWWW",
        "W                  W",
        "W  WWWW   WWWWW    W",
        "W  W      W        W",
        "W  W      W    WWWWW",
        "W        WW         W",
        "WWWWWWWWWWWWWWWWWWWWW"
    ]

    for fila_idx, fila in enumerate(layout):
        for col_idx, col in enumerate(fila):
            if col == "W":
                pared = Pared(col_idx * BLOQUE_SIZE, fila_idx * BLOQUE_SIZE)
                paredes.add(pared)
    return paredes

# Función principal
def ejecutar_laberinto():
    jugador = Jugador(50, 50)
    enemigos = pygame.sprite.Group()
    monedas = pygame.sprite.Group()
    paredes = crear_laberinto()
    todos_sprites = pygame.sprite.Group(jugador)

    # Crear enemigos
    for i in range(5):
        x = random.randint(0, ANCHO - BLOQUE_SIZE)
        y = random.randint(0, ALTO - BLOQUE_SIZE)
        enemigo = Enemigo(x, y)
        enemigos.add(enemigo)
        todos_sprites.add(enemigo)

    # Crear monedas
    for i in range(10):
        x = random.randint(0, ANCHO - BLOQUE_SIZE)
        y = random.randint(0, ALTO - BLOQUE_SIZE)
        moneda = Moneda(x, y)
        monedas.add(moneda)
        todos_sprites.add(moneda)

    # Loop del juego
    puntuacion = 0
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # Actualizar sprites
        teclas = pygame.key.get_pressed()
        jugador.update(teclas)
        enemigos.update()

        # Colisiones
        if pygame.sprite.spritecollideany(jugador, enemigos):
            print("¡Has perdido!")
            ejecutando = False

        monedas_recogidas = pygame.sprite.spritecollide(jugador, monedas, True)
        puntuacion += len(monedas_recogidas)

        # Dibujar todo
        screen.fill(BLANCO)
        paredes.draw(screen)
        todos_sprites.draw(screen)

        # Mostrar puntuación
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"Puntuación: {puntuacion}", True, NEGRO)
        screen.blit(texto, (10, 10))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

# Ejecutar el juego
if __name__ == "__main__":
    ejecutar_laberinto()
