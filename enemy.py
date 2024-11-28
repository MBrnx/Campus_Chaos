import pygame
import random
from settings import SCREEN_HEIGHT  # Importer SCREEN_HEIGHT depuis settings.py

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        super().__init__()
        self.image = pygame.image.load('images/Capture_d_écran_2024-11-05_à_16.06.34-removebg-preview.png')  # Charger l'image de l'ennemi
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensionner l'image si nécessaire
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)  # Position horizontale aléatoire
        self.rect.y = -self.rect.height  # Commence hors de l'écran, au-dessus du haut

        # Vitesse de chute ajustée pour être plus lente
        self.speed = random.randint(7, 25)  # Vitesse de chute plus lente

    def update(self):
        # Déplacer l'ennemi vers le bas
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:  # Supprimer l'ennemi quand il sort de l'écran
            self.kill()

