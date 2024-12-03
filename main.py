import pygame
import time
import random
import os
from player import Player
from enemy import Enemy
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS

def niveauAxel(fen, score_initial):
    """Fonction pour exécuter le niveau 1."""
    #pygame.mixer.init()
    #pygame.mixer.music.load('images/BDD Niv_ax fond_audio.MP3') 
    #pygame.mixer.music.set_volume(0.5)  
    #pygame.mixer.music.play(0) 

    #sons_de_hit = [pygame.mixer.Sound('images/degats.MP3') for _ in range(5)]
    #index_son_hit = 0  

    #def jouer_son_de_hit():
    #    """Jouer un son de collision avec préchargement pour réduire la latence."""
    #    nonlocal index_son_hit
    #    sons_de_hit[index_son_hit].play()
    #    index_son_hit = (index_son_hit + 1) % len(sons_de_hit)
    
    image_portail = pygame.image.load(os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/Portail.png"))
    image_portail = pygame.transform.scale(image_portail, (150, 150)) 
    rect_portail = image_portail.get_rect()

    # Liste des 12 images de fond
    fondsA = [
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-0.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-1.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-2.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-3.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-4.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-5.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-6.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-7.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-8.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-9.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-10.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-11.JPEG",
        "/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images/a-12.JPEG",
    ]
    
    index_fond = 0
    fondA = pygame.image.load(fondsA[index_fond])
    fondA = pygame.transform.scale(fondA, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def changer_fond(nouveau_fond_path):
        """Changer le fond pendant le jeu."""
        nouveau_fond = pygame.image.load(nouveau_fond_path)
        nouveau_fond = pygame.transform.scale(nouveau_fond, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return nouveau_fond

    def init_joueur():
        """Initialise le joueur et le place correctement."""
        joueur = Player()
        hauteur_fond = fondA.get_height()
        hauteur_joueur = joueur.image.get_height()
        position_trottoir_y = hauteur_fond - 55  
        joueur.rect.y = position_trottoir_y - hauteur_joueur
        return joueur

    def afficher_message(message, couleur):
        """Affiche un message générique à la fin du jeu."""
        police = pygame.font.Font(None, 50)
        while True:
            fen.fill((0, 0, 0))  
            texte = police.render(message, True, couleur)
            texte_quitter = police.render("Appuyez sur Q pour quitter.", True, (255, 255, 255))
            texte_reessayer = police.render("Appuyez sur R pour réessayer.", True, (255, 255, 255))

            fen.blit(texte, (SCREEN_WIDTH // 2 - texte.get_width() // 2, 150))
            fen.blit(texte_quitter, (SCREEN_WIDTH // 2 - texte_quitter.get_width() // 2, 300))
            fen.blit(texte_reessayer, (SCREEN_WIDTH // 2 - texte_reessayer.get_width() // 2, 400))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quitter"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: 
                        return "quitter"
                    if event.key == pygame.K_r:
                        return "reessayer"

    joueur = init_joueur()
    ennemis = pygame.sprite.Group()
    timer_ennemi = 0
    peut_spawner_ennemis = True
    portail = None  
    temps_debut = time.time()
    temps_total = 121
    intervalle_changement = 10
    index_fond = 0
    score = 0
    fondA = changer_fond(fondsA[index_fond])

    en_cours = True
    victoire = False  # Indicateur de victoire ou défaite
    
    def spawn_portail():
        rect_portail.x = random.randint(0, SCREEN_WIDTH - rect_portail.width)
        rect_portail.y = SCREEN_HEIGHT - rect_portail.height - 55 
        return rect_portail

    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return score

        fen.blit(fondA, (0, 0))

        temps_ecoule = time.time() - temps_debut
        #temps_restant = temps_total - temps_ecoule

        if temps_ecoule >= temps_total:
            if portail is None:
                portail = pygame.Rect(random.randint(0, SCREEN_WIDTH - 150), SCREEN_HEIGHT - 205, 150, 150)
            peut_spawner_ennemis = False  

        if int(temps_ecoule) % intervalle_changement == 0:
            nouveau_fond_path = fondsA[(int(temps_ecoule) // intervalle_changement) % len(fondsA)]
            if nouveau_fond_path != fondsA[index_fond]:  
                fondA = changer_fond(nouveau_fond_path)
                index_fond = fondsA.index(nouveau_fond_path)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
                pygame.quit()
                return "quitter"

        touches = pygame.key.get_pressed()
        if touches[pygame.K_d]:
            joueur.move('right', SCREEN_WIDTH)
        if touches[pygame.K_q]:
            joueur.move('left', SCREEN_WIDTH)

        timer_ennemi += 1
        if timer_ennemi > 60 and peut_spawner_ennemis:
            ennemis.add(Enemy(SCREEN_WIDTH))
            timer_ennemi = 0

        ennemis.update()
        for ennemi in ennemis:
            fen.blit(ennemi.image, ennemi.rect)

        for ennemi in pygame.sprite.spritecollide(joueur, ennemis, True):
            joueur.health -= 10
            #jouer_son_de_hit()

        if joueur.health <= 0:
            en_cours = False
            victoire = False

        if portail and joueur.rect.colliderect(portail):
            en_cours = False
            victoire = True

        joueur.update()
        fen.blit(joueur.image, joueur.rect)
        joueur.draw_health_bar(fen)

        if portail:
            fen.blit(image_portail, (portail.x, portail.y))

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    if victoire:
        return afficher_message("Félicitations ! Vous avez réussi !", (0, 255, 0))
    else:
        return afficher_message("Vous avez perdu. Réessayez !", (255, 0, 0))
    
