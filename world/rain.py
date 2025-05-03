import pygame
import random

class Raindrop(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        self.image = pygame.Surface((2, 10))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.screen_x)
        self.rect.y = random.randint(-300, -10)
        self.end_y = random.randint(self.screen_y // 2, self.screen_y)
        self.speed = random.uniform(2, 5)
        self.splash_animation = False
        self.splash_timer = 0
        self.splash_pos = (0, 0)

    def reset(self):
        #splash
        self.splash_pos = (self.rect.x, self.rect.y)
        self.splash_animation = True
        self.splash_timer = 0

        #reset
        self.rect.x = random.randint(0, self.screen_x)
        self.rect.y = random.randint(-300, -10)
        self.end_x = random.randint(0, self.screen_x)
        self.end_y = random.randint(self.screen_y // 2, self.screen_y)

        

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > self.end_y:
            self.reset()

        if self.splash_animation:
            self.splash_timer += 1
            #here draw circle at fall place that fades with time
            if self.splash_timer > 300:
                self.splash_timer = 0
                self.splash_animation = False

    def draw_splash(self):
        if self.splash_animation:
            alpha = max(0, 255 - (self.splash_timer * 8))  # fades out
            radius = 5 + self.splash_timer  # expands
            splash_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(splash_surface, (0, 0, 255, alpha), (radius, radius), radius)
            self.screen.blit(splash_surface, (self.splash_pos[0] - radius, self.splash_pos[1] - radius))


class Rain(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        self.raindrops = pygame.sprite.Group()
        self.num_drops = 500
        for _ in range(self.num_drops):
            raindrop = Raindrop(self.screen_x, self.screen_y, self.screen)
            self.raindrops.add(raindrop)

    def update(self, rain_strength):
        active_drops = int(self.num_drops * rain_strength)
        #print(f"Active drops: {active_drops}")
        for i, raindrop in enumerate(self.raindrops):
            if i >= active_drops:
                raindrop.reset()
            else:
                raindrop.speed = random.uniform(2, 5) * rain_strength * 4
                raindrop.update()
        
        for raindrop in self.raindrops:
            if raindrop.speed < 1:
                raindrop.reset()
        
        for raindrop in self.raindrops:
            raindrop.draw_splash()
            

    def draw(self, screen):
        for raindrop in self.raindrops:
            screen.blit(raindrop.image, raindrop.rect)

    
