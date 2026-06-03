import pygame
import config

# --- Player Class (Icarus) ---
class Icarus(pygame.sprite.Sprite):
     def __init__(self, x, y):
          pygame.sprite.Sprite.__init__(self)
          self.images = []
          self.index = 0
          
          self.counter = 0
          for num in range(1,4):
            img = pygame.image.load(f'{config.IMAGE_PATH}icarus{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (config.ICARUS_WIDTH, config.ICARUS_HEIGHT))
            self.images.append(img)
          self.image = self.images[self.index]
          
          #self.image = pygame.image.load(f'{config.IMAGE_PATH}icarus.jpeg').convert_alpha()
          self.rect = self.image.get_rect()
          self.rect.center = [x, y]
          self.velocity = 0
          self.clicked = False

     def update(self):
          # Apply gravity
          self.velocity += config.GRAVITY

          # Limit maximum fall velocity
          if(self.velocity > config.LIMIT_VELOCITY):
               self.velocity = config.LIMIT_VELOCITY

          # Border limits
          if self.rect.bottom < (config.SCREEN_HEIGHT - config.ENV_HEIGHT):
               self.rect.y += int(self.velocity)

          if self.rect.top < (config.ENV_HEIGHT):
               self.velocity = 0
               

          # Jump with mouse and/or keyboard
          '''
          get_pressed returns an array with the state of all mouse buttons
          Index 0 is the left button
          '''
          if (pygame.mouse.get_pressed()[0] == 1 or pygame.key.get_pressed()[pygame.K_SPACE] == 1) and self.clicked == False:
               self.clicked = True
               self.velocity = config.JUMP

          # To avoid multiple jumps with a single press
          if pygame.mouse.get_pressed()[0] == 0 and pygame.key.get_pressed()[pygame.K_SPACE] == 0:
               self.clicked = False


          # Animation handling
          self.counter += 1

          if self.counter > config.FLAP_COOLDOWN:
               self.counter = 0
               self.index += 1
               if self.index >= len(self.images):
                    self.index = 0
          self.image = self.images[self.index]
          

          # Image rotation
          self.image = pygame.transform.rotate(self.images[self.index], self.velocity*config.ROTATION_ANGLE) # change 0 to self.index for animation
          # Update mask for precise collisions after rotation/animation
          self.mask = pygame.mask.from_surface(self.image)
