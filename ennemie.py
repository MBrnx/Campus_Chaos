import pygame

class Ennemie(pygame.sprite.Sprite):
    def __init__(self, x, y, taille, platforme_groupe):
        super().__init__()

        # Position et dimensions
        self.x = x
        self.y = y
        self.taille = taille
        self.rect = pygame.Rect(self.x, self.y, self.taille[0], self.taille[1])

        # Charger l'image de l'ennemi
        self.image_ennemi = pygame.image.load("Desktop/Projet/images/personnage.png").convert_alpha()

        # Liste des frames pour l'animation
        frames = [
            pygame.Rect(179, 29, 92, 136),
            pygame.Rect(274, 29, 92, 136),
            pygame.Rect(465, 29, 92, 136),
            pygame.Rect(100, 220, 110, 136),
            pygame.Rect(210, 220, 135, 136),
        ]

        # Extraire et redimensionner les frames
        self.joueur_marche = [
            self.couleurs_inverse(pygame.transform.scale(self.image_ennemi.subsurface(frame), (32, 64)))
            for frame in frames
        ]

        # Animation
        self.image = self.joueur_marche[0]
        self.current_frame = 0
        self.animation_speed = 4
        self.frame_counter = 0

        # Saut et mouvements
        self.saut = 0
        self.saut_montee = 0
        self.saut_descente = 5
        self.nombre_de_saut = 0
        self.a_sauter = False
        self.direction = 1  # 1 pour droite, -1 pour gauche
        self.est_stable = False
        self.platforme_groupe = platforme_groupe

        # Vie de l'ennemi
        self.vie = 2  # L'ennemi a 2 vies
        self.est_mort = False  # L'ennemi est vivant au début

    def couleurs_inverse(self, image):
        """Inverse les couleurs de l'image."""
        width, height = image.get_size()
        pixels = pygame.surfarray.pixels3d(image)

        for y in range(height):
            for x in range(width):
                pixels[x, y] = (255 - pixels[x, y][0], 255 - pixels[x, y][1], 255 - pixels[x, y][2])

        return image

    def mouvement(self):
        """Déplacement de l'ennemi avec gestion des plateformes et du sol."""
        if self.est_mort:
            return  # Si l'ennemi est mort, il ne bouge pas

        # Mise à jour de l'animation
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.joueur_marche)
            self.image = self.joueur_marche[self.current_frame]

        # Déplacement horizontal avec inversion aux bords
        if self.rect.right >= 1100 or self.rect.left <= 0:
            self.direction = -self.direction  # Inverser la direction à chaque bord
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.x += self.direction * 3  # Mouvement horizontal de l'ennemi

        self.est_stable = False  # Initialiser la stabilité à False
        nouvelle_position = self.rect.bottom

        # Vérification des plateformes sous l'ennemi
        for platforme in self.platforme_groupe:
            if self.rect.colliderect(platforme.rect):  # Collision avec une plateforme
                # Si l'ennemi est bien sur la plateforme (zone de contact)
                if self.rect.bottom <= platforme.rect.top + 10 and self.rect.bottom >= platforme.rect.top:
                    # Réajuster la position de l'ennemi pour qu'il se pose sur la plateforme
                    nouvelle_position = platforme.rect.top
                    self.est_stable = True  # L'ennemi est stable sur la plateforme
                    break

        # Si aucune plateforme n'est détectée sous l'ennemi, appliquer la gravité
        if not self.est_stable:
            self.rect.y += self.saut_descente  # Applique la gravité
            if self.rect.bottom >= 475:  # Limite avec le sol
                self.rect.bottom = 475
                self.est_stable = True
        else:
            self.rect.bottom = nouvelle_position  # Réajuster la position pour rester sur la plateforme

    def subir_degats(self):
        """Réduit la vie de l'ennemi lorsqu'il est touché par un projectile."""
        if not self.est_mort:
            self.vie -= 1
            if self.vie <= 0:
                self.est_mort = True  # L'ennemi est mort
                return True
        return False

    def afficher(self, ecran):
        """Affiche l'ennemi à l'écran."""
        if self.est_mort:
            return  # Ne pas afficher l'ennemi s'il est mort

        # Si l'ennemi regarde à gauche, retourner l'image
        if self.direction == -1:
            image_flipped = pygame.transform.flip(self.image, True, False)
            ecran.blit(image_flipped, (self.rect.x, self.rect.y))
        else:
            ecran.blit(self.image, (self.rect.x, self.rect.y))
