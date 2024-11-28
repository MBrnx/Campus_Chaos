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

def calculer_niveau(xp):
    niveau = xp // 100  # 100 XP par niveau
    xp_restant = xp % 100
    return niveau, xp_restant

pygame.init()

fen = pygame.display.set_mode((1100, 600))
pygame.display.set_caption("Chaos Campus")

# Importation des différentes images 
fond = pygame.image.load(os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "bg.png"))
bouton1 = os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "bouton1.png")
bouton2 = os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "bouton2.png")
bouton3 = os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "bouton3.png")
play = os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "start.png")

# Changement de l'icon dans la barre des tâches 
icon = pygame.image.load(os.path.join("/Users/mathisbruniaux/Desktop/Informatique/L2 informatique 2024-2025/S1/dev app/Projet/Projet/images", "icon.png"))
pygame.display.set_icon(icon)

# Mise en place des différents boutons en fonction d'une position donnée 
bouton1 = Bouton(bouton1, (228, 218))
bouton2 = Bouton(bouton2, (623, 314))
bouton3 = Bouton(bouton3, (983, 391))
bouton = Bouton(play, (550, 300))

# Mise en place des différentes fonctions à lancer 
continuer = True
jeu_en_cours = False
score_niveau1 = 0
score_niveau2 = 0
click = False 
experience = 0

if not afficher_intro(fen, bouton):
    continuer = False 

while continuer:
    fen.blit(fond, (0, 0))
    souris_pos = pygame.mouse.get_pos()
    
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
            if not click and bouton.is_clicked(souris_pos):
                click = True
                continuer = True
            if bouton1.is_clicked(souris_pos):
                jeu_en_cours = True
                score_niveau1 = 0
                score_niveau2 = 0
            elif bouton2.is_clicked(souris_pos):
                if score_niveau1 >= 5:
                    jeu_en_cours = True
                    score_niveau2 = 0
                else:
                    pygame.time.delay(20)
            elif bouton3.is_clicked(souris_pos):
                if score_niveau2 >= 5:
                    jeu_en_cours = True
                else:
                    pygame.time.delay(20)

    # Calculer le niveau et le reste d'XP
    niveau, xp_restant = calculer_niveau(experience)

    # Afficher l'XP et le niveau
    font = pygame.font.Font(None, 36)
    xp_text = font.render(f'XP: {experience}', True, (255, 255, 255))
    fen.blit(xp_text, (10, 50))
    niveau_text = font.render(f'Niveau: {niveau} ({xp_restant}/100)', True, (255, 255, 255))
    fen.blit(niveau_text, (10, 80))

    # Affichage des niveaaux vérouillés en bas de l'écran 
    if score_niveau1 < 5:
        text = font.render("Niveau 2 verrouillé : Atteignez un score de 5 dans le Niveau 1", True, (255, 0, 0))
        fen.blit(text, (200, 520))
    if score_niveau2 < 5:
        text = font.render("Niveau 3 verrouillé : Atteignez un score de 5 dans le Niveau 2", True, (255, 0, 0))
        fen.blit(text, (200, 550))

    pygame.display.flip()

    if jeu_en_cours:
        # Niveau 1
        result = niveau1(fen, score_niveau1)
        if result == "menu":
            jeu_en_cours = False
            score_niveau1 = 0  # Réinitialisation du score
            score_niveau2 = 0  # Réinitialisation du score
            continue  # Retour à l'écran d'accueil
        else:
            score_niveau1 = result

        # Niveau 2
        if score_niveau1 >= 5:
            result = niveau2(fen, score_niveau2)
            if result == "menu":
                jeu_en_cours = False
                score_niveau1 = 0  # Réinitialisation du score
                score_niveau2 = 0  # Réinitialisation du score
                continue  # Retour à l'écran d'accueil
            else:
                score_niveau2 = result

        # Niveau 3
        if score_niveau2 >= 5:
            result = niveau3(fen)
            if result == "menu":
                jeu_en_cours = False
                score_niveau1 = 0  # Réinitialisation du score
                score_niveau2 = 0  # Réinitialisation du score
                continue  # Retour à l'écran d'accueil

pygame.quit()