import pygame
import random

# Code correspondant au niveau 3 du jeu 
def niveau3(surface):
    score = 0 
    drawing = False
    circles = []
    jeu_en_cours = True
    clock = pygame.time.Clock()
    
    while jeu_en_cours:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drawing = True
                pos = event.pos
                circles.append(pos)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drawing = False

        surface.fill((255, 255, 255))
        for pos in circles:
            pygame.draw.circle(surface, (0, 0, 255), pos, 15)

        pygame.display.flip()

    return True