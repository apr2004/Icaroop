import pygame
from pygame.locals import *
import random
import config
from icarus import Icarus
from environment import MovingPlatform
from columns import Columns
from base_column import ColumnBase
from column_body import ColumnBody


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption('Icaroop')

flying = config.FLYING
game_over = config.GAME_OVER

# Load the letter typography
score_font = pygame.font.Font(f'{config.FONT_PATH}Icarop.ttf', config.SCORE_FONT_SIZE)
title_font = pygame.font.Font(f'{config.FONT_PATH}Icarop.ttf', config.TITTLE_FONT_SIZE)

# Groups and objects
# Icarus
icarus_group = pygame.sprite.Group()
icarus = Icarus(100, int(config.SCREEN_HEIGHT/2))
icarus_group.add(icarus)

# Columns (with old method)
columns_group = pygame.sprite.Group()
bottom_column = Columns(-config.SCREEN_WIDTH, int(config.SCREEN_HEIGHT/2) + 118, -1)
top_column = Columns(-config.SCREEN_WIDTH, int(config.SCREEN_HEIGHT/2) - 118, 1)
columns_group.add(bottom_column)
columns_group.add(top_column)
last_column = pygame.time.get_ticks()

# Environment
ground = MovingPlatform("suelo.png", config.SCREEN_HEIGHT)
ceiling = MovingPlatform("techo.jpeg", 0, is_ceiling=True)

# FUNCTIONS
def draw_text(text, font, color, x, y, screen):
    # Convert the text into an image
    # The 'True' is for "Antialiasing" (smooths the edges of the letters)
    text_image = font.render(text, True, color)
    
    # Position the same way as with Icarus
    text_rect = text_image.get_rect(center=(x, y))
    
    # Draw on screen
    screen.blit(text_image, text_rect)

# Background (with protection in case of failure)
try:
    bg = pygame.image.load(f'{config.IMAGE_PATH}fondo.png').convert()
    bg = pygame.transform.scale(bg, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
except:
    bg = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    bg.fill((135, 206, 235))


# Game loop
score = 0
run = True
while run:
        clock.tick(config.FPS) 
        screen.blit(bg, (0, 0))

        # --- DRAW ---
        if(not flying and not game_over):
            draw_text('PLAY', title_font, config.ORANGE, config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2 - 50, screen)

        # Player
        icarus_group.draw(screen)

        # Columns
        columns_group.draw(screen)

        # Environment
        ground.draw(screen)
        ceiling.draw(screen)

        # --- BEHAVIOR ---
        # In Game
        if flying and game_over == False:
            icarus_group.update()
            columns_group.update()
            ground.update()
            ceiling.update()

            # Generate new columns
            current_time = pygame.time.get_ticks()
            if current_time - last_column > config.COLUMN_FREQUENCY:
                column_height = random.randint(-100, 100)
                
                # Define gap coordinates
                y_gap_bottom = int(config.SCREEN_HEIGHT/2) + 118 + column_height
                y_gap_top = int(config.SCREEN_HEIGHT/2) - 118 + column_height
                
                # --- BOTTOM COLUMN  ---
                # Base
                base_bottom = ColumnBase(config.SCREEN_WIDTH + 6, -1)
                columns_group.add(base_bottom)
                
                # Calculate height for the body
                # The base is at (SCREEN_HEIGHT - ENV_HEIGHT), so we subtract its own height
                available_height_bottom = base_bottom.rect.top - y_gap_bottom
                
                # Create the rest of the column
                body_bottom = ColumnBody(config.SCREEN_WIDTH, y_gap_bottom, -1, available_height_bottom)
                columns_group.add(body_bottom)


                # --- TOP COLUMN ---
                # REPEAT THE STEPS OF THE BOTTOM COLUMN
                # Create the Base
                base_top = ColumnBase(config.SCREEN_WIDTH + 6, 1)
                columns_group.add(base_top)

                # Calculate height for the body
                available_height_top = y_gap_top - base_top.rect.bottom

                # Create the rest of the column
                body_top = ColumnBody(config.SCREEN_WIDTH, y_gap_top, 1, available_height_top)
                columns_group.add(body_top)

                last_column = pygame.time.get_ticks()
    
        # Game Over
        if icarus.rect.bottom >= (config.SCREEN_HEIGHT - config.ENV_HEIGHT) or icarus.rect.top <= config.ENV_HEIGHT:
            game_over = True
            draw_text('GAME OVER', title_font, config.ORANGE, config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2 - 50, screen)
        if pygame.sprite.groupcollide(icarus_group, columns_group, False, False, pygame.sprite.collide_mask):
            game_over = True
            draw_text('GAME OVER', title_font, config.ORANGE, config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2 - 50, screen)
        

        # --- EVENTS ---
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
                # Restart the game
                flying = False
                game_over = False

                # Restart Icarus position
                icarus.rect.center = (100, int(config.SCREEN_HEIGHT/2))
                icarus.velocity = 0

                # Clear columns
                columns_group.empty()
                
                # Restart column generation time
                last_column = pygame.time.get_ticks()

        draw_text("score: " + str(score), score_font, config.ORANGE, config.SCREEN_WIDTH // 2, 50, screen)
        pygame.display.update()

pygame.quit()
