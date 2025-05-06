import pygame
from world.rain import Rain

class Season():
    def __init__(self, screen_x, screen_y, screen):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen = screen
        self.calc_season = "dry_start"
        self.season = "dry"
        self.duration = 2000
        self.progression = 0
        self.dry_season_color = (237, 201, 175)
        self.rain_season_color = (100, 149, 237)
        self.start_color = self.dry_season_color
        self.end_color = self.rain_season_color
        self.current_color = self.dry_season_color
        self.rain = Rain(self.screen_x, self.screen_y, self.screen)

    def update(self):
        self.progression += 1

        if self.progression != 0 and (self.duration / self.progression) <= 2:
            if self.calc_season == "dry_start":
                self.season = "rain"
            elif self.calc_season == "rain_start":
                self.season = "dry"

        
        # Background color
        self.color_progression = self.progression / self.duration
        if self.color_progression > 1:
            self.color_progression = 1
        if self.color_progression < 0:
            self.color_progression = 0
        self.color_progression = self.color_progression ** 2
        self.current_color = (
            int(self.start_color[0] + (self.end_color[0] - self.start_color[0]) * self.color_progression),
            int(self.start_color[1] + (self.end_color[1] - self.start_color[1]) * self.color_progression),
            int(self.start_color[2] + (self.end_color[2] - self.start_color[2]) * self.color_progression)
        )

        if self.progression > self.duration:
            if self.calc_season == "dry_start":
                self.calc_season = "rain_start"
                self.start_color = self.rain_season_color
                self.end_color = self.dry_season_color
            else:
                self.calc_season = "dry_start"
                self.start_color = self.dry_season_color
                self.end_color = self.rain_season_color
            self.progression = 0

        # Rain

        progress_ratio = self.progression / self.duration
        progress_ratio = min(1.0, max(0.0, progress_ratio))

        if self.calc_season == "dry_start":
            rain_strength = (progress_ratio ** 6)
        elif self.calc_season == "rain_start":
            rain_strength = (1 - progress_ratio) ** 6
        self.rain.update(rain_strength)


    def draw(self, screen):
        screen.fill(self.current_color)
        self.rain.draw(screen)