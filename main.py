import pygame
import sys, time
from pygame.sprite import Group
from joueur import Joueur
from sol import Sol
from projectiles import Projectile
from platforme import Platforme
from ennemie import Ennemie

class Jeu:

    def __init__(self):

        # Initialiser pygame et le mixer
        pygame.init()
        pygame.mixer.init()

        # Charger les fichiers sonores
        son_ambiance = pygame.mixer.Sound('son/ambiance.wav')
        son_ambiance.play(-1)
        self.son_tir = pygame.mixer.Sound('son/tir.wav')
        self.son_jump = pygame.mixer.Sound('son/jump.wav')
        self.son_tir.set_volume(0.1)

        # Initialisation de l'écran
        self.ecran = pygame.display.set_mode((1100, 600))
        pygame.display.set_caption("Chaos Campus")
        self.jeu_encours = True


        # Chargement de l'image du fond
        self.image_background = pygame.image.load('image/back.jpeg').convert()

        # Définition des rectangles pour l'arrière-plan et le sol
        self.rect_arriere_plan = pygame.Rect(0, 0, 1023, 950)
        self.rect_sol = pygame.Rect(0, 951, 1023, 72)

        # Découpage de l'arrière-plan et du sol
        self.arriere_plan = self.image_background.subsurface(self.rect_arriere_plan)
        self.sol_image = self.image_background.subsurface(self.rect_sol)

        # Redimensionnement pour adapter les surfaces
        self.surface_arriere_plan = pygame.transform.scale(self.arriere_plan, (1100, 500))
        self.surface_sol_image = pygame.transform.scale(self.sol_image, (1100, 100))

        # Définition des FPS
        self.horloge = pygame.time.Clock()
        self.fps = 30

        # Initialisation du joueur
        self.joueur_x, self.joueur_y = 300, 50
        self.taille = (32, 64)
        self.joueur_vitesse_x = 0
        self.joueur = Joueur(self.joueur_x, self.joueur_y, self.taille)
        self.sol = Sol()
        self.gravite = (0, 10)
        self.resistance = (0, 0)
        self.rect = pygame.Rect(0, 0, 1100, 600)
        self.collision_sol = False
        self.projectile_groupe = Group()
        self.t1, self.t2 = 0, 0
        self.delta_temps = 0
        self.image_tir = pygame.image.load('image/tir.png').subsurface(pygame.Rect(6, 10, 17, 11))
        self.image_joueur = pygame.image.load('image/personnage.png').convert()
        self.platforme_groupe = Group()
        self.platforme_liste_rect = [pygame.Rect(0, 300, 300, 50), pygame.Rect(800, 300, 300, 50), pygame.Rect(400, 150, 300, 50)]

        # Initialisation des ennemis
        self.ennemi_count = 0  # Compteur d'ennemis
        self.ennemi_spawn_time = time.time()  # Temps du dernier spawn
        self.ennemis = Group()  # Groupe d'ennemis
        self.ennemis_tues = 0  # Compteur d'ennemis tués

        # Initialisation de l'invincibilité du joueur
        self.invincible = False
        self.invincibilite_temps = 0
        self.duree_invincibilite = 2  # 2 secondes d'invincibilité après un coup

        # Charger l'image du trophée
        self.image_trophee = pygame.image.load('image/trophee.png').subsurface((0, 0, 500, 500))
        self.image_trophee = pygame.transform.scale(self.image_trophee, (100, 100))  # Redimensionner le trophée à une taille raisonnable
        self.trophee_position = (500, 380)  # Position en bas à droite, légèrement décalée du bord
        self.trophee_affiche = False  # Flag pour savoir si le trophée doit être affiché

        # Rectangle pour détecter la collision avec le trophée
        self.trophee_rect = pygame.Rect(self.trophee_position[0], self.trophee_position[1], 100, 100)

        # Initialisation des plateformes une seule fois
        self.platforme_groupe = Group()
        for rectangle in self.platforme_liste_rect:
            platforme = Platforme(rectangle)
            self.platforme_groupe.add(platforme)

    def jouer_tir(self):
        self.son_tir.play()

    def jouer_jump(self):
        self.son_jump.play()



    def spawn_ennemi(self):
        """Faire apparaître un ennemi toutes les 3 secondes, jusqu'à un total de 4 ennemis."""
        if self.ennemi_count < 4 and time.time() - self.ennemi_spawn_time >= 3:
            direction = 1 if self.ennemi_count % 2 == 0 else -1  # Alternance de direction
            ennemi = Ennemie(500, 5, self.taille, self.platforme_groupe)
            ennemi.direction = direction
            self.ennemis.add(ennemi)
            self.ennemi_count += 1
            self.ennemi_spawn_time = time.time()

    def gravite_jeu(self):
        """Applique la gravité à tous les objets."""
        self.joueur.rect.y += self.gravite[1] + self.resistance[1]
        for ennemi in self.ennemis:
            ennemi.rect.y += self.gravite[1] + self.resistance[1]

    def afficher_ennemis_tues(self):
        """Affiche le nombre d'ennemis tués."""
        font = pygame.font.Font(None, 36)  # Police par défaut, taille 36
        texte = f"{self.ennemis_tues}/4"
        surface_texte = font.render(texte, True, (255, 0, 0))  # Texte en rouge
        self.ecran.blit(surface_texte, (self.ecran.get_width() - 100, self.ecran.get_height() - 40))

    def verifier_collision_ennemi(self):
        """Vérifie si le joueur entre en collision avec un ennemi."""
        if self.invincible:
            return  # Le joueur ne peut pas recevoir de dégâts s'il est invincible
        
        for ennemi in self.ennemis:
            if self.joueur.rect.colliderect(ennemi.rect):
                self.joueur.vie -= 1  # Le joueur perd 1 point de vie
                self.invincible = True  # Le joueur devient invincible après avoir pris un coup
                self.invincibilite_temps = time.time()  # Enregistrer l'heure du premier coup
                if self.joueur.vie <= 0:
                    self.joueur.vie = 0
                    self.afficher_mort()  # Afficher l'écran de la mort

    def afficher_mort(self):
        """Affiche un écran de mort avec des boutons."""
        font = pygame.font.Font(None, 74)
        texte = "Vous êtes mort"
        surface_texte = font.render(texte, True, (255, 0, 0))
        
        # Dessiner un fond semi-transparent pour l'écran de mort
        surface_fond = pygame.Surface(self.ecran.get_size())
        surface_fond.set_alpha(128)  # Transparence
        surface_fond.fill((0, 0, 0))
        
        self.ecran.blit(surface_fond, (0, 0))  # Appliquer le fond
        self.ecran.blit(surface_texte, (self.ecran.get_width() // 2 - surface_texte.get_width() // 2, self.ecran.get_height() // 2 - surface_texte.get_height() // 2))
        
        # Ajouter les boutons
        self.creer_boutons()
        pygame.display.flip()  # Rafraîchir l'écran

        # Attente pour que l'écran de mort soit visible
        self.gestion_boutons()

    def verifier_invincibilite(self):
        """Vérifie si la période d'invincibilité est terminée."""
        if self.invincible and time.time() - self.invincibilite_temps >= self.duree_invincibilite:
            self.invincible = False  # La période d'invincibilité est terminée


    def creer_boutons(self):
        """Crée les boutons de l'écran de mort et les centre."""
        font = pygame.font.Font(None, 36)

        # Créer les boutons avec des tailles fixes
        largeur_bouton = 200
        hauteur_bouton = 50
        espace_vertical = 20  # Espacement entre les boutons

        # Calculer la position de départ pour centrer les boutons
        start_x = (self.ecran.get_width() - largeur_bouton) // 2
        start_y = (self.ecran.get_height() - (hauteur_bouton * 3 + espace_vertical * 2) + 350 ) // 2

        # Créer les rectangles des boutons
        self.bouton_recommencer = pygame.Rect(start_x, start_y, largeur_bouton, hauteur_bouton)
        self.bouton_menu = pygame.Rect(start_x, start_y + hauteur_bouton + espace_vertical, largeur_bouton, hauteur_bouton)
        self.bouton_quitter = pygame.Rect(start_x, start_y + (hauteur_bouton + espace_vertical) * 2, largeur_bouton, hauteur_bouton)

        # Dessiner les boutons
        pygame.draw.rect(self.ecran, (0, 255, 0), self.bouton_recommencer)
        pygame.draw.rect(self.ecran, (0, 255, 0), self.bouton_menu)
        pygame.draw.rect(self.ecran, (255, 0, 0), self.bouton_quitter)

        # Ajouter du texte sur les boutons
        texte_recommencer = font.render("Recommencer", True, (255, 255, 255))
        texte_menu = font.render("Menu", True, (255, 255, 255))
        texte_quitter = font.render("Quitter", True, (255, 255, 255))

        # Centrer le texte sur les boutons
        self.ecran.blit(texte_recommencer, (self.bouton_recommencer.centerx - texte_recommencer.get_width() // 2, 
                                            self.bouton_recommencer.centery - texte_recommencer.get_height() // 2))
        self.ecran.blit(texte_menu, (self.bouton_menu.centerx - texte_menu.get_width() // 2, 
                                    self.bouton_menu.centery - texte_menu.get_height() // 2))
        self.ecran.blit(texte_quitter, (self.bouton_quitter.centerx - texte_quitter.get_width() // 2, 
                                        self.bouton_quitter.centery - texte_quitter.get_height() // 2))


    def gestion_boutons(self):
        """Gère les actions des boutons sur l'écran de mort."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.bouton_recommencer.collidepoint(event.pos):
                        self.recommencer()
                    elif self.bouton_menu.collidepoint(event.pos):
                        self.menu()
                    elif self.bouton_quitter.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

    def recommencer(self):
        """Redémarre le jeu."""
        self.__init__()  # Réinitialiser le jeu
        self.ecran.fill((255, 255, 255))  # Remplir l'écran en blanc pour réinitialiser l'affichage
        pygame.display.flip()  # Forcer le rafraîchissement de l'écran
        time.sleep(0.1)  # Attendre un court instant pour éviter des conflits de timing avec l'affichage
        self.boucle_principale()  # Relancer la boucle principale du jeu

    def menu(self):
        """Retourner au menu principal."""
        pygame.quit()
        sys.exit()

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
                            self.jouer_jump()

                    if event.key == pygame.K_p:
                        self.t = time.time()
                        self.joueur.etat = 'attaque'
                        self.jouer_tir()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d or event.key == pygame.K_q:
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
                if self.joueur.nombre_de_saut < 2:
                    self.joueur.sauter()

            if self.joueur.a_tire:
                if len(self.projectile_groupe) < self.joueur.tir_autorise and self.delta_temps > 0.05:
                    projectile = Projectile(self.joueur.rect.x - 10, self.joueur.rect.y + 10, [10, 10], self.joueur.direction, self.image_tir)
                    self.projectile_groupe.add(projectile)
                    self.joueur.a_tire = False

            for projectile in self.projectile_groupe:
                projectile.mouvement(50)
                if projectile.rect.right >= self.rect.right or projectile.rect.left <= self.rect.left:
                    self.projectile_groupe.remove(projectile)

            for rectangle in self.platforme_liste_rect:
                platforme = Platforme(rectangle)  # Cette ligne ne doit pas être répétée dans la boucle
                if self.joueur.rect.midbottom[1] // 10 * 10 == platforme.rect.top and self.joueur.rect.colliderect(rectangle):
                    self.resistance = (0, -10)
                    self.joueur.nombre_de_saut = 0


            self.delta_temps = self.t2 - self.t1
            self.joueur.mouvement(self.joueur_vitesse_x)
            self.gravite_jeu()
            self.joueur.rect.clamp_ip(self.rect)
            self.ecran.fill((255, 255, 255))

            self.ecran.blit(self.surface_arriere_plan, (0, 0))
            self.ecran.blit(self.surface_sol_image, (0, 500))
            self.joueur.afficher(self.ecran, dictionnaire_images)
            self.joueur.afficher_vie(self.ecran)

            for platforme in self.platforme_groupe:
                platforme.afficher(self.ecran)

            for projectile in self.projectile_groupe:
                projectile.afficher(self.ecran, self.delta_temps)

            self.spawn_ennemi()

            for ennemi in self.ennemis:
                ennemi.mouvement()
                ennemi.update()
                ennemi.afficher(self.ecran)

            # Vérifier les collisions entre les projectiles et les ennemis
            for projectile in self.projectile_groupe:
                if projectile.verifier_collision(self.ennemis, self.projectile_groupe):
                    self.ennemis_tues += 1

            # Retirer les ennemis morts
            for ennemi in self.ennemis:
                if ennemi.est_mort:
                    self.ennemis.remove(ennemi)

            # Afficher le nombre d'ennemis tués
            self.afficher_ennemis_tues()

            self.verifier_collision_ennemi()
            self.verifier_invincibilite()

            # Vérifier si tous les ennemis sont tués pour afficher le trophée
            if self.ennemis_tues == 4:
                self.trophee_affiche = True

            if self.trophee_affiche:
                self.ecran.blit(self.image_trophee, self.trophee_position)
            
            # Vérifier si le joueur est proche du trophée
            if self.trophee_affiche and self.joueur.rect.colliderect(self.trophee_rect):
                # Afficher le texte d'instruction
                font = pygame.font.Font(None, 36)  # Police par défaut, taille 36
                texte_instruction = "Appuyez sur E pour finir le niveau"
                surface_texte = font.render(texte_instruction, True, (255, 255, 255))  # Texte en blanc
                x_text = self.trophee_position[0] + self.trophee_rect.width // 2 - surface_texte.get_width() // 2
                y_text = self.trophee_position[1] - 40
                self.ecran.blit(surface_texte, (x_text, y_text))

                # Vérifier si le joueur appuie sur E
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.menu()  



            pygame.draw.rect(self.ecran, (255, 0, 0), self.rect, 1)
            self.horloge.tick(self.fps)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    Jeu().boucle_principale()
    pygame.quit()
