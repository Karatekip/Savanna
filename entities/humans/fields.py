import pygame
import random

class Field(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__()
        self.screen = screen
        self.width, self.height = 20, 20
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        #draw vertical lines on field
        self.direction = random.choice(['horizontal', 'vertical'])
        self.draw_field()
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
        self.draw_field()

    def draw_field(self):
        if self.direction == 'vertical':
            for line in range(2, self.width, 5):
                pygame.draw.line(self.image, (0, 0, 0), (line, 2), (line, self.height - 2), 1)
        elif self.direction == 'horizontal':
            for line in range(2, self.height, 5):
                pygame.draw.line(self.image, (0, 0, 0), (2, line), (self.width - 2, line), 1)


    def draw(self):
        self.screen.blit(self.image, self.rect)
