import pygame
import config

# --- Columns Class ---
class Columns(pygame.sprite.Sprite):
        def __init__(self, x, y, position):
                pygame.sprite.Sprite.__init__(self)
                column = pygame.image.load(f"{config.IMAGE_PATH}columna.png").convert_alpha()

                new_height = int(column.get_height() * config.COLUMN_SCALE)
                new_width = int(column.get_width() * config.COLUMN_SCALE)
                self.image = pygame.transform.scale(column, (new_width, new_height))
                self.rect = self.image.get_rect()
                
                # position 1 is upper column, -1 lower column
                if position == 1:
                        self.image = pygame.transform.flip(self.image, False, True)                
                        self.rect.bottomleft = [x, y]
                if position == -1:
                        self.rect.topleft = [x, y]

                # Mask for precise collisions
                self.mask = pygame.mask.from_surface(self.image)

        def update(self):
                self.rect.x -= config.SCROLL_SPEED
                if self.rect.right < 0:
                        self.kill()
