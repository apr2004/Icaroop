import pygame
from pygame.locals import *
import random
import configuracion
from icarus import Icarus
from entorno import PlataformaMovil
from columnas import Columnas
from base_columna import ColumnaBase
from fuste_cabeza import ColumnaCuerpo


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((configuracion.SCREEN_WIDTH, configuracion.SCREEN_HEIGHT))
pygame.display.set_caption('Icaroop')

flying = configuracion.FLYING
game_over = configuracion.GAME_OVER

# Cargamos la tipografia de letra
score_font = pygame.font.Font(f'{configuracion.FONT_PATH}Icarop.ttf', configuracion.SCORE_FONT_SIZE)
title_font = pygame.font.Font(f'{configuracion.FONT_PATH}Icarop.ttf', configuracion.TITTLE_FONT_SIZE)

# Grupos y objetos
# ícaro
icarus_group = pygame.sprite.Group()
icarus = Icarus(100, int(configuracion.SCREEN_HEIGHT/2))
icarus_group.add(icarus)

# columnas (con método antiguo)
columnas_group = pygame.sprite.Group()
bottom_column = Columnas(-configuracion.SCREEN_WIDTH, int(configuracion.SCREEN_HEIGHT/2) + 118, -1)
top_column = Columnas(-configuracion.SCREEN_WIDTH, int(configuracion.SCREEN_HEIGHT/2) - 118, 1)
columnas_group.add(bottom_column)
columnas_group.add(top_column)
ultima_columna = pygame.time.get_ticks()

# Entorno
suelo = PlataformaMovil("suelo.png", configuracion.SCREEN_HEIGHT)
techo = PlataformaMovil("techo.jpeg", 0, es_techo=True)

# FUNCIONES
def dibujar_texto(texto, fuente, color, x, y, pantalla):
    # Convertimos el texto en imagen
    # El 'True' es para el "Antialiasing" (suaviza los bordes de las letras)
    imagen_texto = fuente.render(texto, True, color)
    
    # Posicionamos de la misma manera que con Ícaro
    rectangulo_texto = imagen_texto.get_rect(center=(x, y))
    
    # Dibujamos en pantalla
    pantalla.blit(imagen_texto, rectangulo_texto)

# Fondo (con protección por si falla)
try:
    bg = pygame.image.load(f'{configuracion.IMAGE_PATH}fondo.png').convert()
    bg = pygame.transform.scale(bg, (configuracion.SCREEN_WIDTH, configuracion.SCREEN_HEIGHT))
except:
    bg = pygame.Surface((configuracion.SCREEN_WIDTH, configuracion.SCREEN_HEIGHT))
    bg.fill((135, 206, 235))


# Bucle del juego
score = 0
run = True
while run:
        clock.tick(configuracion.FPS) 
        screen.blit(bg, (0, 0))

        # --- DIBUJAR ---
        if(not flying and not game_over):
            dibujar_texto('PLAY', title_font, configuracion.NARANJA, configuracion.SCREEN_WIDTH/2, configuracion.SCREEN_HEIGHT/2 - 50, screen)

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
                column_height = random.randint(-100, 100)
                
                # Definir coordenadas del hueco
                y_hueco_abajo = int(configuracion.SCREEN_HEIGHT/2) + 118 + column_height
                y_hueco_arriba = int(configuracion.SCREEN_HEIGHT/2) - 118 + column_height
                
                # --- COLUMNA DE ABAJO  ---
                # Base
                base_abajo = ColumnaBase(configuracion.SCREEN_WIDTH + 6, -1)
                columnas_group.add(base_abajo)
                
                # Calculamos altura para el cuerpo
                # La base está en (SCREEN_HEIGHT - ENV_HEIGHT), así que restamos su propia altura
                altura_disponible_abajo = base_abajo.rect.top - y_hueco_abajo
                
                # Creamos el resto de la columna
                cuerpo_abajo = ColumnaCuerpo(configuracion.SCREEN_WIDTH, y_hueco_abajo, -1, altura_disponible_abajo)
                columnas_group.add(cuerpo_abajo)


                # --- COLUMNA DE ARRIBA ---
                # REPETIMOS LOS PASOS DE LA COLUMNA DE ABAJO
                # Creamos la Base
                base_arriba = ColumnaBase(configuracion.SCREEN_WIDTH + 6, 1)
                columnas_group.add(base_arriba)

                # Calculamos altura para el cuerpo
                altura_disponible_arriba = y_hueco_arriba - base_arriba.rect.bottom

                # Creamos el resto de la columna
                cuerpo_arriba = ColumnaCuerpo(configuracion.SCREEN_WIDTH, y_hueco_arriba, 1, altura_disponible_arriba)
                columnas_group.add(cuerpo_arriba)

                ultima_columna = pygame.time.get_ticks()
    
        # Game Over
        if icarus.rect.bottom >= (configuracion.SCREEN_HEIGHT - configuracion.ENV_HEIGHT) or icarus.rect.top <= configuracion.ENV_HEIGHT:
            game_over = True
            dibujar_texto('GAME OVER', title_font, configuracion.NARANJA, configuracion.SCREEN_WIDTH/2, configuracion.SCREEN_HEIGHT/2 - 50, screen)
        if pygame.sprite.groupcollide(icarus_group, columnas_group, False, False, pygame.sprite.collide_mask):
            game_over = True
            dibujar_texto('GAME OVER', title_font, configuracion.NARANJA, configuracion.SCREEN_WIDTH/2, configuracion.SCREEN_HEIGHT/2 - 50, screen)
        

        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if (event.type == pygame.MOUSEBUTTONDOWN or 
                (event.type == pygame.KEYDOWN and 
                 event.key == pygame.K_SPACE)) and flying == False and game_over == False:
                flying = True
            if(game_over and (event.type == pygame.MOUSEBUTTONDOWN or 
                (event.type == pygame.KEYDOWN and 
                 event.key == pygame.K_SPACE))):
                # Reiniciar el juego
                flying = False
                game_over = False

                # Reiniciar posición de Ícaro
                icarus.rect.center = (100, int(configuracion.SCREEN_HEIGHT/2))
                icarus.velocidad = 0

                # Vaciar columnas
                columnas_group.empty()
                
                # Reiniciar tiempo de generación de columnas
                ultima_columna = pygame.time.get_ticks()

        dibujar_texto("score: " + str(score), score_font, configuracion.NARANJA, configuracion.SCREEN_WIDTH // 2, 50, screen)
        pygame.display.update()

pygame.quit()