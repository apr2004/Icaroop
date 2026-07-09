import pygame
import config

class ColumnBody(pygame.sprite.Sprite):
    def __init__(self, shaft_image, head_image, x, y, position, available_height):
        pygame.sprite.Sprite.__init__(self)

        # shaft_image and head_image come pre-loaded from assets.Assets.
        # The shaft still needs to be re-scaled per instance because
        # available_height changes every time (it depends on the random
        # gap), but we no longer read either PNG from disk here.
        head_height = head_image.get_height()
        head_width = head_image.get_width()
        shaft_width = shaft_image.get_width()

        # The shaft fills the remaining space (Total - Head)
        shaft_height = max(0, available_height - head_height)
        scaled_shaft = pygame.transform.scale(shaft_image, (shaft_width, shaft_height))

        # Centering and Canvas
        max_width = max(head_width, shaft_width)
        x_head = (max_width - head_width) // 2
        x_shaft = (max_width - shaft_width) // 2

        self.image = pygame.Surface((max_width, available_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        # Draw (we always build "standing": head up, shaft down)
        self.image.blit(head_image, (x_head, 0))
        self.image.blit(scaled_shaft, (x_shaft, head_height))

        # Position relative to the GAP (y)
        if position == 1:
            # Upper Column: comes from the ceiling and its BOTTOM edge is the gap
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y]
        else:
            # Lower Column: comes from the ground and its TOP edge is the gap
            self.rect.topleft = [x, y]

        # Mask for precise collisions (adjusted to the drawing, not the canvas)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, speed_increment):
        self.rect.x -= config.INITIAL_SCROLL_SPEED + speed_increment
        if self.rect.right < 0:
            self.kill()