import pygame
import random
import math
class House(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen, human_spawn_pos, house_kind, storage_house_group):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        
        self.width, self.height = (40, 40) if house_kind == 'church' else (30, 30)
        self.roof_height = 10
        self.cross_height = 10
        self.image = pygame.Surface((self.width, self.height + self.roof_height + self.cross_height), pygame.SRCALPHA)
        #self.color = (120, 80, 40) if house_kind == 'church' else (random.randint(90,150), random.randint(60,100), random.randint(30,60))
        if house_kind == 'church':
            self.color = (170, 150, 120)
            self.roof_color = (90, 0, 140)
        elif house_kind == 'wood_storage':
            self.color = (
                random.randint(100, 130),
                random.randint(70, 90),
                random.randint(40, 60)
            )
            self.roof_color = (
                random.randint(90, 120),
                random.randint(30, 50),
                random.randint(0, 20)
            )

        elif house_kind == 'food_storage':
            self.color = (
                random.randint(180, 210),
                random.randint(140, 170),
                random.randint(90, 110)
            )
            self.roof_color = (
                random.randint(150, 180),
                random.randint(80, 100),
                random.randint(60, 80)
            )

        # draw
        if house_kind == 'church':
            # body
            pygame.draw.rect(self.image, self.color, (0, self.roof_height + self.cross_height, self.width, self.height))
            # roof
            pygame.draw.polygon(
                self.image, self.roof_color,
                [(0, self.roof_height + self.cross_height), (self.width // 2, self.cross_height), (self.width, self.roof_height + self.cross_height)]
            )
            # door
            door_width, door_height = self.width // 4, self.height // 2
            door_x = (self.width - door_width) // 2
            door_y = self.height + self.roof_height + self.cross_height - door_height
            pygame.draw.rect(self.image, (60, 30, 0), (door_x, door_y, door_width, door_height))
            # Round window
            pygame.draw.circle(self.image, (200, 200, 230), (self.width // 2, self.roof_height + self.cross_height + 5), 4)
            # cross
            self.heigt_hor_bar = 7
            pygame.draw.line(self.image, (255, 255, 255), (self.width // 2, self.cross_height), (self.width // 2,self.cross_height -10), 2)
            pygame.draw.line(self.image, (255, 255, 255), (self.width // 2 - 3, self.cross_height - self.heigt_hor_bar), (self.width // 2 + 3, self.cross_height - self.heigt_hor_bar), 2)
        elif house_kind == 'wood_storage':
            # body
            pygame.draw.rect(self.image, self.color, (0, self.roof_height, self.width, self.height))
            # Roof
            pygame.draw.polygon(
                self.image, self.roof_color, 
                [(0, self.roof_height), (self.width // 2, 0), (self.width, self.roof_height)]
            )

            # Plank lines
            for i in range(5, self.width, 5):
                pygame.draw.line(self.image, (80, 60, 30), (i, self.roof_height), (i, self.height + self.roof_height), 1)

            # Axe symbol
            pygame.draw.line(self.image, (100, 100, 100), (5, self.height), (10, self.height - 10), 2)
            pygame.draw.line(self.image, (150, 70, 20), (10, self.height - 10), (12, self.height - 8), 4)
        elif house_kind == 'food_storage':
            pygame.draw.rect(self.image, self.color, (0, self.roof_height, self.width, self.height))

            # Roof with rounded feel (2 triangles for curve)
            pygame.draw.polygon(
                self.image, self.roof_color, 
                [(0, self.roof_height), (self.width // 3, 0), (self.width // 2, 2), (2 * self.width // 3, 0), (self.width, self.roof_height)]
            )

            # Grain sacks (circles)
            pygame.draw.circle(self.image, (240, 220, 130), (self.width // 3, self.height + self.roof_height - 5), 4)
            pygame.draw.circle(self.image, (240, 220, 130), (2 * self.width // 3, self.height + self.roof_height - 5), 4)

            # Straw lines
            for i in range(0, self.width, 6):
                pygame.draw.line(self.image, (200, 200, 100), (i, self.roof_height + 10), (i + 2, self.height + self.roof_height - 5), 1)

        else:
            pygame.draw.rect(self.image, self.color, (0, self.roof_height, self.width, self.height))
            pygame.draw.polygon(
                self.image, self.roof_color, 
                [(0, self.roof_height), (self.width // 2, 0), (self.width, self.roof_height)]
           )
            

        self.human_spawn_pos = human_spawn_pos
        self.storage_house_group = storage_house_group
        if house_kind == 'church':
            self.x_pos, self.y_pos = self.human_spawn_pos
        elif house_kind == 'wood_storage':
            self.x_pos, self.y_pos = self.get_spawn_near(human_spawn_pos, self.storage_house_group)
        elif house_kind == 'food_storage':
            self.x_pos, self.y_pos = self.get_spawn_near(human_spawn_pos, self.storage_house_group)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos, self.y_pos)
        if house_kind == 'church':
            self.food_storage = 0
            self.food_storage_max = 30
            self.wood_storage = 0
            self.wood_storage_max = 30
        elif house_kind == 'food_storage':
            self.food_storage = 0
            self.food_storage_max = 30
            self.wood_storage = 0
            self.wood_storage_max = 0
        elif house_kind == 'wood_storage':
            self.food_storage = 0
            self.food_storage_max = 0
            self.wood_storage = 0
            self.wood_storage_max = 100


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

                # Check for overlaps and if in screen
                if 0 <= new_x <= self.screen_x and 0 <= new_y <= self.screen_y:
                    if not any(h.rect.colliderect(test_rect) for h in existing_houses):
                        return (new_x, new_y)

        return None

    def update(self, tot_food_storage, tot_wood_storage, tot_food_storage_max, tot_wood_storage_max, storage_house_group):
        if tot_wood_storage >= tot_wood_storage_max:
            house_kind = "wood_storage"
            new_storage_house = House(self.screen_x, self.screen_y, self.screen, self.human_spawn_pos, house_kind, storage_house_group)
            storage_house_group.add(new_storage_house)
        if tot_food_storage >= tot_food_storage_max:
            house_kind = "food_storage"
            new_storage_house = House(self.screen_x, self.screen_y, self.screen, self.human_spawn_pos, house_kind, storage_house_group)
            storage_house_group.add(new_storage_house)
        

    def draw(self):
        self.screen.blit(self.image, self.rect)