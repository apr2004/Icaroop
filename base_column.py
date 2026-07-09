import pygame
import config

class ColumnBase(pygame.sprite.Sprite):
    def __init__(self, base_image, x, position):
        pygame.sprite.Sprite.__init__(self)

        # base_image comes pre-loaded and pre-scaled from assets.Assets, so
        # there's no more per-instance pygame.image.load()/transform.scale()

        # AUTOMATIC POSITIONING
        if position == 1:
            # Upper Column: The base goes attached to the ceiling (below the environment edge)
            self.image = pygame.transform.flip(base_image, False, True)
            self.rect = self.image.get_rect()
            self.rect.topleft = [x, config.ENV_HEIGHT]
        else:
            # Lower Column: The base goes attached to the ground
            self.image = base_image
            self.rect = self.image.get_rect()
            self.rect.bottomleft = [x, config.SCREEN_HEIGHT - config.ENV_HEIGHT]

        # Mask for precise collisions
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, speed_increment):
        self.rect.x -= config.INITIAL_SCROLL_SPEED + speed_increment
        if self.rect.right < 0:
            self.kill()