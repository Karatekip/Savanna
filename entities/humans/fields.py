import pygame
import random

class Field(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__()
        self.screen = screen
        self.width, self.height = 20, 20
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.color_growing = (120, 180, 80)
        self.color_ready = (200, 180, 100)
        self.color = self.color_growing

        self.growth_time = 0
        self.max_growth_time = random.randint(1500,3200)  # ~10 seconds at 60fps
        self.ready = False

    def update(self, season):
        if not self.ready:
            if season == 'rain':
                self.growth_time += 2
            else:
                self.growth_time += 0.1

            if self.growth_time >= self.max_growth_time:
                self.ready = True
                self.color = self.color_ready
        self.image.fill(self.color)

    def draw(self):
        self.screen.blit(self.image, self.rect)
