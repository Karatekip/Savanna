import pygame
from world.simulation import Simulation
#test

def main():
    pygame.init()
    
    pygame.display.set_caption("Animal Simulation")
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_x, screen_y = screen.get_size()
    #screen = pygame.display.set_mode((screen_x, screen_y))
    sim = Simulation(screen, screen_x, screen_y)
    sim.run()
    pygame.quit()


if __name__ == "__main__":
    main()
