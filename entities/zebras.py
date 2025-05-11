import pygame
import random

class Zebra(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen):
        super().__init__()
        self.screen = screen
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.generation = 1
        self.width, self.height = 20, 10
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.color = (255, 255, 255)
        # draw zebra
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(50, screen_x - 50),
            random.randint(50, screen_y - 50)
        )
        self.font = pygame.font.SysFont(None, 14)
        for stripe in range(0, self.width, 5):
            pygame.draw.rect(self.image, (0, 0, 0), (stripe, 0, 2, self.height))
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.speed = random.uniform(0.3, 1.2)
        self.hunger = 0
        self.hunger_speed = random.uniform(0.001, 0.004)
        self.age = 0
        self.max_age = random.randint(2000, 15000)
        self.x_pos, self.y_pos = random.randint(50, screen_x - 50), random.randint(50, screen_y - 50)

    def update(self, grass_group, zebra_group, lion_group, season):
        # hunger
        self.hunger += self.hunger_speed
        # movement
        if self.hunger > 10:
            if len(grass_group) > 10:
                closest_grass = min(grass_group, key=lambda grass: pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(grass.rect.center)))
                target_x, target_y = closest_grass.rect.center
                dx = target_x - self.rect.centerx
                dy = target_y - self.rect.centery
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance > 1:
                    self.x_pos += self.speed * (dx / distance)
                    self.y_pos += self.speed * (dy / distance)
                    self.rect.center = (int(self.x_pos), int(self.y_pos))
                if self.rect.colliderect(closest_grass.rect):
                    self.hunger -= 1
                    closest_grass.kill()
        else:
            #mover randomly
            self.x_pos += random.uniform(-self.speed, self.speed)
            self.y_pos += random.uniform(-self.speed, self.speed)
            self.rect.center = (int(self.x_pos), int(self.y_pos))
            

    def draw(self):
        self.screen.blit(self.image, self.rect)