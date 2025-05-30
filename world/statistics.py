import pygame


class Statistics:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 24)
        self.giraffe_count = 0
        self.giraffe_mid_huger = 0
        self.gireaffe_mid_neck_height = 0
        self.giraffe_mid_speed = 0
        self.giraffe_mid_generation = 0
        self.lion_count = 0
        self.lion_mid_hunger = 0
        self.lion_mid_speed = 0
        self.lion_mid_generation = 0
        self.tree_count = 0
        self.tree_mid_height = 0
        self.human_count = 0
        self.human_mid_hunger = 0
        self.house_count = 0
        self.house_wood = 0
        self.house_food = 0

        self.season_progression = 0
        self.last_comment = None
        
    
    def update(self, giraffe_group, tree_group, lion_group, human_group, house_group, season, tot_food_storage, tot_wood_storage, tot_food_storage_max, tot_wood_storage_max, giraffe_comment=None, lion_comment=None):
        for house in house_group:
            house = house
        # Stats calculation
        self.giraffe_count = len(giraffe_group)
        self.giraffe_mid_huger = sum(giraffe.hunger for giraffe in giraffe_group) / self.giraffe_count if self.giraffe_count > 0 else 0
        self.gireaffe_mid_neck_height = sum(giraffe.neck_length for giraffe in giraffe_group) / self.giraffe_count if self.giraffe_count > 0 else 0
        self.giraffe_mid_speed = sum(giraffe.speed for giraffe in giraffe_group) / self.giraffe_count if self.giraffe_count > 0 else 0
        self.giraffe_mid_generation = sum(giraffe.generation for giraffe in giraffe_group) / self.giraffe_count if self.giraffe_count > 0 else 0
        self.lion_count = len(lion_group)
        self.lion_mid_hunger = sum(lion.hunger for lion in lion_group) / self.lion_count if self.lion_count > 0 else 0
        self.lion_mid_speed = sum(lion.speed for lion in lion_group) / self.lion_count if self.lion_count > 0 else 0
        self.lion_mid_generation = sum(lion.generation for lion in lion_group) / self.lion_count if self.lion_count > 0 else 0
        self.tree_count = len(tree_group)
        self.tree_mid_height = sum(tree.height for tree in tree_group) / self.tree_count if self.tree_count > 0 else 0
        self.human_count = len(human_group)
        self.human_mid_hunger = sum(human.hunger for human in human_group) / self.human_count if self.human_count > 0 else 0
        self.house_count = len(house_group)
        self.house_food = tot_food_storage
        self.house_wood = tot_wood_storage
        self.house_food_max = tot_food_storage_max
        self.house_wood_max = tot_wood_storage_max


        # Season progression
        self.season_progression = season.progression
        self.season_name = season.season
        self.season_duration = season.duration

        # Comments 
        if giraffe_comment:
            self.last_comment = giraffe_comment


    def draw(self):
        giraffe_text = self.font.render(f"Giraffes: {self.giraffe_count}", True, (0, 255, 255))
        giraffe_hunger_text = self.font.render(f"Giraffes Average Hunger: {self.giraffe_mid_huger:.2f}", True, (0, 255, 255))
        giraffe_neck_text = self.font.render(f"Giraffes Average Neck Height: {self.gireaffe_mid_neck_height:.2f}", True, (0, 255, 255))
        giraffe_speed_text = self.font.render(f"Giraffes Average Speed: {self.giraffe_mid_speed:.2f}", True, (0, 255, 255))
        giraffe_generation_text = self.font.render(f"Giraffes Average Generation: {self.giraffe_mid_generation:.2f}", True, (0, 255, 255))
        lion_text = self.font.render(f"Lions: {self.lion_count}", True, (0, 255, 255))
        lion_hunger_text = self.font.render(f"Lions Average Hunger: {self.lion_mid_hunger:.2f}", True, (0, 255, 255))
        lion_speed_text = self.font.render(f"Lions Average Speed: {self.lion_mid_speed:.2f}", True, (0, 255, 255))
        lion_generation_text = self.font.render(f"Lions Average Generation: {self.lion_mid_generation:.2f}", True, (0, 255, 255))
        tree_text = self.font.render(f"Trees: {self.tree_count}", True, (0, 255, 255))
        tree_height_text = self.font.render(f"Trees Height: {self.tree_mid_height:.2f}", True, (0, 255, 255))
        human_text = self.font.render(f"Humans: {self.human_count}", True, (0, 255, 255))
        human_hunger_text = self.font.render(f"Humans Average Hunger: {self.human_mid_hunger:.2f}", True, (0, 255, 255))
        house_text = self.font.render(f"Storage Houses: {self.house_count}", True, (0, 255, 255))
        house_wood_text = self.font.render(f"Storage House Wood: {int(self.house_wood)} / {int(self.house_wood_max)}", True, (0, 255, 255))
        house_food_text = self.font.render(f"Storage House Food: {int(self.house_food)} / {int(self.house_food_max)}", True, (0, 255, 255))

        
        season_progression_text = self.font.render(f"{self.season_name} season progression: {self.season_progression} / {self.season_duration}", True, (0, 255, 255))

        comment_text = self.font.render(f"Comment: {self.last_comment}", True, (0, 255, 255))


        
        self.screen.blit(giraffe_text, (10, 10))
        self.screen.blit(giraffe_hunger_text, (10, 30))
        self.screen.blit(giraffe_neck_text, (10, 50))
        self.screen.blit(giraffe_speed_text, (10, 70))
        self.screen.blit(giraffe_generation_text, (10, 90))
        self.screen.blit(lion_text, (10, 110))
        self.screen.blit(lion_hunger_text, (10, 130))
        self.screen.blit(lion_speed_text, (10, 150))
        self.screen.blit(lion_generation_text, (10, 170))
        self.screen.blit(tree_text, (10, 190))
        self.screen.blit(tree_height_text, (10, 210))
        self.screen.blit(human_text, (10, 230))
        self.screen.blit(human_hunger_text, (10, 250))
        self.screen.blit(house_text, (10, 270))
        self.screen.blit(house_wood_text, (10, 290))
        self.screen.blit(house_food_text, (10, 310))
        
        self.screen.blit(season_progression_text, (10, 330))

        '''
        self.screen.blit(comment_text, (10, 400))
        '''