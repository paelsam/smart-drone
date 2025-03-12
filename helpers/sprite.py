import pygame

class Sprite(pygame.sprite.Sprite):
   # Crear un sprite a partir de una imagen y el tamaño de la imagen
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
       

    # Dibujar el sprite en la ventana
    def draw(self, window):
        window.blit(self.image, self.rect)


