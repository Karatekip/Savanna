import pygame
import random
import math
class House(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen, human_spawn_pos, first_house, storage_house_group):
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
        self.storage_house_group = storage_house_group
        if first_house:
            self.x_pos, self.y_pos = self.human_spawn_pos
        else:
            
            self.x_pos, self.y_pos = self.get_spawn_near(human_spawn_pos, self.storage_house_group)
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos, self.y_pos)
        self.food_storage = 50
        self.food_storage_max = 150
        self.wood_storage = 50
        self.wood_storage_max = 150

    def get_spawn_near(self, village_center, existing_houses, max_attempts=1000):
        base_radius = 50
        step_radius = 20
        angle_step = 10 

        for radius_multiplier in range(1, 20):  # Try up to radius ~400
            radius = base_radius + step_radius * radius_multiplier

            for _ in range(int(360 / angle_step)):
                angle = random.uniform(0, 360)
                rad = math.radians(angle)
                dx = math.cos(rad) * radius
                dy = math.sin(rad) * radius
                new_x = int(village_center[0] + dx)
                new_y = int(village_center[1] + dy)

                # Create a fake rect to test for collision
                house_width, house_height = 30, 40  # match your house size
                test_rect = pygame.Rect(0, 0, house_width, house_height)
                test_rect.center = (new_x, new_y)

                # Check for overlaps
                if not any(h.rect.colliderect(test_rect) for h in existing_houses):
                    return (new_x, new_y)

        return None

    def update(self, tot_food_storage, tot_wood_storage, tot_food_storage_max, tot_wood_storage_max, storage_house_group):
        if tot_food_storage >= tot_food_storage_max or tot_wood_storage >= tot_wood_storage_max:
            first_house = False
            new_storage_house = House(self.screen_x, self.screen_y, self.screen, self.human_spawn_pos, first_house, storage_house_group)
            storage_house_group.add(new_storage_house)
        

    def draw(self):
        self.screen.blit(self.image, self.rect)