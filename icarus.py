import pygame
import configuracion

# --- Clase Jugador (Ícaro) ---
class Icarus(pygame.sprite.Sprite):
     def __init__(self, x, y):
          pygame.sprite.Sprite.__init__(self)
          self.images = []
          self.index = 0
          
          self.counter = 0
          for num in range(1,4):
            img = pygame.image.load(f'{configuracion.IMAGE_PATH}icarus{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (configuracion.ICARUS_WIDTH, configuracion.ICARUS_HEIGHT))
            self.images.append(img)
          self.image = self.images[self.index]
          
          #self.image = pygame.image.load(f'{configuracion.IMAGE_PATH}icarus.jpeg').convert_alpha()
          self.rect = self.image.get_rect()
          self.rect.center = [x, y]
          self.vel = 0
          self.clicked = False

     def update(self):
          # Aplicar gravedad
          self.vel += configuracion.GRAVITY

          # Limitamos la velocidad máxima de caída
          if(self.vel > configuracion.LIMIT_VELOCITY):
               self.vel = configuracion.LIMIT_VELOCITY

          # Limites de los bordes
          if self.rect.bottom < (configuracion.SCREEN_HEIGHT - configuracion.ENV_HEIGHT):
               self.rect.y += int(self.vel)

          if self.rect.top < (configuracion.ENV_HEIGHT):
               self.vel = 0
               

          # Salto con ratón y/o tecclado
          '''
          get_pressed devuelve un array con el estado de todos los botones del ratón
          El índice 0 es el botón izquierdo
          '''
          if (pygame.mouse.get_pressed()[0] == 1 or pygame.key.get_pressed()[pygame.K_SPACE] == 1) and self.clicked == False:
               self.clicked = True
               self.vel = configuracion.JUMP

          # Para evitar múltiples saltos con una sola pulsación
          if pygame.mouse.get_pressed()[0] == 0 and pygame.key.get_pressed()[pygame.K_SPACE] == 0:
               self.clicked = False


          # Manejo de la animación
          self.counter += 1

          if self.counter > configuracion.FLAP_COOLDOWN:
               self.counter = 0
               self.index += 1
               if self.index >= len(self.images):
                    self.index = 0
          self.image = self.images[self.index]
          

          # rotación de la imagen
          self.image = pygame.transform.rotate(self.images[self.index], self.vel*configuracion.ROTATION_ANGLE) # cambiar 0 por self.index para animación
          # Actualizar máscara para colisiones precisas tras la rotación/animación
          self.mask = pygame.mask.from_surface(self.image)