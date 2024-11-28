import pygame
import time
from player import Player
from enemy import Enemy
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS

# Initialisation de Pygame
pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('images/BDD Niv_ax fond_audio.MP3') 
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(-1) 

# Paramètres de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chaos Campus")

# Charger l'icône du jeu
icon = pygame.image.load('images/Capture_d_écran_2024-11-05_à_16.06.34-removebg-preview.png')
pygame.display.set_icon(icon)

# Chronomètre de 120 secondes
start_time = time.time()  # Moment où le jeu commence
change_interval = 10  # Changer le fond toutes les 10 secondes
total_time = 121  # 120 secondes au total

# Liste des 12 images de fond
backgrounds = [
    'images/a-0.JPEG',
    'images/a-1.JPEG',
    'images/a-2.JPEG',
    'images/a-3.JPEG',
    'images/a-4.JPEG',
    'images/a-5.JPEG',
    'images/a-6.JPEG',
    'images/a-7.JPEG',
    'images/a-8.JPEG',
    'images/a-9.JPEG',
    'images/a-10.JPEG',
    'images/a-11.JPEG',
    'images/a-12.JPEG',
]

background_index = 0
background = pygame.image.load(backgrounds[background_index])
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialiser l'horloge
clock = pygame.time.Clock()

def change_background(new_background_path):
    """Change le fond pendant le jeu."""
    new_background = pygame.image.load(new_background_path)
    new_background = pygame.transform.scale(new_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return new_background

def init_player():
    """Initialise le joueur et le place correctement."""
    player = Player()
    background_height = background.get_height()
    player_height = player.image.get_height()
    trottoir_y_position = background_height - 55  # Ajustez cette valeur si nécessaire
    player.rect.y = trottoir_y_position - player_height
    return player

def display_end_screen():
    """Affiche l'écran de fin et gère les interactions."""
    font = pygame.font.Font(None, 74)
    running = True
    while running:
        screen.fill((0, 0, 0))  # Fond noir
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        retry_text = font.render("Réessayer (R)", True, (255, 255, 255))
        quit_text = font.render("Quitter (Q)", True, (255, 255, 255))

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, 300))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Relancer
                    return "retry"
                if event.key == pygame.K_q:  # Quitter
                    running = False
                    pygame.quit()
                    return "quit"

# Boucle principale
while True:
    # Initialiser le joueur et les ennemis
    player = init_player()
    enemies = pygame.sprite.Group()
    enemy_timer = 0
    can_spawn_enemies = True

    # Boucle de jeu
    running = True
    while running:
        screen.blit(background, (0, 0))

        # Vérifier combien de temps s'est écoulé
        elapsed_time = time.time() - start_time
        remaining_time = total_time - elapsed_time

        # Si le temps écoulé dépasse 120 secondes, arrêter les ennemis
        if remaining_time <= 0:
            can_spawn_enemies = False


        if elapsed_time >= 121:
            player.health = 100  
            start_time = time.time()

        # Change le fond toutes les 10 secondes
        if int(elapsed_time) % change_interval == 0 and elapsed_time < total_time:
            new_background_path = backgrounds[(int(elapsed_time) // change_interval) % len(backgrounds)]
            if new_background_path != backgrounds[background_index]:  # Si le fond change
                background = change_background(new_background_path)
                background_index = backgrounds.index(new_background_path)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                running = False
                pygame.quit()
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player.move('right', SCREEN_WIDTH)
        if keys[pygame.K_q]:
            player.move('left', SCREEN_WIDTH)

        enemy_timer += 1
        if enemy_timer > 60 and can_spawn_enemies:
            enemies.add(Enemy(SCREEN_WIDTH))
            enemy_timer = 0

        enemies.update()
        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect)

        for enemy in pygame.sprite.spritecollide(player, enemies, True):
            print("Collision avec un ennemi détectée !")
            player.health -= 10

        if player.health <= 0:
            print("Le joueur n'a plus de vie. Fin du jeu.")
            running = False

        player.update()
        screen.blit(player.image, player.rect)
        player.draw_health_bar(screen)

        pygame.display.flip()
        clock.tick(FPS)  # Limiter à FPS frames par seconde

    # Afficher l'écran de fin
    result = display_end_screen()
    if result == "retry":
        pygame.mixer.music.play(-1)
        start_time = time.time()  # Réinitialiser le chrono
        continue  # Relancer la boucle principale
    elif result == "quit":
        pygame.mixer.music.stop()
        break  # Quitter le jeu

    #oui