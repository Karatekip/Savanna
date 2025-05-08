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
        self.age = 0
        self.generation = 1

        self.breed_timer = 0
        self.breed_timer_interval = random.randint(500, 1000)

        
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 220, 177), (self.width // 2, 5), 4)  # Head
        pygame.draw.rect(self.image, self.color, (2, 8, 6, 12))  # Body
        

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
        self.caught_giraffe = False
        self.caught_wood = False
        
        self.build_storage_timer = 0
        self.time_to_build_storage = 1000

    
    def update(self, tree_group, humans_group, storage_house_group, giraffe_group, House, tot_food_storage, tot_wood_storage, tot_food_storage_max, tot_wood_storage_max):
        
        closest_storage_house = min(storage_house_group, key=lambda storage_house: pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(storage_house.rect.center)))
        self.x_pos = float(self.rect.centerx)
        self.y_pos = float(self.rect.centery)
        
        
        
        # hunger
        self.hunger += self.hunger_speed
        if self.hunger > 100:
            self.die()
        if self.hunger > 90:
            self.mission = "home"



        #Chaising
        if tot_food_storage <= (self.food_proportion * len(humans_group)) and self.caught_giraffe == False:
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
                self.x_pos += self.speed * dx / distance
                self.y_pos += self.speed * dy / distance
                self.rect.center = (int(self.x_pos), int(self.y_pos))

            
            if self.rect.colliderect(closest_giraffe.rect):
                giraffe_group.remove(closest_giraffe)
                #print("Giraffe hunted by human at", self.rect.center)
                self.mission = "home"
                self.caught_giraffe = True
                self.hunger += 2
                

            

        
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
                self.x_pos += self.speed * dx / distance
                self.y_pos += self.speed * dy / distance
                self.rect.center = (int(self.x_pos), int(self.y_pos))


            if self.rect.colliderect(closest_tree.rect):

                tree_group.remove(closest_tree)
                #print("Tree logged by human at", self.rect.center)
                self.mission = "home"
                self.caught_wood = True
                self.hunger += 2
        



        # going home
        if self.mission == "home":
            
            target_x, target_y = self.human_spawn_pos

            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 1:
                self.x_pos += self.speed * dx / distance
                self.y_pos += self.speed * dy / distance
                self.rect.center = (int(self.x_pos), int(self.y_pos))


            else:
                # Optionally play animation / sound
                #print("Human returned home at", self.rect.center)
                self.eat_from_storage(closest_storage_house)
                self.mission = "logging"

                if self.caught_giraffe:
                    closest_storage_house.food_storage += 20
                    self.caught_giraffe = False

                if self.caught_wood:
                    closest_storage_house.wood_storage += 20
                    self.caught_wood = False

                '''
                if closest_storage_house.food_storage > closest_storage_house.food_storage_max:
                    closest_storage_house.food_storage = closest_storage_house.food_storage_max
                    self.mission = "build_storage"
                elif closest_storage_house.wood_storage > closest_storage_house.wood_storage_max:
                    closest_storage_house.wood_storage = closest_storage_house.wood_storage
                    self.mission = "build_storage"
                '''
        
        '''
        # building new storage house
        if self.mission == "build_storage":
            self.build_storage_timer += 1



            if self.build_storage_timer >= self.time_to_build_storage:
                storage_house = House(self.screen_x, self.screen_y, self.screen, self.human_spawn_pos, first_house=False)
                storage_house_group.add(storage_house)
                print("new house")
                self.mission = "home"
        '''


    
    def eat_from_storage(self, storage_house):
        if self.hunger > 10:
            self.food_proportion = self.hunger
        else:
            self.food_proportion = 5

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
        if self.mission == "logging":
            pygame.draw.line(self.image, (160, 82, 45), (8, 12), (10, 18), 6)  # Axe
        elif self.mission == "hunt":
            pygame.draw.line(self.image, (105, 105, 105), (8, 12), (10, 18), 6)  # Spear

        