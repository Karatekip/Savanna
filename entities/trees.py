#trees.py
import pygame
import random

class Tree(pygame.sprite.Sprite):
    def __init__(self, screen_x, screen_y, screen, x=None, y=None):
        super().__init__()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        self.height = random.randint(1, 5)
        self.color = (0, 51 * self.height, 0)
        self.diameter = 20

        self.image = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.diameter // 2, self.diameter // 2), self.diameter // 2)
        self.rect = self.image.get_rect()

        # Position
        if x is None or y is None:
            self.rect.center = (random.randint(0, screen_x), random.randint(0, screen_y))
        else:
            self.rect.center = (x, y)

        self.growth_timer = 0
        self.growth_delay = random.randint(500, 2500)


    def update(self, tree_group):
        self.growth_timer += 1
        if self.growth_timer > self.growth_delay:
            self.try_grow(tree_group)
            self.growth_timer = 0
        


    def try_grow(self, tree_group):
        # Try a few random positions around the parent
        for _ in range(5):
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.randint(25, 40)
            new_x = self.rect.centerx + int(distance * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
            new_y = self.rect.centery + int(distance * pygame.math.Vector2(1, 0).rotate_rad(angle).y)

            # Create a temporary rect for the new tree
            temp_rect = pygame.Rect(0, 0, self.diameter, self.diameter)
            temp_rect.center = (new_x, new_y)

            # Ensure it's within screen and doesn't collide with others
            if 0 <= new_x <= self.screen_x and 0 <= new_y <= self.screen_y:
                if not any(temp_rect.colliderect(tree.rect) for tree in tree_group):
                    new_tree = Tree(self.screen_x, self.screen_y, self.screen, new_x, new_y)
                    #new_tree.height = max(1, min(5, int(self.height + random.choice([-1, 0, 1]))))
                    new_tree.height = int(self.height + random.choice([-1, 0, 1]))
                    if new_tree.height > 5:
                        new_tree.height = 5
                    elif new_tree.height < 1:
                        new_tree.height = 1
                    new_tree.color = (0, int(51 * new_tree.height), 0)
                    pygame.draw.circle(new_tree.image, new_tree.color, (new_tree.diameter // 2, new_tree.diameter // 2), new_tree.diameter // 2)
                    #print(f"color old {self.color} new {new_tree.color}")
                    tree_group.add(new_tree)
                    break

    def draw(self):
        # Draw the tree
        self.screen.blit(self.image, self.rect)
        # Draw the height of the tree above it
        #font = pygame.font.SysFont(None, 14)
        #height_text = font.render(f"Height: {self.height}", True, (255, 255, 255))
        #screen.blit(height_text, (self.rect.x, self.rect.y - 20))