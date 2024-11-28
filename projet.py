# Importation des différentes bibliothèque utile dans le code 
import pygame
import os

# Importation des différents niveau du jeu 
from niveau1 import niveau1
from niveau2 import niveau2
from niveau3 import niveau3 

# Importation de bouton
from bouton import Bouton

# Importation de l'introduction du jeu 
from intro import afficher_intro

pygame.init()

fen = pygame.display.set_mode((1100, 600))
pygame.display.set_caption("Chaos Campus")

# Importation des différentes images 
fond = pygame.image.load(os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "bg.png"))
bouton1_img = os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "bouton1.png")
bouton2_img = os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "bouton2.png")
bouton3_img = os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "bouton3.png")
play_img = os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "start.png")

# Changement de l'icon dans la barre des tâches 
icon = pygame.image.load(os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "icon.png"))
pygame.display.set_icon(icon)

# Mise en place des différents boutons en fonction d'une position donnée 
bouton1 = Bouton(bouton1_img, (228, 218))
bouton2 = Bouton(bouton2_img, (623, 314))
bouton3 = Bouton(bouton3_img, (983, 391))
bouton_start = Bouton(play_img, (550, 300))

# Variables du jeu
continuer = True
score_niveau1 = 0
score_niveau2 = 0
score_niveau3 = 0
jeu_en_cours = False

# Afficher l'intro
if not afficher_intro(fen, bouton_start):
    continuer = False

while continuer:
    fen.blit(fond, (0, 0))
    souris_pos = pygame.mouse.get_pos()
    
    # Gestion des boutons
    bouton1.check_hover(souris_pos)
    bouton2.check_hover(souris_pos)
    bouton3.check_hover(souris_pos)
    bouton1.draw(fen)
    bouton2.draw(fen)
    bouton3.draw(fen)

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            continuer = False

        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
            if bouton1.is_clicked(souris_pos):
                result = niveau1(fen, score_niveau1)
                if isinstance(result, int):
                    score_niveau1 = result
            elif bouton2.is_clicked(souris_pos):
                if score_niveau1 >= 5:  # Condition pour débloquer le niveau 2
                    result = niveau2(fen, score_niveau2)
                    if isinstance(result, int):
                        score_niveau2 = result
            elif bouton3.is_clicked(souris_pos):
                if score_niveau2 >= 5:  # Condition pour débloquer le niveau 3
                    result = niveau3(fen, score_niveau3)
                    if isinstance(result, int):
                        score_niveau2 = result

    # Afficher les messages de verrouillage des niveaux
    font = pygame.font.Font(None, 24)
    if score_niveau1 < 5:
        text = font.render("Niveau 2 verrouillé : Atteignez un score de 5 dans le Niveau 1", True, (255, 0, 0))
        fen.blit(text, (200, 520))
    if score_niveau2 < 5:
        text = font.render("Niveau 3 verrouillé : Atteignez un score de 5 dans le Niveau 2", True, (255, 0, 0))
        fen.blit(text, (200, 550))
        
    if jeu_en_cours:
        # Lors du clic sur les boutons, assurez-vous de passer le score en paramètre pour chaque niveau
        
        # Niveau 1
        if bouton1.is_clicked(souris_pos): 
            result = niveau1(fen, score_niveau1)  # Passer le score actuel
            if result == "menu":
                jeu_en_cours = False  # Retour au menu principal
            else:
                score_niveau1 = result  # Mise à jour du score du niveau 1

        # Niveau 2
        elif bouton2.is_clicked(souris_pos):
            if score_niveau1 >= 5:
                result = niveau2(fen, score_niveau2)  # Passer le score actuel
                if result == "menu":
                    jeu_en_cours = False  # Retour au menu principal
                else:
                    score_niveau2 = result  # Mise à jour du score du niveau 2

        # Niveau 3 
        elif bouton2.is_clicked(souris_pos):
            if score_niveau2 >= 5:
                result = niveau3(fen, score_niveau2)  # Passer le score actuel
                if result == "menu":
                    jeu_en_cours = False  # Retour au menu principal
                else:
                    score_niveau3 = result  # Mise à jour du score du niveau 3

    pygame.display.flip()

pygame.quit()