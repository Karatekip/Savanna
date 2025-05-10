import pygame
import random
from world.trees import Tree
from world.grass import Grass
from world.grass import Wind
from entities.giraffe import Giraffe
from entities.lions import Lion
from world.statistics import Statistics
from entities.humans.humans import Human
from entities.humans.houses import House
from entities.humans.fields import Field
from world.seasons import Season
from world.rain import Raindrop
from world.rain import Rain

class Simulation:
    def __init__(self, screen, screen_x, screen_y):
        pygame.init()
        self.screen = screen
        self.screen_x, self.screen_y = screen_x, screen_y
        self.running = True
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.initial_trees = 40
        self.initial_grass = 20
        self.initial_giraffes = 20
        self.initial_lions = 4
        self.initial_humans = 4

        self.season = Season(self.screen_x, self.screen_y, self.screen)

        self.tree_group = pygame.sprite.Group()
        for i in range(self.initial_trees):
            tree = Tree(self.screen_x, self.screen_y, self.screen)
            self.tree_group.add(tree)

        self.grass_group = pygame.sprite.Group()
        for i in range(self.initial_grass):
            grass = Grass(self.screen_x, self.screen_y, self.screen)
            self.grass_group.add(grass)
        self.wind_group = pygame.sprite.Group()
        for i in range(5):
            wind = Wind(self.screen_x, self.screen_y, self.screen)
            self.wind_group.add(wind)



        self.giraffe_group = pygame.sprite.Group()
        for i in range(self.initial_giraffes):
            giraffe = Giraffe(screen_x, screen_y, screen)
            self.giraffe_group.add(giraffe)

        self.lion_group = pygame.sprite.Group()
        for i in range(self.initial_lions):
            lion = Lion(screen_x, screen_y, screen)
            self.lion_group.add(lion)
        
            


        self.human_spawn_x_pos = random.randint(50, screen_x - 50)
        self.human_spawn_y_pos = random.randint(50, screen_y - 50)
        self.human_spawn_pos = (self.human_spawn_x_pos, self.human_spawn_y_pos)

        self.field_group = pygame.sprite.Group()
        for i in range(0):
            field = Field(self.screen_x -20, self.screen_y -20, self.screen)
            self.field_group.add(field)

            
        self.house_group = pygame.sprite.Group()
        house_kind = 'church'
        for i in range(1):
            house = House(self.screen_x, self.screen_y, self.screen, self.human_spawn_pos, house_kind, self.house_group, self.field_group)
            self.house_group.add(house)
        


        self.human_group = pygame.sprite.Group()
        for i in range(self.initial_humans):
            human = Human(screen_x, screen_y, screen, self.human_spawn_pos, self.human_group, self.giraffe_group)
            self.human_group.add(human)

        


        

        self.new_rand_tree_timer = 0

        self.stats = Statistics(self.screen)
        self.player_playing = False

        self.tot_food_storage = 0
        self.tot_food_storage_max = 0
        self.tot_wood_storage = 0
        self.tot_wood_storage_max = 0

        


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    # player lion
                    if not self.player_playing:
                        player_lion = Lion(self.screen_x, self.screen_y, self.screen, player_controlled=True)
                        self.lion_group.add(player_lion)
                        self.player_playing = True
                    else:
                        #remove player lion
                        for lion in self.lion_group:
                            if lion.player_controlled:
                                lion.kill()
                                self.player_playing = False
                                break
                #control fps with + an -
                if event.key == pygame.K_l:
                    self.FPS += 10
                if event.key == pygame.K_j:
                    self.FPS -= 10
                    if self.FPS < 1:
                        self.FPS = 1
                print("FPS: ", self.FPS)

    
    def update(self):
        #season
        self.season.update()

        

        #Trees
        for tree in self.tree_group:
            tree.update(self.tree_group, self.season, self.grass_group, self.house_group)

        #Grass
        for grass in self.grass_group:
            grass.update(self.grass_group, self.season, self.tree_group, self.house_group, self.wind_group)

        for wind_wave in self.wind_group:
            wind_wave.update()


        #Giraffes
        for giraffe in self.giraffe_group:
            giraffe.update(self.tree_group, self.giraffe_group, self.season.season)

        #Lions
        for lion in self.lion_group:
            lion.update(self.giraffe_group, self.lion_group, self.season.season)


        #Storage house
        self.tot_food_storage = 0
        self.tot_wood_storage = 0
        self.tot_food_storage_max = 0
        self.tot_wood_storage_max = 0
        for house in self.house_group:
            self.tot_food_storage += house.food_storage
            self.tot_wood_storage += house.wood_storage
            self.tot_food_storage_max += house.food_storage_max
            self.tot_wood_storage_max += house.wood_storage_max

        # Build one storage house if needed
        if self.tot_wood_storage >= self.tot_wood_storage_max:
            new_house = House(self.screen_x, self.screen_y, self.screen, self.human_spawn_pos, "wood_storage", self.house_group, self.field_group)
            self.house_group.add(new_house)

        elif self.tot_food_storage >= self.tot_food_storage_max:
            new_house = House(self.screen_x, self.screen_y, self.screen, self.human_spawn_pos, "food_storage", self.house_group, self.field_group)
            self.house_group.add(new_house)


        for house in self.house_group:
            house.update(self.tot_food_storage, self.tot_wood_storage, self.tot_food_storage_max, self.tot_wood_storage_max, self.house_group, self.field_group)


        #Humans
        for human in self.human_group:
            human.update(self.tree_group, self.human_group, self.house_group, self.giraffe_group, House, self.tot_food_storage, self.tot_wood_storage, self.tot_food_storage_max, self.tot_wood_storage_max, self.field_group, Field)

        #Fields
        for field in self.field_group:
            field.update(self.season.season)

        
        
        
        #Statistics
        self.stats.update(self.giraffe_group, self.tree_group, self.lion_group, self.human_group, self.house_group, self.season, self.tot_food_storage, self.tot_wood_storage, self.tot_food_storage_max, self.tot_wood_storage_max)

       

        
        
    def draw(self):
        #draw background based on season
        self.season.draw(self.screen)

        
        #grass
        for grass in self.grass_group:
            grass.draw()

        for wind_wave in self.wind_group:
            wind_wave.draw()

        #trees
        for tree in self.tree_group:
            tree.draw()

        #houses
        for house in self.house_group:
            house.draw()

        #giraffes
        for giraffe in self.giraffe_group:
            giraffe.draw()

        #lions
        for lion in self.lion_group:
            lion.draw()

        #fields
        for field in self.field_group:
            field.draw()    

        #humans
        for human in self.human_group:
            human.draw()

        

        '''
        for drop in Rain.raindrops:
            drop.draw()
        '''
        
        

        #statistics
        self.stats.draw()
