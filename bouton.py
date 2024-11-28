import pygame 

# Création de la classe bouton, on va s'en servir pour le bouton play et les boutons des différents niveaux 
class Bouton: 
    
    # Initialisation du bouton 
    def __init__(self, image_path, center):
        self.image = pygame.image.load(image_path)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=center)
        self.hovered = False

    # Permet d'afficher l'image à l'écran 
    def draw(self, surface):
        if self.hovered:
            scaled_image = pygame.transform.scale(self.original_image, (int(self.rect.width * 1.1), int(self.rect.height * 1.1)))
            scaled_rect = scaled_image.get_rect(center=self.rect.center)
            surface.blit(scaled_image, scaled_rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.hovered and self.rect.collidepoint(pos)