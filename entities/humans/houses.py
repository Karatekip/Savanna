import pygame
import random

class House(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen, human_spawn_pos):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        
        self.width, self.height = 50, 50
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.color = (100, 100, 100)
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        self.human_spawn_pos = human_spawn_pos
        self.x_pos, self.y_pos = self.human_spawn_pos
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos, self.y_pos)
        self.food_storage = 300
        self.food_storage_max = 1000

    def update(self):
        print(f"Food storage: {self.food_storage}")

    def draw(self):
        self.screen.blit(self.image, self.rect)
