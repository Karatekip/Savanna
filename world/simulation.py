import pygame
import random
from world.trees import Tree
from entities.giraffe import Giraffe
from entities.lions import Lion
from world.statistics import Statistics
from entities.humans.humans import Human
from entities.humans.houses import House
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
        self.initial_giraffes = 20
        self.initial_lions = 4
        self.initial_humans = 3

        self.season = Season(self.screen_x, self.screen_y, self.screen)


        self.tree_group = pygame.sprite.Group()
        for i in range(self.initial_trees):
            tree = Tree(self.screen_x, self.screen_y, self.screen)
            self.tree_group.add(tree)

        self.giraffe_group = pygame.sprite.Group()
        for i in range(self.initial_giraffes):
            giraffe = Giraffe(screen_x, screen_y, screen)
            self.giraffe_group.add(giraffe)

        self.lion_group = pygame.sprite.Group()
        for i in range(self.initial_lions):
            lion = Lion(screen_x, screen_y, screen)
            self.lion_group.add(lion)
        
        #self.house_group = pygame.sprite.Group()
            


        self.human_spawn_x_pos = random.randint(50, screen_x - 50)
        self.human_spawn_y_pos = random.randint(50, screen_y - 50)
        self.human_spawn_pos = (self.human_spawn_x_pos, self.human_spawn_y_pos)

        #self.storage_house = House(self.screen_x, self.screen_y, self.screen, self.human_spawn_pos)

        self.storage_house_group = pygame.sprite.Group()
        house_kind = 'church'
        for i in range(1):
            storage_house = House(self.screen_x, self.screen_y, self.screen, self.human_spawn_pos, house_kind, self.storage_house_group)
            self.storage_house_group.add(storage_house)
        


        self.human_group = pygame.sprite.Group()
        for i in range(self.initial_humans):
            human = Human(screen_x, screen_y, screen, self.human_spawn_pos)
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
    
    def update(self):
        #season
        self.season.update()

        #Giraffes
        for giraffe in self.giraffe_group:
            giraffe.update(self.tree_group, self.giraffe_group)

        #Trees
        for tree in self.tree_group:
            tree.update(self.tree_group, self.season)

        #Lions
        for lion in self.lion_group:
            lion.update(self.giraffe_group, self.lion_group, self.season.season)


        #Storage house
        self.tot_food_storage = 0
        self.tot_wood_storage = 0
        self.tot_food_storage_max = 0
        self.tot_wood_storage_max = 0
        for storage_house in self.storage_house_group:
            self.tot_food_storage += storage_house.food_storage
            self.tot_wood_storage += storage_house.wood_storage
            self.tot_food_storage_max += storage_house.food_storage_max
            self.tot_wood_storage_max += storage_house.wood_storage_max

        for storage_house in self.storage_house_group:
            storage_house.update(self.tot_food_storage, self.tot_wood_storage, self.tot_food_storage_max, self.tot_wood_storage_max, self.storage_house_group)


        #Humans
        for human in self.human_group:
            human.update(self.tree_group, self.human_group, self.storage_house_group, self.giraffe_group, House, self.tot_food_storage, self.tot_wood_storage, self.tot_food_storage_max, self.tot_wood_storage_max)

        
        
        #Statistics
        self.stats.update(self.giraffe_group, self.tree_group, self.lion_group, self.human_group, self.storage_house_group, self.season, self.tot_food_storage, self.tot_wood_storage, self.tot_food_storage_max, self.tot_wood_storage_max)


        '''
        # New random tree
        self.new_rand_tree_timer += 1
        if self.new_rand_tree_timer > 100:
            self.new_rand_tree = Tree(self.screen_x, self.screen_y)
            self.tree_group.add(self.new_rand_tree)
            self.new_rand_tree_timer = 0
            #print("NEW RAND TREE")
        '''
        
        '''
        self.tot_food_storage = 0
        self.tot_wood_storage = 0
        self.tot_food_storage_max = 0
        self.tot_wood_storage_max = 0
        for storage_house in self.storage_house_group:
            self.tot_food_storage += storage_house.food_storage
            self.tot_wood_storage += storage_house.wood_storage
            self.tot_food_storage_max += storage_house.food_storage_max
            self.tot_wood_storage_max += storage_house.wood_storage_max
        '''


        

        
        
    def draw(self):
        #draw background based on season
        self.season.draw(self.screen)

        #houses
        for storage_house in self.storage_house_group:
            storage_house.draw()
        
        #trees
        for tree in self.tree_group:
            tree.draw()
        #giraffes
        for giraffe in self.giraffe_group:
            giraffe.draw()

        #lions
        for lion in self.lion_group:
            lion.draw()

        

        #humans
        for human in self.human_group:
            human.draw()

        '''
        for drop in Rain.raindrops:
            drop.draw()
        '''
        
        

        #statistics
        self.stats.draw()
