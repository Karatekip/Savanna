import pygame
import random
from entities.giraffe import Giraffe
from world.seasons import Season

class Lion(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen, player_controlled=False):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        self.player_controlled = player_controlled
        self.generation = 1
        if self.player_controlled:
            self.speed = 3
        else:
            self.speed = random.uniform(1, 2)

        self.hunger = 0
        self.hunger_speed = random.uniform(0.001, 0.004)
        if self.player_controlled:
            self.color = (0, 0, 255)
        else:
            self.color =  (255, 100, 0)
        self.width, self.height = 20, 20
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.polygon(self.image, self.color, [(self.width // 2, 0), (0, self.height), (self.width, self.height)])

        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(50, self.screen_x - 50),
            random.randint(50, self.screen_y - 50)
        )
        self.font = pygame.font.SysFont(None, 14)

        self.change_direction_timer = 0
        self.change_direction_interval = random.randint(30, 100)

        self.x_dir = random.choice([-1, 1]) * self.speed
        self.y_dir = random.choice([-1, 1]) * self.speed

        self.eat_nead = random.randint(0, 500)

        self.max_breed_attempts = 3
        self.breed_attempts = 0
        self.breed_timer = random.randint(0, 3000)
        self.breed_timer_interval = random.randint(500, 3000)

        self.comment = "New baby lion"

    def update(self, giraffe_group, lion_group, season):
        #movement
        keys = pygame.key.get_pressed()

        if self.player_controlled:
            speed = self.speed
            self.x_dir, self.y_dir = 0, 0
            if keys[pygame.K_LEFT]:
                self.x_dir = -speed
            if keys[pygame.K_RIGHT]:
                self.x_dir = speed
            if keys[pygame.K_UP]:
                self.y_dir = -speed
            if keys[pygame.K_DOWN]:
                self.y_dir = speed
        else:
            lion_amount = 0
            x_mid = 0
            y_mid = 0
            for lion in lion_group:
                lion_amount += 1
                x_mid += lion.rect.centerx
                y_mid += lion.rect.centery
            x_mid /= lion_amount
            y_mid /= lion_amount


            self.change_direction_timer += 1
            if random.randint(0, 100) < 9:
                if self.change_direction_timer > self.change_direction_interval:
                    self.x_dir = random.choice([-1, 0, 1]) * self.speed
                    self.y_dir = random.choice([-1, 0, 1]) * self.speed
                    self.change_direction_timer = 0
                else:
                    self.x_dir = self.x_dir
                    self.y_dir = self.y_dir
            else:
                if self.change_direction_timer > self.change_direction_interval:

                    if self.rect.centerx < x_mid:
                        self.x_dir = self.speed
                    elif self.rect.centerx > x_mid:
                        self.x_dir = -self.speed
                    else:
                        self.x_dir = 0

                    if self.rect.centery < y_mid:
                        self.y_dir = self.speed
                    elif self.rect.centery > y_mid:
                        self.y_dir = -self.speed
                    else:
                        self.y_dir = 0
                else:
                    self.x_dir = self.x_dir
                    self.y_dir = self.y_dir

        if self.hunger >= 10 or self.player_controlled:
            self.rect.x += self.x_dir
            self.rect.y += self.y_dir

        
        if self.rect.left < 0 or self.rect.right > self.screen_x:
            self.x_dir = -self.x_dir
            self.rect.x += self.x_dir

        if self.rect.top < 0 or self.rect.bottom > self.screen_y:
            self.y_dir = -self.y_dir
            self.rect.y += self.y_dir

        #hunger
        self.hunger += 0.015
        if self.hunger > 100:
            self.die("Lion died of hunger.")
            print(f"Lion at {self.rect.center} has died of hunger.")

        #eating giraffe
        self.hunger += self.hunger_speed
        for giraffe in list(giraffe_group):
            if self.rect.colliderect(giraffe.rect):
                if self.hunger >= 30 or self.player_controlled:
                    giraffe.die()
                    print("Lion has eaten a giraffe!")  
                    self.hunger -= 40
                    if self.hunger < 0:
                        self.hunger = 0

        

        # breeding
        if season == "rain":
            self.breed_timer += 1
        '''
        if self.player_controlled:
            self.breed_timer = self.breed_timer_interval + 1
            self.breed_attempts = 0
        '''
        for stranger_lion in list(lion_group):
            if self.breed_timer > self.breed_timer_interval and stranger_lion.breed_timer > self.breed_timer_interval and self.breed_attempts < self.max_breed_attempts:
                if self.rect.colliderect(stranger_lion.rect) and stranger_lion != self:
                    baby_lion = Lion(self.screen_x, self.screen_y, self.screen)
                    baby_lion.rect.center = self.rect.center
                    baby_lion.hunger = (self.hunger + stranger_lion.hunger) / 2
                    baby_lion.speed = (self.speed + stranger_lion.speed) / 2
                    baby_lion.hunger_speed = (self.hunger_speed + stranger_lion.hunger_speed) / 2
                    baby_lion.generation = max(self.generation, stranger_lion.generation) + 1
                    lion_group.add(baby_lion)
                    print(f"New baby lion at {baby_lion.rect.center} with speed {baby_lion.speed}")
                    self.comment = "New baby lion"
                    self.breed_timer = 0
                    stranger_lion.breed_timer = 0
                    self.breed_attempts += 1
                    break

    def die(self, comment=None):
        self.kill()
        if comment:
            print(comment)
        else:
            comment = "Lion has died."
            print("Lion has died.")
    def draw(self):
        # Draw the lion
        self.screen.blit(self.image, self.rect)

        # Draw the speed
        self.speed_color = (int(255 - (63 * self.speed)), int(63 * self.speed), 0)
        self.speed_surf = pygame.Surface((self.width / 3, self.height / 3), pygame.SRCALPHA)
        self.speed_surf.fill(self.speed_color)
        self.speed_rect = self.speed_surf.get_rect(bottomleft=self.rect.bottomleft)
        self.screen.blit(self.speed_surf, self.speed_rect)

        #Draw the hunger speed
        self.hunger_speed_color = (int(63750 * self.hunger_speed), int(255 - (63750 * self.hunger_speed)), 0)
        self.hunger_speed_surf = pygame.Surface((self.width / 3, self.height / 3), pygame.SRCALPHA)
        self.hunger_speed_surf.fill(self.hunger_speed_color)
        self.hunger_speed_rect = self.hunger_speed_surf.get_rect(midbottom=self.rect.midbottom)
        self.screen.blit(self.hunger_speed_surf, self.hunger_speed_rect)

        # Draw the hunger
        self.hunger_color = (int(2 * self.hunger), int(255 - (2 * self.hunger)), 0)
        self.hunger_surf = pygame.Surface((self.width / 3, self.height / 3), pygame.SRCALPHA)
        self.hunger_surf.fill(self.hunger_color)
        self.hunger_rect = self.hunger_surf.get_rect(bottomright=self.rect.bottomright)
        self.screen.blit(self.hunger_surf, self.hunger_rect)

        stats = f"S:{self.speed:.2f} HS: {self.hunger_speed:.3f} H:{self.hunger:.2f}"
        text_surf = self.font.render(stats, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 2))
        self.screen.blit(text_surf, text_rect)

        # Draw the generation
        generation_text = self.font.render(f"Gen: {self.generation}", True, (255, 255, 255))
        generation_rect = generation_text.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 11))
        self.screen.blit(generation_text, generation_rect)
        # Draw the breed attempts