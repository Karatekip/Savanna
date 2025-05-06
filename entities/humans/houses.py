import pygame
import random

class House(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen, human_spawn_pos, first_house):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        
        self.width, self.height = (40, 40) if first_house else (30, 30)
        self.roof_height = 10
        self.image = pygame.Surface((self.width, self.height + self.roof_height), pygame.SRCALPHA)
        self.color = (120, 80, 40) if first_house else (random.randint(90,150), random.randint(60,100), random.randint(30,60))
        pygame.draw.rect(self.image, self.color, (0, self.roof_height, self.width, self.height))
        self.roof_color = (150, 0, 0) if first_house else (random.randint(100,180), 0, 0)
        pygame.draw.polygon(
            self.image, self.roof_color, 
            [(0, self.roof_height), (self.width // 2, 0), (self.width, self.roof_height)]
        )
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
