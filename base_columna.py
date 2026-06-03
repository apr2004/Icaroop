import pygame
import configuracion

class ColumnaBase(pygame.sprite.Sprite):
    def __init__(self, x, position):
        pygame.sprite.Sprite.__init__(self)

        # Cargar y escalar
        base = pygame.image.load(f"{configuracion.IMAGE_PATH}base.png").convert_alpha()
        self.height = int(base.get_height() * configuracion.ESCALA_COLUMNAS)
        self.width = int(base.get_width() * configuracion.ESCALA_COLUMNAS)
        
        base_escalada = pygame.transform.scale(base, (self.width, self.height))

        # Crear lienzo (del tamaño exacto de la base)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        # Pintamos en (0,0) porque el lienzo es del tamaño justo de la imagen
        self.image.blit(base_escalada, (0, 0))

        # POSICIONAMIENTO AUTOMÁTICO
        if position == 1: 
            # Columna Superior: La base va pegada al techo (debajo del borde del entorno)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.topleft = [x, configuracion.ENV_HEIGHT]
        else:
            # Columna Inferior: La base va pegada al suelo
            self.rect.bottomleft = [x, configuracion.SCREEN_HEIGHT - configuracion.ENV_HEIGHT]

        # Máscara para colisiones precisas
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= configuracion.SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()