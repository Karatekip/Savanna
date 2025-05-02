import pygame
import random
from entities.humans.houses import House

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
        self.hunger_speed = 0.01
        self.food_proportion = 5

    
    def update(self, tree_group, humans_group, storage_house, giraffe_group):
        
        
        
        # hunger
        self.hunger += self.hunger_speed
        if self.hunger > 100:
            self.die()
        if self.hunger > 90:
            self.mission = "home"



        #Chaising
        if storage_house.food_storage < (self.food_proportion * len(humans_group)):
            self.mission = "hunt"
        
        
        if self.mission == "hunt":
            if len(giraffe_group) == 0:
                return
            
            closest_giraffe = min(giraffe_group, key=lambda giraffe: pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(giraffe.rect.center)))
            target_x, target_y = closest_giraffe.rect.center

            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 1:
                self.rect.centerx += int(self.speed * dx / distance)
                self.rect.centery += int(self.speed * dy / distance)
            
            if self.rect.colliderect(closest_giraffe.rect):
                giraffe_group.remove(closest_giraffe)
                print("Giraffe hunted by human at", self.rect.center)
                self.mission = "home"
                self.hunger += 2
                storage_house.food_storage += 20

            

        
        # going to closest tree
        if self.mission == "logging":
            if len(tree_group) == 0:
                return
            
            closest_tree = min(tree_group, key=lambda tree: pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(tree.rect.center)))
            target_x, target_y = closest_tree.rect.center

            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 1:
                self.rect.centerx += int(self.speed * dx / distance)
                self.rect.centery += int(self.speed * dy / distance)

            if self.rect.colliderect(closest_tree.rect):

                tree_group.remove(closest_tree)
                print("Tree logged by human at", self.rect.center)
                self.mission = "home"
                self.hunger += 2
        
        # going home
        elif self.mission == "home":
            
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
                self.eat_from_storage(storage_house)
                self.mission = "logging"

    
    def eat_from_storage(self, storage_house):
        if storage_house.food_storage >= self.food_proportion:
            self.hunger -= self.food_proportion
            if self.hunger < 0:
                self.hunger = 0
            storage_house.food_storage -= self.food_proportion

    def die(self):
        print("Human died of hunger.")
        self.kill()



    def draw(self):
        self.screen.blit(self.image, self.rect)
        