import pygame
import config

class ColumnBody(pygame.sprite.Sprite):
    def __init__(self, x, y, position, available_height):
        pygame.sprite.Sprite.__init__(self)

        shaft = pygame.image.load(f"{config.IMAGE_PATH}fuste.png").convert_alpha()
        head = pygame.image.load(f"{config.IMAGE_PATH}cabeza.png").convert_alpha()

        # Calculate necessary heights and widths
        head_height = int(head.get_height() * config.COLUMN_SCALE)
        
        # The shaft fills the remaining space (Total - Head)
        shaft_height = available_height - head_height
        
        # Safety: If the gap is too small, shaft is 0
        if shaft_height < 0: shaft_height = 0

        # Calculate widths
        head_width = int(head.get_width() * config.COLUMN_SCALE)
        shaft_width = int(shaft.get_width() * config.COLUMN_SCALE)

        # Scale
        scaled_shaft = pygame.transform.scale(shaft, (shaft_width, shaft_height))
        scaled_head = pygame.transform.scale(head, (head_width, head_height))

        # 4. Centering and Canvas
        max_width = max(head_width, shaft_width)
        x_head = (max_width - head_width) // 2
        x_shaft = (max_width - shaft_width) // 2

        self.image = pygame.Surface((max_width, available_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        # 5. Draw (We always build "standing": Head up, shaft down)
        self.image.blit(scaled_head, (x_head, 0))
        self.image.blit(scaled_shaft, (x_shaft, head_height))

        # 6. Position relative to the GAP (y)
        if position == 1:
            # Upper Column: Comes from the ceiling and its BOTTOM edge is the gap
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y] 
        else:
            # Lower Column: Comes from the ground and its TOP edge is the gap
            self.rect.topleft = [x, y]

        # Mask for precise collisions (adjusted to the drawing, not the canvas)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= config.SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()
