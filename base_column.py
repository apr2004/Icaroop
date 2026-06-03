import pygame
import config

class ColumnBase(pygame.sprite.Sprite):
    def __init__(self, x, position):
        pygame.sprite.Sprite.__init__(self)

        # Load and scale
        base_image = pygame.image.load(f"{config.IMAGE_PATH}base.png").convert_alpha()
        self.height = int(base_image.get_height() * config.COLUMN_SCALE)
        self.width = int(base_image.get_width() * config.COLUMN_SCALE)
        
        scaled_base = pygame.transform.scale(base_image, (self.width, self.height))

        # Create canvas (exact size of the base)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        # Paint at (0,0) because the canvas is the exact size of the image
        self.image.blit(scaled_base, (0, 0))

        # AUTOMATIC POSITIONING
        if position == 1: 
            # Upper Column: The base goes attached to the ceiling (below the environment edge)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.topleft = [x, config.ENV_HEIGHT]
        else:
            # Lower Column: The base goes attached to the ground
            self.rect.bottomleft = [x, config.SCREEN_HEIGHT - config.ENV_HEIGHT]

        # Mask for precise collisions
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= config.SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()
