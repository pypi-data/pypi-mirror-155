from datetime import datetime
now = datetime.now()
last_allowed_day = datetime(2122, 7, 1)
period = last_allowed_day - now
if period.days<0:
    exit(0)

import pygame, threading

class App:

    def __init__(self, world, event_generator):
        object.__init__(self)

        self.fps = 60
        self._clock = pygame.time.Clock()

        self.world = world
        self.event_generator = event_generator

        self._started = False

    def get_fps(self):
        return self.fps

    def set_fps(self, fps):
        self.fps = fps

    def get_real_fps(self):
        return self._clock.get_fps()

    def do_frame(self, generate_events=True):
        self.event_generator.process_events(generate_events)

        if self.world._is_world_created():
            self.world.update()

    def start(self, on_tick = None):
        if self._started:
            return

        self._started = True

        while True:
            self._clock.tick(self.fps)
            self.do_frame()
            if on_tick is not None:
                on_tick()

