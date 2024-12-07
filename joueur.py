import pygame

class Joueur(pygame.sprite.Sprite):

    def __init__(self, x, y, taille):

        super().__init__()
        self.x = x
        self.y = y
        self.taille = taille
        self.rect = pygame.Rect(self.x, self.y, self.taille[0], self.taille[1])
        self.saut = 0
        self.saut_montee = 0
        self.saut_descente = 5
        self.nombre_de_saut = 0
        self.a_sauter = False
        self.a_tire = False
        self.tir_autorise = 1
        self.direction = 1

        self.vie = 2

        self.image_joueur = pygame.image.load("Desktop/Projet/images/personnage.png")

        self.joueur_debout = [pygame.Rect(84, 29, 92, 136)]

        self.joueur_marche = [
            pygame.Rect(179, 29, 92, 136),
            pygame.Rect(274, 29, 92, 136),
            pygame.Rect(465, 29, 92, 136),
            pygame.Rect(100, 220, 110, 136),
            pygame.Rect(210, 220, 135, 136)]
        
        self.joueur_saute = [pygame.Rect(370, 29, 92, 136),]

        self.joueur_tir = [pygame.Rect(210, 220, 135, 136)]

        self.etat = 'debout'
        self.index = 0

    def mouvement(self, vitesse):
        """
        creer le mouvement de gauche a droite
        :param vitesse:
        """

        self.rect.x += vitesse   

    def afficher(self, surface, dico):
        """
        affiche le joueur
        :param surface:
        """
        self.index += 1

        if self.index >= len(dico[self.etat]):
            self.index = 0

        image = dico[self.etat][self.index]

        if self.direction == -1:
            image = pygame.transform.flip(image, True, False)

        surface.blit(image, self.rect)
        pygame.draw.rect(surface, (0, 255, 255), self.rect, 1)

    def sauter(self):

        if self.a_sauter:

            if self.saut_montee >= 10:
                self.saut_descente -= 1
                self.saut = self.saut_descente
            
            else:

                self.saut_montee += 1
                self.saut = self.saut_montee
            
            if self.saut_descente < 0 :
                self.saut_montee = 0
                self.saut_descente = 5
                self.a_sauter = False
        
        self.rect.y = self.rect.y - (10 * (self.saut / 2))
    
    def convertir_rect_surface(self, image, dico):

        for image_debout in self.joueur_debout:

            joueur_rectangle_supprime = self.joueur_debout.pop(0)
            image_joueur = image.subsurface(joueur_rectangle_supprime)
            image_joueur = pygame.transform.scale(image_joueur, (32, 64))
            self.joueur_debout.append(image_joueur)

        dico['debout'] = self.joueur_debout

        for image_marche in self.joueur_marche:

            image_rect = self.joueur_marche.pop(0)
            image_joueur = image.subsurface(image_rect)
            image_joueur = pygame.transform.scale(image_joueur, (32,64))
            self.joueur_marche.append(image_joueur)

        dico['bouger'] = self.joueur_marche

        for image_saut in self.joueur_saute:

            image_sa = self.joueur_saute.pop(0)
            image_joueur = image.subsurface(image_sa)
            image_joueur = pygame.transform.scale(image_joueur, (32, 64))
            self.joueur_saute.append(image_joueur)

        dico['saut'] = self.joueur_saute

        for image_tir in self.joueur_tir:

            image_t = self.joueur_tir.pop(0)
            image_joueur = image.subsurface(image_t)
            image_joueur = pygame.transform.scale(image_joueur, (32, 64))
            self.joueur_tir.append(image_joueur)

        dico['attaque'] = self.joueur_tir

        return dico
    
    def afficher_vie(self, surface):
        """Affiche la barre de vie du joueur en bas à gauche."""
        # Dimensions de la barre de vie
        largeur_barre = 100
        hauteur_barre = 10
        marge = 10
            
        # Couleur de la barre de vie
        couleur_fond = (255, 0, 0)  # Rouge pour le fond
        couleur_vie = (0, 255, 0)   # Vert pour la vie restante
            
        # Dessiner le fond de la barre de vie
        pygame.draw.rect(surface, couleur_fond, (marge, surface.get_height() - hauteur_barre - marge, largeur_barre, hauteur_barre))
            
        # Dessiner la vie restante
        vie_restante = int((self.vie / 2) * largeur_barre)  # Calculer la largeur de la barre de vie
        pygame.draw.rect(surface, couleur_vie, (marge, surface.get_height() - hauteur_barre - marge, vie_restante, hauteur_barre))

