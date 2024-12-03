import pygame
import sys
import os
from plt2 import charger_image

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
LARGEUR = 1100
HAUTEUR = 600
taille_ecran = (LARGEUR, HAUTEUR)

# Initialisation de l'écran
ecran = pygame.display.set_mode(taille_ecran)
pygame.display.set_caption("Jeu de plateforme avec obstacles")

# # Charger les images avec vérification de leur existence
def charger_image(nom_image, taille=None):
    chemin_image = os.path.join("assets", nom_image)
    if not os.path.isfile(chemin_image):
        print(f"Erreur : le fichier '{nom_image}' est manquant.")
        sys.exit()
    image = pygame.image.load(chemin_image).convert_alpha()
    if taille:
        image = pygame.transform.scale(image, taille)
    return image

background = charger_image("background.png", (3200, HAUTEUR))
player_img = charger_image("player.png", (50, 60))
platform_img = charger_image("platform.png")
goal_img = charger_image("goal.png", (100, 100))
enemy_img = charger_image("enemy.png", (50, 50))
obstacle_img = charger_image("obstacle.png", (100, 200))

# Initialisation de la police pour le texte du menu
police = pygame.font.Font(None, 74)

# Variables globales pour le joueur
joueur_largeur = player_img.get_width()
joueur_hauteur = player_img.get_height()
joueur_vitesse_x = 5
joueur_vitesse_y = 0
gravite = 0.8
saut_puissance = -15
sante_joueur = 1
sur_sol = False



def jeu_principal():
    global joueur_x, joueur_y, joueur_vitesse_y, sur_sol, sante_joueur

    joueur_x = 100
    joueur_y = HAUTEUR - joueur_hauteur - 50
    joueur_vitesse_y = 0
    sur_sol = False
    
    plateformes = [
        pygame.Rect(100, 500, 100, 20),
        pygame.Rect(310, 390, 100, 20),
        pygame.Rect(400, 390, 100, 20),
        pygame.Rect(550, 300, 100, 20),
        pygame.Rect(760, 300, 100, 20),
        pygame.Rect(850, 370, 100, 20),
        pygame.Rect(1150, 370, 100, 20),
        pygame.Rect(1700, 500, 100, 20),
        pygame.Rect(2100, 500, 100, 20),
        pygame.Rect(2700, 500, 100, 20)
    ]
    obstacles = [
        pygame.Rect(350, 600 - obstacle_img.get_height(), obstacle_img.get_width(), obstacle_img.get_height()),
        pygame.Rect(800, 600 - obstacle_img.get_height(), obstacle_img.get_width(), obstacle_img.get_height()),
        pygame.Rect(1150, 600 - obstacle_img.get_height(), obstacle_img.get_width(), obstacle_img.get_height()),
        
    ]
    goal_x = 3000
    ennemis = [{"rect": pygame.Rect(310, 350, 50, 50), "vitesse": 2},
               {"rect": pygame.Rect(700, 550, 50, 50), "vitesse": 2},
               {"rect": pygame.Rect(950, 350, 50, 50), "vitesse": 2},
               {"rect": pygame.Rect(1270, 550, 50, 50), "vitesse": 15},
               {"rect": pygame.Rect(1850, 550, 50, 50), "vitesse": 15},
               {"rect": pygame.Rect(900, 550, 50, 50), "vitesse": 2}]

    clock = pygame.time.Clock()
    jeu_en_cours = True
    deplacement_ecran = 0
    invulnerable_timer = 0

    while jeu_en_cours:
        
#         if invulnerable_timer == 0 and joueur_rect.colliderect(ennemi_rect):
#             sante_joueur -= 1
#             invulnerable_timer = 60  # Immunité temporaire (60 frames)
#         
#         
#         if invulnerable_timer > 0:
#              invulnerable_timer -= 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_en_cours = False

        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and joueur_x > 0:
            joueur_x -= joueur_vitesse_x
        if touches[pygame.K_RIGHT]:
            joueur_x += joueur_vitesse_x
        if touches[pygame.K_UP] and sur_sol:
            joueur_vitesse_y = saut_puissance
            sur_sol = False

        joueur_vitesse_y += gravite
        joueur_y += joueur_vitesse_y

        # Empêcher de traverser le sol
        if joueur_y >= HAUTEUR - joueur_hauteur:
            joueur_y = HAUTEUR - joueur_hauteur
            joueur_vitesse_y = 0
            sur_sol = True

        # Gestion des collisions avec les plateformes
        for plateforme in plateformes:
            # Ajuster les coordonnées de la plateforme pour tenir compte du défilement
            plateforme_rect = pygame.Rect(
                plateforme.x - deplacement_ecran, plateforme.y, plateforme.width, plateforme.height
            )

            # Vérifier si le joueur entre en collision par le dessus
            if (
                joueur_x + joueur_largeur > plateforme_rect.x  # Joueur à droite du bord gauche
                and joueur_x < plateforme_rect.x + plateforme_rect.width  # Joueur à gauche du bord droit
                and joueur_y <= plateforme_rect.y  # Joueur au-dessus de la plateforme
                and joueur_y + joueur_hauteur + joueur_vitesse_y > plateforme_rect.y  # Joueur descend vers la plateforme
            ):
                joueur_y = plateforme_rect.y - joueur_hauteur  # Positionner le joueur sur la plateforme
                joueur_vitesse_y = 0
                sur_sol = True



        # Gestion des collisions avec les obstacles
       
        for obstacle in obstacles:
            # Calcul des coordonnées ajustées par le décalage de l'écran
            obstacle_position_x = obstacle.x - deplacement_ecran

            # Collision par le dessus (atterrir sur l'obstacle)
            if (
                joueur_x + joueur_largeur >= obstacle_position_x
                and joueur_x < obstacle_position_x + obstacle.width
                and joueur_y + joueur_hauteur <= obstacle.y
                and joueur_y + joueur_hauteur + joueur_vitesse_y > obstacle.y
            ):
                joueur_y = obstacle.y - joueur_hauteur
                joueur_vitesse_y = 0
                sur_sol = True

            # Collision latérale (bloquer le passage)
            if joueur_y + joueur_hauteur > obstacle.y + 5 and joueur_y < obstacle.y + obstacle.height - 5:
                if joueur_x + joueur_largeur > obstacle_position_x and joueur_x < obstacle_position_x + obstacle.width / 2:
                    joueur_x = obstacle_position_x - joueur_largeur  # Collision côté gauche
                elif joueur_x < obstacle_position_x + obstacle.width and joueur_x + joueur_largeur > obstacle_position_x + obstacle.width:
                    joueur_x = obstacle_position_x + obstacle.width



        for ennemi in ennemis:
            # Ajuster les coordonnées de l'ennemi pour tenir compte du défilement
            ennemi_rect = pygame.Rect(
                ennemi["rect"].x - deplacement_ecran,
                ennemi["rect"].y,
                ennemi["rect"].width,
                ennemi["rect"].height,
            )

            # Détecter les collisions entre le joueur et l'ennemi
            if (
                joueur_x + joueur_largeur > ennemi_rect.x  # Joueur à droite du bord gauche de l'ennemi
                and joueur_x < ennemi_rect.x + ennemi_rect.width  # Joueur à gauche du bord droit de l'ennemi
                and joueur_y + joueur_hauteur > ennemi_rect.y  # Joueur en bas de l'ennemi
                and joueur_y < ennemi_rect.y + ennemi_rect.height  # Joueur en haut de l'ennemi
            ):
                sante_joueur -= 1
                print(f"Vous avez été touché ! Santé restante : {sante_joueur}")
                if sante_joueur <= 0:
                    print("Vous avez perdu !")
                    jeu_en_cours = False
                    
        

        # Gestion du défilement de l'écran
        bord_gauche = 350
        bord_droit = LARGEUR - 350

        if joueur_x > bord_droit and deplacement_ecran < background.get_width() - LARGEUR:
            deplacement_ecran += joueur_vitesse_x
            joueur_x = bord_droit
        elif joueur_x < bord_gauche and deplacement_ecran > 0:
            deplacement_ecran -= joueur_vitesse_x
            joueur_x = bord_gauche


        # Affichage des éléments
        ecran.blit(background, (-deplacement_ecran, 0))
        ecran.blit(player_img, (joueur_x, joueur_y))
        
#         # affichage des rectangle d'affichage
#         for obstacle in obstacles:
#             pygame.draw.rect(ecran, (255, 0, 0), (obstacle.x - deplacement_ecran, obstacle.y, obstacle.width, obstacle.height), 2)
#             pygame.draw.rect(ecran, (0, 255, 0), (joueur_x, joueur_y, joueur_largeur, joueur_hauteur), 2)
#             
#         for plateforme in plateformes:
#             pygame.draw.rect(ecran, (0, 0, 255), (plateforme.x - deplacement_ecran, plateforme.y, plateforme.width, plateforme.height), 2)
#             
#         for ennemi in ennemis:
#             pygame.draw.rect(ecran, (255, 255, 0), (ennemi["rect"].x - deplacement_ecran, ennemi["rect"].y, ennemi["rect"].width, ennemi["rect"].height), 2)
# 
#         pygame.draw.rect(ecran, (255, 0, 255), (goal_x - deplacement_ecran, HAUTEUR - goal_img.get_height(), goal_img.get_width(), goal_img.get_height()), 2)
#         
        
        # Affichage des plateformes
        for plateforme in plateformes:
            plateforme_img = pygame.transform.scale(platform_img, (plateforme.width, plateforme.height))
        # Ajuster la position en fonction du défilement
            ecran.blit(plateforme_img, (plateforme.x - deplacement_ecran, plateforme.y))

        for obstacle in obstacles:
            ecran.blit(obstacle_img, (obstacle.x - deplacement_ecran, obstacle.y))

        for ennemi in ennemis:
            if(ennemi == ennemis[0]):
                # Mettre à jour la position réelle de l'ennemi
                ennemi["rect"].x += ennemi["vitesse"]
                
                # Inverser la direction si l'ennemi atteint les bords de son aire de mouvement
                if ennemi["rect"].left < 250 or ennemi["rect"].right > 1000:
                    ennemi["vitesse"] *= -1

                # Afficher l'ennemi avec le décalage de l'écran
                ecran.blit(
                    enemy_img,
                    (ennemi["rect"].x - deplacement_ecran, ennemi["rect"].y),
                )
            if(ennemi==ennemis[1]):
                # Mettre à jour la position réelle de l'ennemi
                ennemi["rect"].x += ennemi["vitesse"]
                
                # Inverser la direction si l'ennemi atteint les bords de son aire de mouvement
                if ennemi["rect"].left < 420 or ennemi["rect"].right > 810:
                    ennemi["vitesse"] *= -1

                # Afficher l'ennemi avec le décalage de l'écran
                ecran.blit(
                    enemy_img,
                    (ennemi["rect"].x - deplacement_ecran, ennemi["rect"].y),
                )
                
            if(ennemi == ennemis[2]):
                # Mettre à jour la position réelle de l'ennemi
                ennemi["rect"].x += ennemi["vitesse"]
                
                # Inverser la direction si l'ennemi atteint les bords de son aire de mouvement
                if ennemi["rect"].left < 250 or ennemi["rect"].right > 1000:
                    ennemi["vitesse"] *= -1

                # Afficher l'ennemi avec le décalage de l'écran
                ecran.blit(
                    enemy_img,
                    (ennemi["rect"].x - deplacement_ecran, ennemi["rect"].y),
                )
                
            if(ennemi==ennemis[3]):
                # Mettre à jour la position réelle de l'ennemi
                ennemi["rect"].x += ennemi["vitesse"]
                
                # Inverser la direction si l'ennemi atteint les bords de son aire de mouvement
                if ennemi["rect"].left < 1250 or ennemi["rect"].right > 2900:
                    ennemi["vitesse"] *= -1

                # Afficher l'ennemi avec le décalage de l'écran
                ecran.blit(
                    enemy_img,
                    (ennemi["rect"].x - deplacement_ecran, ennemi["rect"].y),
                )
                
            if(ennemi == ennemis[4]):
                # Mettre à jour la position réelle de l'ennemi
                ennemi["rect"].x += ennemi["vitesse"]
                
                # Inverser la direction si l'ennemi atteint les bords de son aire de mouvement
                if ennemi["rect"].left < 1250 or ennemi["rect"].right > 2900:
                    ennemi["vitesse"] *= -1

                # Afficher l'ennemi avec le décalage de l'écran
                ecran.blit(
                    enemy_img,
                    (ennemi["rect"].x - deplacement_ecran, ennemi["rect"].y),
                )
                
            if(ennemi==ennemis[5]):
                # Mettre à jour la position réelle de l'ennemi
                ennemi["rect"].x += ennemi["vitesse"]
                
                # Inverser la direction si l'ennemi atteint les bords de son aire de mouvement
                if ennemi["rect"].left < 860 or ennemi["rect"].right > 1190:
                    ennemi["vitesse"] *= -1

                # Afficher l'ennemi avec le décalage de l'écran
                ecran.blit(
                    enemy_img,
                    (ennemi["rect"].x - deplacement_ecran, ennemi["rect"].y),
                )

        ecran.blit(goal_img, (goal_x - deplacement_ecran, HAUTEUR - goal_img.get_height()))

        # Victoire
        if joueur_x + joueur_largeur >= goal_x - deplacement_ecran:
            print("Vous avez atteint l'objectif !")
            jeu_en_cours = False

        pygame.display.flip()
        clock.tick(30)

jeu_principal()
pygame.quit()
sys.exit()
