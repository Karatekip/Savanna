import pygame
import random

class Human(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen, human_spawn_pos):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        self.human_spawn_pos = human_spawn_pos
        self.human_spawn_pos_x, self.human_spawn_pos_y = self.human_spawn_pos
        self.hunger = 0
        self.color = (51, 25, 0)
        self.width, self.height = 10, 20
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))

        self.rect = self.image.get_rect()
        self.x_pos = self.human_spawn_pos_x + random.randint(-100, 100)
        self.y_pos = self.human_spawn_pos_y + random.randint(-100, 100)
        if self.x_pos < 0:
            self.x_pos = 0
        elif self.x_pos > screen_x:
            self.x_pos = screen_x
        if self.y_pos < 0:
            self.y_pos = 0
        elif self.y_pos > screen_y:
            self.y_pos = screen_y

        self.rect.center = (self.x_pos, self.y_pos)
        self.mission = "logging"
        self.speed = 1.5
    
    def update(self, tree_group, giraffe_group):
        # hunger
        self.hunger += 0.01
        

        if self.mission == "logging":
            if len(tree_group) == 0:
                return  # No trees to cut
            # Find closest tree
            closest_tree = min(tree_group, key=lambda tree: pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(tree.rect.center)))
            target_x, target_y = closest_tree.rect.center

            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 1:
                self.rect.centerx += int(self.speed * dx / distance)
                self.rect.centery += int(self.speed * dy / distance)

            if self.rect.colliderect(closest_tree.rect):
                # Optionally play animation / sound
                tree_group.remove(closest_tree)
                print("Tree logged by human at", self.rect.center)
                self.mission = "home"
                self.hunger += 10
        
        elif self.mission == "home":
            # Move towards the human spawn position
            target_x, target_y = self.human_spawn_pos

            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 1:
                self.rect.centerx += int(self.speed * dx / distance)
                self.rect.centery += int(self.speed * dy / distance)

            else:
                # Optionally play animation / sound
                print("Human returned home at", self.rect.center)
                self.mission = "logging"
    


    def draw(self):
        self.screen.blit(self.image, self.rect)
        