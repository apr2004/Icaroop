import pygame
from pygame.locals import *
import random
import configuracion
from icarus import Icarus
from entorno import PlataformaMovil
from columnas import Columnas


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((configuracion.SCREEN_WIDTH, configuracion.SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Icarus')

flying = configuracion.FLYING
game_over = configuracion.GAME_OVER


# Grupos y objetos
# ícaro
icarus_group = pygame.sprite.Group()
icarus = Icarus(100, int(configuracion.SCREEN_HEIGHT/2))
icarus_group.add(icarus)

# columnas
columnas_group = pygame.sprite.Group()
bottom_column = Columnas(configuracion.SCREEN_WIDTH, int(configuracion.SCREEN_HEIGHT/2) + 118, -1)
top_column = Columnas(configuracion.SCREEN_WIDTH, int(configuracion.SCREEN_HEIGHT/2) - 118, 1)
columnas_group.add(bottom_column)
columnas_group.add(top_column)
ultima_columna = pygame.time.get_ticks()

# Entorno
suelo = PlataformaMovil("suelo.png", configuracion.SCREEN_HEIGHT)
techo = PlataformaMovil("techo.jpeg", 0, es_techo=True)

# Fondo (con protección por si falla)
try:
    bg = pygame.image.load('imagenes/fondo.png').convert()
    bg = pygame.transform.scale(bg, (configuracion.SCREEN_WIDTH, configuracion.SCREEN_HEIGHT))
except:
    bg = pygame.Surface((configuracion.SCREEN_WIDTH, configuracion.SCREEN_HEIGHT))
    bg.fill((135, 206, 235))


# Bucle del juego
run = True
while run:
        clock.tick(configuracion.FPS) 
        screen.blit(bg, (0, 0))

        # --- DIBUJAR ---
        # Jugador
        icarus_group.draw(screen)

        # Columnas
        columnas_group.draw(screen)

        # Entorno
        suelo.draw(screen)
        techo.draw(screen)

        # --- COMPORTAMIENTO ---
        # In Game
        if flying and game_over == False:
            icarus_group.update()
            columnas_group.update()
            suelo.update()
            techo.update()

            # Generar nuevas columnas
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - ultima_columna > configuracion.FRECUENCIA_COLUMNAS:
                #column_height = random.randint(-100, 100)
                column_height = 0
                bottom_column = Columnas(configuracion.SCREEN_WIDTH, int(configuracion.SCREEN_HEIGHT/2) + 118 + column_height, -1)
                top_column = Columnas(configuracion.SCREEN_WIDTH, int(configuracion.SCREEN_HEIGHT/2) - 118 + column_height, 1)
                columnas_group.add(bottom_column)
                columnas_group.add(top_column)
                ultima_columna = pygame.time.get_ticks()
    
        # Game Over
        if icarus.rect.bottom >= (configuracion.SCREEN_HEIGHT - configuracion.ENV_HEIGHT) or icarus.rect.top <= configuracion.ENV_HEIGHT:
            game_over = True
        

        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if (event.type == pygame.MOUSEBUTTONDOWN or 
                (event.type == pygame.KEYDOWN and 
                 event.key == pygame.K_SPACE)) and flying == False and game_over == False:
                flying = True

        pygame.display.update()

pygame.quit()