import pygame
import random

class Disease(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.active = False
        self.start_strength = 3
        self.pause = False
        self.pause_timer = 0
        
    def update(self, giraffe_group):
        for giraffe in giraffe_group:
            if giraffe.sick == True:
                self.active = True
                break

        if self.active == False and len(giraffe_group) > 50 and self.pause == False:
            for i, giraffe in enumerate(giraffe_group):
                if i < self.start_strength:
                    giraffe.sick = True
                    self.active = True
                    
        if self.active == True:
            for giraffe in giraffe_group:
                if giraffe.sick == True:
                    giraffe.hunger += 0.04
                    giraffe.set_color((255, 0, 0))
            # infect other giraffes when collition
            for giraffe in giraffe_group:
                if giraffe.sick == True:
                    for other_giraffe in giraffe_group:
                        if giraffe != other_giraffe and giraffe.rect.colliderect(other_giraffe.rect):
                            other_giraffe.sick = True
                            other_giraffe.set_color((255, 0, 0))
                            break
        if self.active == True:
            still_active = False
            for giraffe in giraffe_group:
                if giraffe.sick == True:
                    still_active = True
                    break
            if still_active == False:
                self.active = False
                self.pause = True

        if self.pause == True:
            self.pause_timer += 1
            if self.pause_timer > 500:
                self.pause = False

