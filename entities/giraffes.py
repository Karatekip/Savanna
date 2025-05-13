import pygame
import random

class Giraffe(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        self.generation = 1
        self.speed = random.uniform(0.5, 1.5)
        self.neck_length = random.randint(3, 10)
        self.hunger = 0
        self.color = (255, 191, 125)
        self.width, self.height = 20, 20
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.age = 0
        self.max_age = random.randint(2000, 15000)

        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(50, self.screen_x - 50),
            random.randint(50, self.screen_y - 50)
        )
        self.font = pygame.font.SysFont(None, 14)

        self.change_direction_timer = 0
        self.change_direction_interval = random.randint(30, 300)  # Change direction every 2 seconds

        self.x_dir = random.choice([-1, 0, 1]) * self.speed
        self.y_dir = random.choice([-1, 0, 1]) * self.speed
        
        self.max_breed_attempts = 3  # Maximum attempts to breed
        self.breed_attempts = 0
        self.breed_timer = 0 #random.randint(0, 3000)
        self.breed_timer_interval = random.randint(500, 1000)  # Time before next breed attempt

        self.eat_nead = random.randint(10, 30)  # Hunger level needed to eat
        self.comment = f"New baby giraffe"

        self.sick = False

    
    def update(self, tree_group, giraffe_group, season):
        #movement
        self.change_direction_timer += 1
        if self.change_direction_timer > self.change_direction_interval:
            self.x_dir = random.uniform(-self.speed, self.speed)
            self.y_dir = random.uniform(-self.speed, self.speed)
            self.change_direction_timer = 0
            #print("changing direction")
        else:
            self.x_dir = self.x_dir
            self.y_dir = self.y_dir
        
        self.rect.x += self.x_dir
        self.rect.y += self.y_dir
        
        #self.rect.clamp_ip(pygame.Rect(0, 0, self.screen_x, self.screen_y))
        if self.rect.left < 0 or self.rect.right > self.screen_x:
            self.x_dir = -self.x_dir
            self.rect.x += self.x_dir

        if self.rect.top < 0 or self.rect.bottom > self.screen_y:
            self.y_dir = -self.y_dir
            self.rect.y += self.y_dir

        #hunger
        self.hunger += 0.015
        if self.hunger > 100:
            self.die("Giraffe died of hunger.")

        #eating tree
        for tree in list(tree_group):
            if self.rect.colliderect(tree.rect) and self.sick == False:
                if self.neck_length >= tree.height and self.hunger >= self.eat_nead:
                    tree_group.remove(tree)
                    self.hunger -= 50
                    if self.hunger < 0:
                        self.hunger = 0

        #breeding
        if season == "rain":
            self.breed_timer += 2
        else:
            self.breed_timer += 0.7
        for stranger_giraffe in list(giraffe_group):
            if self.breed_timer > self.breed_timer_interval and stranger_giraffe.breed_timer > self.breed_timer_interval and self.breed_attempts < self.max_breed_attempts:
                if self.rect.colliderect(stranger_giraffe.rect) and stranger_giraffe != self:
                    baby_giraffe = Giraffe(self.screen_x, self.screen_y, self.screen)
                    baby_giraffe.rect.center = self.rect.center
                    baby_giraffe.neck_length = (self.neck_length + stranger_giraffe.neck_length) / 2
                    baby_giraffe.hunger = (self.hunger + stranger_giraffe.hunger) / 2
                    baby_giraffe.speed = (self.speed + stranger_giraffe.speed) / 2
                    baby_giraffe.generation = max(self.generation, stranger_giraffe.generation) + 1
                    giraffe_group.add(baby_giraffe)
                    print(f"New baby giraffe at {baby_giraffe.rect.center} with neck length {baby_giraffe.neck_length}")
                    self.breed_timer = 0
                    stranger_giraffe.breed_timer = 0
                    self.breed_attempts += 1
                    break
        
        # age
        self.age += 1
        if self.age > self.max_age:
            self.die("Giraffe has died of old age.")
            print(f"Giraffe at {self.rect.center} has died of old age.")

    def set_color(self, new_color):
        self.color = new_color
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))


    def die(self, comment=None):
        self.kill()
        if comment:
            self.comment = comment
            print(comment)
        else:
            self.comment = "Giraffe has died."
            print(f"Giraffe at {self.rect.center} has died.")

    def draw(self):
        # Draw the giraffe
        pygame.draw.rect(self.screen, (255, 255, 100), (self.rect.centerx - 5, self.rect.centery - self.neck_length * 5, 10, self.neck_length * 5))
        self.screen.blit(self.image, self.rect)
        
        # Draw the giraffe's neck
        self.neck_color = (int(255 - (25 * self.neck_length)), int(25 * self.neck_length), 0)
        self.neck_surface = pygame.Surface((self.width / 3, self.height / 3), pygame.SRCALPHA)
        self.neck_surface.fill(self.neck_color)
        self.neck_rect = self.neck_surface.get_rect(bottomleft=self.rect.bottomleft)
        self.screen.blit(self.neck_surface, self.neck_rect)

        # Draw the giraffe's speed
        self.speed_color = (int(255 - (170 * self.speed)), int(170 * self.speed), 0)
        self.speed_surface = pygame.Surface((self.width / 3, self.height / 3), pygame.SRCALPHA)
        self.speed_surface.fill(self.speed_color)
        self.speed_rect = self.speed_surface.get_rect(midbottom=self.rect.midbottom)
        self.screen.blit(self.speed_surface, self.speed_rect)

        # Draw the giraffe's hungryness
        self.hunger_color = (int(2 * self.hunger), int(255 - (2 * self.hunger)), 0)
        self.hunger_surface = pygame.Surface((self.width / 3, self.height / 3), pygame.SRCALPHA)
        self.hunger_surface.fill(self.hunger_color)
        self.hunger_rect = self.hunger_surface.get_rect(bottomright=self.rect.bottomright)
        self.screen.blit(self.hunger_surface, self.hunger_rect)

        

        # draw stats under the giraffe
        stats = f"N:{int(self.neck_length)} S:{round(self.speed,1)} H:{int(self.hunger)}"
        text_surface = self.font.render(stats, True, (255, 255, 255))
        text_rect = text_surface.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 2))
        #text_rect.midtop = (self.rect.centerx, self.rect.bottom + 2)
        self.screen.blit(text_surface, text_rect)

        
        # Draw the generation
        generation_text = self.font.render(f"Gen: {self.generation}", True, (255, 255, 255))
        generation_rect = generation_text.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 11))
        self.screen.blit(generation_text, generation_rect)

        # Draw the age
        age_text = self.font.render(f"Age: {int(self.age / 600)} / {int(self.max_age / 600)}", True, (255, 255, 255))
        age_rect = age_text.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 22))
        self.screen.blit(age_text, age_rect)
