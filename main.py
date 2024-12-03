import pygame
import time
import random
from player import Player
from enemy import Enemy
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS

# Initialisation de Pygame
pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('images/BDD Niv_ax fond_audio.MP3') 
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(0) 

# Charger le son de collision
sons_de_hit = [pygame.mixer.Sound('images/degats.MP3') for _ in range(5)]  # Précharger 5 sons
index_son_hit = 0  

def jouer_son_de_hit():
    """Jouer un son de collision avec préchargement pour réduire la latence."""
    global index_son_hit
    sons_de_hit[index_son_hit].play()
    index_son_hit = (index_son_hit + 1) % len(sons_de_hit)

# Paramètres de la fenêtre
ecran = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chaos Campus")

# Charger l'icône du jeu
icone = pygame.image.load('images/Capture_d_écran_2024-11-05_à_16.06.34-removebg-preview.png')
pygame.display.set_icon(icone)

# Chronomètre de 121 secondes
temps_debut = time.time()  
intervalle_changement = 10  
temps_total = 121  

# Liste des 12 images de fond
fonds = [
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

index_fond = 0
fond = pygame.image.load(fonds[index_fond])
fond = pygame.transform.scale(fond, (SCREEN_WIDTH, SCREEN_HEIGHT))

image_portail = pygame.image.load('images/Portail.png')

image_portail = pygame.transform.scale(image_portail, (150, 150)) 
rect_portail = image_portail.get_rect()

# Initialiser l'horloge
horloge = pygame.time.Clock()

def changer_fond(nouveau_fond_path):
    """Changer le fond pendant le jeu."""
    nouveau_fond = pygame.image.load(nouveau_fond_path)
    nouveau_fond = pygame.transform.scale(nouveau_fond, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return nouveau_fond

def init_joueur():
    """Initialise le joueur et le place correctement."""
    joueur = Player()
    hauteur_fond = fond.get_height()
    hauteur_joueur = joueur.image.get_height()
    position_trottoir_y = hauteur_fond - 55  
    joueur.rect.y = position_trottoir_y - hauteur_joueur
    return joueur

def afficher_message(message, couleur):
    """Affiche un message générique à la fin du jeu."""
    police = pygame.font.Font(None, 50)
    en_cours = True
    while en_cours:
        ecran.fill((0, 0, 0))  
        texte = police.render(message, True, couleur)
        texte_quitter = police.render("Appuyez sur Q pour quitter.", True, (255, 255, 255))
        texte_reessayer = police.render("Appuyez sur R pour réessayer.", True, (255, 255, 255))

        ecran.blit(texte, (SCREEN_WIDTH // 2 - texte.get_width() // 2, 150))
        ecran.blit(texte_quitter, (SCREEN_WIDTH // 2 - texte_quitter.get_width() // 2, 300))
        ecran.blit(texte_reessayer, (SCREEN_WIDTH // 2 - texte_reessayer.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
                pygame.quit()
                return "quitter"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: 
                    en_cours = False
                    pygame.quit()
                    return "quitter"
                if event.key == pygame.K_r:
                    return "reessayer"

def spawn_portail():
    rect_portail.x = random.randint(0, SCREEN_WIDTH - rect_portail.width)
    rect_portail.y = SCREEN_HEIGHT - rect_portail.height - 55 
    return rect_portail

# Boucle principale
while True:
    # Initialiser le joueur et les ennemis
    joueur = init_joueur()
    ennemis = pygame.sprite.Group()
    timer_ennemi = 0
    peut_spawner_ennemis = True
    portail = None  

    # Boucle de jeu
    en_cours = True
    victoire = False  # Indicateur de victoire ou défaite

    while en_cours:
        ecran.blit(fond, (0, 0))

        temps_ecoule = time.time() - temps_debut
        temps_restant = temps_total - temps_ecoule

        if temps_ecoule >= 121:
            if portail is None:
                portail = spawn_portail()  
            peut_spawner_ennemis = False  

        # Change le fond toutes les 10 secondes
        if int(temps_ecoule) % intervalle_changement == 0 and temps_ecoule < temps_total:
            nouveau_fond_path = fonds[(int(temps_ecoule) // intervalle_changement) % len(fonds)]
            if nouveau_fond_path != fonds[index_fond]:  
                fond = changer_fond(nouveau_fond_path)
                index_fond = fonds.index(nouveau_fond_path)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                en_cours = False
                pygame.quit()
                break

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
            ecran.blit(ennemi.image, ennemi.rect)

        for ennemi in pygame.sprite.spritecollide(joueur, ennemis, True):
            print("Collision avec un ennemi détectée !")
            joueur.health -= 10
            jouer_son_de_hit()

        if joueur.health <= 0:
            print("Le joueur n'a plus de vie. Fin du jeu.")
            en_cours = False
            victoire = False

        # Vérifier la collision avec le portail si il est activé
        if portail and joueur.rect.colliderect(portail):
            print("Le joueur a touché le portail !")
            en_cours = False
            victoire = True

        joueur.update()
        ecran.blit(joueur.image, joueur.rect)
        joueur.draw_health_bar(ecran)

        # Afficher le portail uniquement après 121 secondes
        if portail:
            ecran.blit(image_portail, portail)

        pygame.display.flip()
        horloge.tick(FPS)

    # Afficher le résultat
    if victoire:
        resultat = afficher_message("Félicitations ! Vous avez réussi à sortir de ce cauchemar !", (0, 255, 0))
    else:
        resultat = afficher_message("Vous avez perdu. Réessayez !", (255, 0, 0))

    if resultat == "quitter":
        pygame.mixer.music.stop()
        break
        break
    elif resultat == "reessayer":
        pygame.mixer.music.stop()
        pygame.mixer.music.play(0)
        temps_debut = time.time()  # Réinitialiser le chronomètre
        continue




