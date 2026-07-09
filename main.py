import asyncio
import pygame
from pygame.locals import *
import random

import config
from assets import Assets
from icarus import Icarus
from environment import MovingPlatform
from base_column import ColumnBase
from column_body import ColumnBody
from game_state import GameState

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption('Icaroop')

# Load every image ONCE at start-up
assets = Assets()

# Load the letter typography
score_font = pygame.font.Font(f'{config.FONT_PATH}Icarop.ttf', config.SCORE_FONT_SIZE)
title_font = pygame.font.Font(f'{config.FONT_PATH}Icarop.ttf', config.TITTLE_FONT_SIZE)

# Groups and objects
# Icarus
icarus_group = pygame.sprite.Group()
icarus = Icarus(config.ICARUS_START_X, config.ICARUS_START_Y, assets.icarus_frames)
icarus_group.add(icarus)

# Columns
columns_group = pygame.sprite.Group()

# Environment
ground = MovingPlatform(assets.ground_image, config.SCREEN_HEIGHT)
ceiling = MovingPlatform(assets.ceiling_image, 0, is_ceiling=True)

# Centralized state (replaces the old flying/game_over/score/... globals)
state = GameState(icarus, columns_group)


# FUNCTIONS
def draw_text(text, font, color, x, y, screen):
    # Convert the text into an image
    # The 'True' is for "Antialiasing" (smooths the edges of the letters)
    text_image = font.render(text, True, color)

    # Position the same way as with Icarus
    text_rect = text_image.get_rect(center=(x, y))

    # Draw on screen
    screen.blit(text_image, text_rect)


def spawn_column_pair(assets, columns_group):
    """Creates a new top+bottom column (base + body) pair at the right edge."""
    height_variation = random.randint(
        -config.COLUMN_HEIGHT_VARIATION, config.COLUMN_HEIGHT_VARIATION
    )

    y_gap_bottom = config.SCREEN_HEIGHT // 2 + config.COLUMN_GAP_HALF + height_variation
    y_gap_top = config.SCREEN_HEIGHT // 2 - config.COLUMN_GAP_HALF + height_variation

    # --- BOTTOM COLUMN ---
    base_bottom = ColumnBase(assets.column_base, config.SCREEN_WIDTH + 6, -1)
    columns_group.add(base_bottom)

    available_height_bottom = base_bottom.rect.top - y_gap_bottom
    body_bottom = ColumnBody(
        assets.column_shaft, assets.column_head,
        config.SCREEN_WIDTH, y_gap_bottom, -1, available_height_bottom
    )
    columns_group.add(body_bottom)

    # --- TOP COLUMN ---
    base_top = ColumnBase(assets.column_base, config.SCREEN_WIDTH + 6, 1)
    columns_group.add(base_top)

    available_height_top = y_gap_top - base_top.rect.bottom
    body_top = ColumnBody(
        assets.column_shaft, assets.column_head,
        config.SCREEN_WIDTH, y_gap_top, 1, available_height_top
    )
    columns_group.add(body_top)


# Spawn the very first column pair using the SAME system as every
# subsequent one
spawn_column_pair(assets, columns_group)

async def main():
    run = True
    while run:
        clock.tick(config.FPS)
        screen.blit(assets.background, (0, 0))

        # --- DRAW ---
        if not state.flying and not state.game_over:
            draw_text('PLAY', title_font, config.ORANGE, config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 - 50, screen)

        # Player
        if state.flying or state.game_over:
            icarus_group.draw(screen)

        # Columns
        columns_group.draw(screen)

        # Environment
        ground.draw(screen)
        ceiling.draw(screen)

        # --- BEHAVIOR ---
        # In Game
        if state.flying and not state.game_over:
            icarus_group.update()
            columns_group.update(state.speed_increment)
            ground.update(state.speed_increment)
            ceiling.update(state.speed_increment)
            state.update_score()

            # Generate new columns
            current_time = pygame.time.get_ticks()
            if state.time_for_new_column(current_time):
                spawn_column_pair(assets, columns_group)
                state.register_column_spawn(current_time)

        # Game Over
        if icarus.rect.bottom >= (config.SCREEN_HEIGHT - config.ENV_HEIGHT) or icarus.rect.top <= config.ENV_HEIGHT:
            state.end_game()
        if pygame.sprite.groupcollide(icarus_group, columns_group, False, False, pygame.sprite.collide_mask):
            state.end_game()

        if state.game_over:
            draw_text('GAME OVER', title_font, config.ORANGE, config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 - 50, screen)

        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if (event.type == pygame.MOUSEBUTTONDOWN or
                    (event.type == pygame.KEYDOWN and
                     event.key == pygame.K_SPACE)) and not state.flying and not state.game_over:
                state.start_flying()
            if state.game_over and (event.type == pygame.MOUSEBUTTONDOWN or
                                     (event.type == pygame.KEYDOWN and
                                      event.key == pygame.K_SPACE)):
                state.reset()
                spawn_column_pair(assets, columns_group)

        draw_text("SCORE " + str(state.score), score_font, config.ORANGE, 100, 90, screen)
        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())