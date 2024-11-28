import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 20))  # Taille du projectile
        self.image.fill((255, 0, 0))  # Couleur du projectile (rouge)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 5  # Vitesse du projectile
        self.direction = direction  # La direction du projectile (1 pour droite, -1 pour gauche)

    def update(self):
        """Met à jour la position du projectile en fonction de sa direction."""
        self.rect.x += self.speed * self.direction  # Déplace le projectile en fonction de la direction

        # Si le projectile dépasse la largeur de l'écran, il est supprimé
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width():
            self.kill()
