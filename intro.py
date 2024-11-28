import pygame 
from pygame.locals import *

# Permet la création de l'introduction au début du jeu, avant son lancement 
def afficher_intro(surface, start_button):
    font = pygame.font.SysFont("Arial", 48)
    surface.fill((0, 0, 0))
    start_button.draw(surface)
    pygame.display.update()

    # Attend le click sur le bouton play pour lancer le jeu 
    attendre_debut = True
    while attendre_debut:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                souris_pos = event.pos
                if start_button.is_clicked(souris_pos):
                    attendre_debut = False 

        start_button.check_hover(pygame.mouse.get_pos())
        start_button.draw(surface)
        pygame.display.update()
    return True