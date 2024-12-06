import pygame

class Platforme(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load('image/platforme.png').subsurface((1, 322, 490, 89))
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))  # Ajuster la taille de l'image

    def afficher(self, surface):
        
        surface.blit(self.image, (self.rect.x, self.rect.y))
