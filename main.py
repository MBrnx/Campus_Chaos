import pygame
import sys, time
from pygame.sprite import Group
from joueur import Joueur
from sol import Sol
from projectiles import Projectile
from platforme import Platforme

class Jeu:

    def __init__(self):
        self.ecran = pygame.display.set_mode((1100, 600))
        pygame.display.set_caption("Chaos Campus")
        self.jeu_encours = True
        self.joueur_x, self.joueur_y = 300, 50
        self.taille = (32, 64)
        self.joueur_vitesse_x = 0
        self.joueur = Joueur(self.joueur_x, self.joueur_y, self.taille)
        self.sol = Sol()
        self.gravite = (0, 10)
        self.resistance = (0, 0)
        self.rect = pygame.Rect(0, 0, 1100, 600)
        self.collision_sol = False
        self.horloge = pygame.time.Clock()
        self.fps = 30
        self.projectile_groupe = Group()
        self.t1, self.t2 = 0, 0
        self.delta_temps = 0
        self.image_tir = pygame.image.load('image/tir.png')
        self.image_joueur = pygame.image.load('image/personnage.png')
        self.image_tir_rect = pygame.Rect(6, 10, 17, 11)
        self.image_tir = self.image_joueur.subsurface(self.image_tir_rect)  # Appliquez le rectangle de découpe à l'image

        self.platforme_groupe = Group()
        self.platforme_liste_rect = [pygame.Rect(0, 300, 300, 50), pygame.Rect(800, 300, 300, 50), pygame.Rect(400, 150, 300, 50)]

    def gravite_jeu(self):
            
            self.joueur.rect.y += self.gravite[1] + self.resistance[1]
                    

    def boucle_principale(self):

        dictionnaire_vide = {}
        dictionnaire_images = self.joueur.convertir_rect_surface(self.image_joueur, dictionnaire_vide)
        while self.jeu_encours:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_d:
                        self.joueur_vitesse_x = 10
                        self.joueur.direction = 1
                        self.joueur.etat = 'bouger'

                    if event.key == pygame.K_q:
                        self.joueur_vitesse_x = -10
                        self.joueur.direction = -1
                        self.joueur.etat = 'bouger'

                    if event.key == pygame.K_z:
                        if self.collision_sol: 
                            self.joueur.a_sauter = True
                            self.joueur.nombre_de_saut += 1
                            self.joueur.etat = 'saut'

                    if event.key == pygame.K_p:
                        self.t = time.time()
                        self.joueur.etat = 'attaque'

                if event.type == pygame.KEYUP:
                    
                    if event.key == pygame.K_d:
                        self.joueur_vitesse_x = 0
                        self.joueur.etat = 'debout'

                    if event.key == pygame.K_q:
                        self.joueur_vitesse_x = 0
                        self.joueur.etat = 'debout'
                    
                    if event.key == pygame.K_p:
                        self.t2 = time.time()
                        self.joueur.a_tire = True
                        self.joueur.etat = 'debout'

            if self.sol.rect.colliderect(self.joueur.rect):
                self.resistance = (0, -10)
                self.collision_sol = True
                self.joueur.nombre_de_saut = 0
            
            else:
                self.resistance = (0, 0)

            if self.joueur.a_sauter and self.collision_sol:
                if self.joueur.nombre_de_saut < 2 :
                    self.joueur.sauter()

            if self.joueur.a_tire:

                if len(self.projectile_groupe) < self.joueur.tir_autorise and self.delta_temps > 0.05:
                    projectile = Projectile(self.joueur.rect.x + 20, self.joueur.rect.y - 5, [10, 10], self.joueur.direction, self.image_tir)
                    self.projectile_groupe.add(projectile)
                    self.joueur.a_tire = False
                

            for projectile in self.projectile_groupe:
                projectile.mouvement(50)
                if projectile.rect.right >= self.rect.right or projectile.rect.left <= self.rect.left:
                    self.projectile_groupe.remove(projectile)

            for rectangle in self.platforme_liste_rect:
                platforme = Platforme(rectangle)
                self.platforme_groupe.add(platforme)
                if self.joueur.rect.midbottom[1] // 10 * 10 == platforme.rect.top and self.joueur.rect.colliderect(rectangle):
                    self.resistance = (0, -10)
                    self.joueur.nombre_de_saut = 0


            self.delta_temps = self.t2 - self.t1
            self.joueur.mouvement(self.joueur_vitesse_x)
            self.gravite_jeu()
            self.joueur.rect.clamp_ip(self.rect)
            self.ecran.fill((255, 255, 255))

            self.joueur.afficher(self.ecran, dictionnaire_images)
            self.sol.afficher(self.ecran)

            for platforme in self.platforme_groupe:
                platforme.afficher(self.ecran)

            for projectile in self.projectile_groupe:    
                print("Position du projectile:", projectile.rect.x, projectile.rect.y)
                projectile.afficher(self.ecran, self.delta_temps)

            pygame.draw.rect(self.ecran, (255, 0, 0), self.rect, 1)
            self.horloge.tick(self.fps)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    Jeu().boucle_principale()
    pygame.quit()
