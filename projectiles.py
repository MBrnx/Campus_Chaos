import pygame

class Projectile(pygame.sprite.Sprite):

    def __init__(self, x, y, taille, direction, image):

        super().__init__()
        self.x = x
        self.y = y 
        self.taille = taille
        self.direction = direction
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.taille[0], self.taille[1])
                                
    def afficher(self, surface, delta_temps):

        if delta_temps > 2:
            self.image = pygame.transform.scale(self.image, (50, 30))

        surface.blit(self.image, self.rect)

    def mouvement(self, vitesse):

        self.rect.x +=( vitesse * self.direction)