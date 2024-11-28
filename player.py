import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 1000
        self.max_health = 100
        self.attack = 10
        self.velocity = 3
        self.position_x = 250.0
        
        # Charger les images pour l'animation
        self.images = [
            pygame.image.load('images/marche_1.png'),
            pygame.image.load('images/marche_2.png'),
            pygame.image.load('images/marche_3.png'),
            pygame.image.load('images/marche_4.png')
        ]
        self.images = [pygame.transform.scale(img, (80, 100)) for img in self.images]
        self.image = self.images[0]

        # Initialisation du rectangle
        self.rect = self.image.get_rect()
        self.rect.x = int(self.position_x)
        self.image_index = 0
        self.animation_timer = 0
        self.is_moving = False
        self.facing_right = True

    def move(self, direction, screen_width):
        if direction == 'right' and self.rect.right + self.velocity <= screen_width:
            self.position_x += self.velocity
            self.is_moving = True
            self.facing_right = True
        elif direction == 'left' and self.rect.left - self.velocity >= 0:
            self.position_x -= self.velocity
            self.is_moving = True
            self.facing_right = False
        else:
            self.is_moving = False

        self.rect.x = round(self.position_x)

    def update(self):
        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer > 10:
                self.animation_timer = 0
                self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
        else:
            self.image = self.images[0]

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        x_position = 10
        y_position = screen.get_height() - bar_height - 15
        pygame.draw.rect(screen, (255, 0, 0), (x_position, y_position, bar_width, bar_height))
        current_health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, (0, 255, 0), (x_position, y_position, current_health_width, bar_height))
