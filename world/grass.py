import pygame
import random
import math
from world.seasons import Season

class Wind(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen

        self.width, self.height = 1, random.randint(100, screen_y // 2)
        self.color = (255, 255, 255)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(2, self.screen_x), random.randint(0, self.screen_y))
        self.wind_speed = random.randint(2, 4)


    def update(self):
        if self.rect.centerx < 0:
            self.reset()
        else:
            self.rect.centerx -= self.wind_speed
    def reset(self):
        self.height = random.randint(100, self.screen_y // 2)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen_x, random.randint(0, self.screen_y))


    def draw(self):
        #self.screen.blit(self.image, self.rect.topleft)
        pass


class Grass(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen, x=None, y=None):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        self.width, self.height = 10, 10
        self.base_color = (100, 180, 90)
        self.color = tuple(min(255, max(0, c + random.randint(-20, 20))) for c in self.base_color)
        self.fix_color = self.color
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        self.rect = self.image.get_rect()

        # Position
        if x is None or y is None:
            self.rect.center = (random.randint(0, screen_x), random.randint(0, screen_y))
        else:
            self.rect.center = (x, y)

        self.growth_timer = 0
        self.growth_delay = random.randint(500, 2500)


        # Wind
        self.brightness_timer = 0

    def update(self, grass_group, season, tree_group, house_group, wind_group):
        # growing
        if season.season == "dry":
            self.growth_timer += 1
        else:
            self.growth_timer += 3
        if self.growth_timer > self.growth_delay:
            self.try_grow(grass_group, tree_group, house_group)
            self.growth_timer = 0
        #self.growth_timer += 20

        # wind
        if pygame.sprite.spritecollideany(self, wind_group):
            self.color = tuple(min(255, c + 20) for c in self.fix_color)
        else:
            self.color = self.fix_color

        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))


    def try_grow(self, grass_group, tree_group, house_group):
        for _ in range(4):
            angle = random.choice([0, 90, 180, 270])
            distance = 11

            new_x = self.rect.centerx + int(distance * pygame.math.Vector2(1, 0).rotate(angle).x)
            new_y = self.rect.centery + int(distance * pygame.math.Vector2(1, 0).rotate(angle).y)

            temp_rect = pygame.Rect(0, 0, self.width, self.height)
            temp_rect.center = (new_x, new_y)

            if 0 <= new_x <= self.screen_x and 0 <= new_y <= self.screen_y:
                if not any(temp_rect.colliderect(grass.rect) for grass in grass_group) and not any(temp_rect.colliderect(tree.rect) for tree in tree_group) and not any(temp_rect.colliderect(house.rect) for house in house_group):
                    new_grass = Grass(self.screen_x, self.screen_y, self.screen, new_x, new_y)
                    grass_group.add(new_grass)
                    break

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)