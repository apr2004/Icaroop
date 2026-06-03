import pygame
import configuracion

class PlataformaMovil(pygame.sprite.Sprite):
    def __init__(self, imagen_nombre, y_pos, es_techo=False):
        pygame.sprite.Sprite.__init__(self)
        
        # Cargar imagen
        ruta = f"{configuracion.IMAGE_PATH}{imagen_nombre}"
        img_original = pygame.image.load(ruta).convert_alpha()
        
        # Lógica de escalado (conservando tu lógica original)
        scale_factor = configuracion.ENV_HEIGHT / img_original.get_height()
        ancho_nuevo = int(img_original.get_width() * scale_factor)
        
        self.image = pygame.transform.scale(img_original, (ancho_nuevo, configuracion.ENV_HEIGHT))
        self.rect = self.image.get_rect()
        
        # Posición inicial
        if es_techo:
            self.rect.topleft = (0, 0)
        else:
            self.rect.bottomleft = (0, configuracion.SCREEN_HEIGHT)
            
        # Para controlar el scroll interno
        self.width = ancho_nuevo
        self.x_pos = 0 

    def update(self):
        # Mover la posición X
        self.x_pos -= configuracion.SCROLL_SPEED
        
        # Reset del scroll infinito
        if self.x_pos <= -self.width:
            self.x_pos = 0

    def draw(self, screen):
        # Dibujamos la imagen dos veces para el efecto infinito
        screen.blit(self.image, (self.x_pos, self.rect.y))
        screen.blit(self.image, (self.x_pos + self.width, self.rect.y))