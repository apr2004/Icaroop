"""
GameState groups together everything that used to be loose global
variables in flappy_icarus.py: flying, game_over, score, inside_column,
speed_increment and last_column.

Keeping them in one object makes it obvious what "the state of a run"
actually is, and turns reset_game() into a single state.reset() call
instead of a function full of global statements.
"""
import pygame
import config

class GameState:
    def __init__(self, icarus, columns_group):
        self.icarus = icarus
        self.columns_group = columns_group
        self.reset()

    def reset(self):
        self.flying = False
        self.game_over = False
        self.score = 0
        self.inside_column = False
        self.speed_increment = 0
        self.last_column_time = pygame.time.get_ticks()

        self.icarus.rect.center = (config.ICARUS_START_X, config.ICARUS_START_Y)
        self.icarus.velocity = 0
        self.icarus.clicked = False

        self.columns_group.empty()

    def start_flying(self):
        self.flying = True
        # Reset the spawn timer here too: otherwise, if the player waits on
        # the "PLAY" screen longer than COLUMN_FREQUENCY, the very first
        # flying frame thinks a new column is "overdue" and spawns a second
        # pair on top of the one already sitting at the right edge.
        self.last_column_time = pygame.time.get_ticks()

    def end_game(self):
        self.game_over = True

    def register_column_spawn(self, current_time):
        self.last_column_time = current_time

    def time_for_new_column(self, current_time):
        return current_time - self.last_column_time > config.COLUMN_FREQUENCY

    def update_score(self):
        columns = self.columns_group
        if len(columns) == 0:
            return

        first_column = columns.sprites()[0]

        if (self.icarus.rect.right > first_column.rect.left
                and self.icarus.rect.left < first_column.rect.right
                and not self.inside_column):
            self.inside_column = True

        if self.inside_column and self.icarus.rect.left > first_column.rect.right:
            self.score += config.SCORE_INCREMENT
            self.speed_increment += config.SPEED_INCREMENT_STEP
            self.inside_column = False