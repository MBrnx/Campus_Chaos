import pygame
import random
from settings import SCREEN_HEIGHT  

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        super().__init__()
        self.image = pygame.image.load('images/Capture_d_écran_2024-11-05_à_16.06.34-removebg-preview.png') 
        self.image = pygame.transform.scale(self.image, (50, 50))  
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width) 
        self.rect.y = -self.rect.height  
        
        self.speed = random.randint(7, 25)  

    def update(self):
        
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT: 
            self.kill()

