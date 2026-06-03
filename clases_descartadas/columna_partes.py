import pygame
import configuracion

# --- Clase Columnas ---
class Columnas(pygame.sprite.Sprite):
        def __init__(self, x, y, position):
                pygame.sprite.Sprite.__init__(self)

                base = pygame.image.load(f"{configuracion.IMAGE_PATH}base.png").convert_alpha()
                fuste = pygame.image.load(f"{configuracion.IMAGE_PATH}fuste.png").convert_alpha()
                cabeza = pygame.image.load(f"{configuracion.IMAGE_PATH}cabeza.png").convert_alpha()

                columna = pygame.image.load(f"{configuracion.IMAGE_PATH}columna.png").convert_alpha()
                new_height = int(columna.get_height() * configuracion.ESCALA_COLUMNAS)

                height_base = int(base.get_height() * configuracion.ESCALA_COLUMNAS)
                width_base = int(base.get_width() * configuracion.ESCALA_COLUMNAS)

                height_cabeza = int(cabeza.get_height() * configuracion.ESCALA_COLUMNAS)
                width_cabeza = int(cabeza.get_width() * configuracion.ESCALA_COLUMNAS)

                height_fuste = int(new_height - height_base - height_cabeza)
                width_fuste = int(fuste.get_width() * configuracion.ESCALA_COLUMNAS)
                
                base_escalada = pygame.transform.scale(base, (width_base, height_base))
                fuste_escalado = pygame.transform.scale(fuste, (width_fuste, height_fuste))
                cabeza_escalada = pygame.transform.scale(cabeza, (width_cabeza, height_cabeza))

                # Buscamos cuál es la parte más ancha para que sea el ancho del lienzo
                max_width = max(width_base, width_cabeza, width_fuste)

                # Calculamos la posición X para centrar cada pieza usando tu fórmula
                # Usamos // para división entera (los píxeles no tienen decimales)
                x_base = (max_width - width_base) // 2
                x_cabeza = (max_width - width_cabeza) // 2
                x_fuste = (max_width - width_fuste) // 2

                self.image = pygame.Surface((max_width, new_height), pygame.SRCALPHA)
                self.rect = self.image.get_rect()

                # Dibujar siempre la columna "de pie"
                # Cabeza arriba del todo (Y=0)
                self.image.blit(cabeza_escalada, (x_cabeza, 0))

                # Fuste justo debajo de la cabeza
                self.image.blit(fuste_escalado, (x_fuste, height_cabeza))

                # Base justo debajo del fuste
                self.image.blit(base_escalada, (x_base, height_cabeza + height_fuste))

                # Si es la del techo, le damos la vuelta
                if position == 1:
                        self.image = pygame.transform.flip(self.image, False, True)
                        self.rect.bottomleft = [x, y] 
                else:
                        self.rect.topleft = [x, y]
                        

        def update(self):
                self.rect.x -= configuracion.SCROLL_SPEED
                if self.rect.right < 0:
                        self.kill()