import pygame
import random

class House(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen, human_spawn_pos, first_house):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        
        self.width, self.height = 40, 40
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.color = (100, 100, 100)
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        self.human_spawn_pos = human_spawn_pos
        if first_house:
            self.x_pos, self.y_pos = self.human_spawn_pos
        else:
            self.x_pos, self.y_pos = random.randint(0, screen_x), random.randint(0, screen_y)
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos, self.y_pos)
        self.food_storage = 50
        self.food_storage_max = 100
        self.wood_storage = 50
        self.wood_storage_max = 100

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.image, self.rect)
