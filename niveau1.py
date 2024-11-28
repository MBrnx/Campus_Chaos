import pygame 

# Code correspondant un niveau 1 du jeu 
def niveau1(surface, score):
    score = 0
    ball_pos = [240, 400]
    ball_speed = [0, 0]
    previous_pos = ball_pos[0]
    distance_parcourue = 0
    jeu_en_cours = True
    screen_width = surface.get_width()
    screen_height = surface.get_height()

    # Initialiser le timer
    start_time = pygame.time.get_ticks()

    while jeu_en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, 0  # Retourne aussi l'XP gagnée
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return score, 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ball_speed[0] = -5
        elif keys[pygame.K_RIGHT]:
            ball_speed[0] = 5
        else:
            ball_speed[0] = 0

        if keys[pygame.K_UP]:
            ball_speed[1] = -5
        elif keys[pygame.K_DOWN]:
            ball_speed[1] = 5
        else:
            ball_speed[1] = 0

        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        if ball_pos[0] < 0:
            ball_pos[0] = 0
        elif ball_pos[0] > screen_width - 30:
            ball_pos[0] = screen_width - 30

        if ball_pos[1] < 0:
            ball_pos[1] = 0
        elif ball_pos[1] > screen_height - 30:
            ball_pos[1] = screen_height - 30

        distance_parcourue += abs(ball_pos[0] - previous_pos)
        previous_pos = ball_pos[0]

        if distance_parcourue >= 20:
            score += 1
            distance_parcourue = 0

        surface.fill((0, 0, 0))
        pygame.draw.circle(surface, (255, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), 30)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        surface.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.delay(30)

    # Calculer l'XP basée sur le temps passé
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # En secondes
    xp_gagnee = int(elapsed_time * 10)  # 10 XP par seconde

    return score, xp_gagnee