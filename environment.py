import pygame
import config

class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, image, y_position, is_ceiling=False):
        pygame.sprite.Sprite.__init__(self)

        # image now comes pre-loaded and pre-scaled from assets.Assets,
        # instead of being loaded from disk here
        self.image = image
        self.rect = self.image.get_rect()

        # Initial position
        if is_ceiling:
            self.rect.topleft = (0, 0)
        else:
            self.rect.bottomleft = (0, config.SCREEN_HEIGHT)

        # To control internal scroll
        self.width = self.image.get_width()
        self.x_position = 0

    def update(self, speed_increment):
        # Move X position
        self.x_position -= config.INITIAL_SCROLL_SPEED + speed_increment

        # Reset infinite scroll
        if self.x_position <= -self.width:
            self.x_position = 0

    def draw(self, screen):
        # Draw the image twice for the infinite effect
        screen.blit(self.image, (self.x_position, self.rect.y))
        screen.blit(self.image, (self.x_position + self.width, self.rect.y))