import pygame
import random

# Code correspondant au niveau 2 du jeu 
def niveau2(surface, score):
    target_pos = [random.randint(50, 430), random.randint(50, 730)]
    target_radius = 30
    score = 0
    jeu_en_cours = True
    complet = False
    clock = pygame.time.Clock()
    
    while jeu_en_cours:
        clock.tick(30)
        surface.fill((255, 255, 255))
        pygame.draw.circle(surface, (0, 255, 0), target_pos, target_radius)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                souris_pos = event.pos
                if (souris_pos[0] - target_pos[0])**2 + (souris_pos[1] - target_pos[1])**2 < target_radius**2:
                    score += 1
                    target_pos = [random.randint(50, 430), random.randint(50, 730)]
                    
            if score == 5: 
                complet = True 

        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        surface.blit(score_text, (10, 10))

        pygame.display.flip()

    return score
