import pygame
import config

class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, image_name, y_position, is_ceiling=False):
        pygame.sprite.Sprite.__init__(self)
        
        # Load image
        path = f"{config.IMAGE_PATH}{image_name}"
        original_img = pygame.image.load(path).convert_alpha()
        
        # Scaling logic (preserving your original logic)
        scale_factor = config.ENV_HEIGHT / original_img.get_height()
        new_width = int(original_img.get_width() * scale_factor)
        
        self.image = pygame.transform.scale(original_img, (new_width, config.ENV_HEIGHT))
        self.rect = self.image.get_rect()
        
        # Initial position
        if is_ceiling:
            self.rect.topleft = (0, 0)
        else:
            self.rect.bottomleft = (0, config.SCREEN_HEIGHT)
            
        # To control internal scroll
        self.width = new_width
        self.x_position = 0 

    def update(self):
        # Move X position
        self.x_position -= config.SCROLL_SPEED
        
        # Reset infinite scroll
        if self.x_position <= -self.width:
            self.x_position = 0

    def draw(self, screen):
        # Draw the image twice for the infinite effect
        screen.blit(self.image, (self.x_position, self.rect.y))
        screen.blit(self.image, (self.x_position + self.width, self.rect.y))
