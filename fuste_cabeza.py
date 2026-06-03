import pygame
import configuracion

class ColumnaCuerpo(pygame.sprite.Sprite):
    def __init__(self, x, y, position, altura_disponible):
        pygame.sprite.Sprite.__init__(self)

        fuste = pygame.image.load(f"{configuracion.IMAGE_PATH}fuste.png").convert_alpha()
        cabeza = pygame.image.load(f"{configuracion.IMAGE_PATH}cabeza.png").convert_alpha()

        # Calculamos la alturas y anchos necesarios
        height_cabeza = int(cabeza.get_height() * configuracion.ESCALA_COLUMNAS)
        
        # El fuste rellena el espacio que sobra (Total - Cabeza)
        height_fuste = altura_disponible - height_cabeza
        
        # Seguridad: Si el hueco es muy pequeño, fuste es 0
        if height_fuste < 0: height_fuste = 0

        # Calculamos anchos
        width_cabeza = int(cabeza.get_width() * configuracion.ESCALA_COLUMNAS)
        width_fuste = int(fuste.get_width() * configuracion.ESCALA_COLUMNAS)

        # Escalamos
        fuste_escalado = pygame.transform.scale(fuste, (width_fuste, height_fuste))
        cabeza_escalada = pygame.transform.scale(cabeza, (width_cabeza, height_cabeza))

        # 4. Centrado y Lienzo
        max_width = max(width_cabeza, width_fuste)
        x_cabeza = (max_width - width_cabeza) // 2
        x_fuste = (max_width - width_fuste) // 2

        self.image = pygame.Surface((max_width, altura_disponible), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        # 5. Dibujar (Siempre construimos "de pie": Cabeza arriba, fuste abajo)
        self.image.blit(cabeza_escalada, (x_cabeza, 0))
        self.image.blit(fuste_escalado, (x_fuste, height_cabeza))

        # 6. Posicionar respecto al HUECO (y)
        if position == 1:
            # Columna Superior: Viene del techo y su borde INFERIOR es el hueco
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y] 
        else:
            # Columna Inferior: Sale del suelo y su borde SUPERIOR es el hueco
            self.rect.topleft = [x, y]

        # Máscara para colisiones precisas (ajustada al dibujo, no al lienzo)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= configuracion.SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()