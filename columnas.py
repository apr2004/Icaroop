import pygame
import configuracion

# --- Clase Columnas ---
class Columnas(pygame.sprite.Sprite):
        def __init__(self, x, y, position):
                pygame.sprite.Sprite.__init__(self)
                columna = pygame.image.load(f"{configuracion.IMAGE_PATH}columna.png").convert_alpha()

                new_height = int(columna.get_height() * configuracion.ESCALA_COLUMNAS)
                new_width = int(columna.get_width() * configuracion.ESCALA_COLUMNAS)
                self.image = pygame.transform.scale(columna, (new_width, new_height))
                self.rect = self.image.get_rect()
                
                # position 1 es columna superior, -1 columna inferior
                if position == 1:
                        self.image = pygame.transform.flip(self.image, False, True)                
                        self.rect.bottomleft = [x, y]
                if position == -1:
                        self.rect.topleft = [x, y]

                # Máscara para colisiones precisas
                self.mask = pygame.mask.from_surface(self.image)

        def update(self):
                self.rect.x -= configuracion.SCROLL_SPEED
                if self.rect.right < 0:
                        self.kill()