import pygame


class Id_generator():

    def get_id(self):
        assert False, "Method get_id() of class Event_id_generator is abstract and must be overriden!"


class Pygame_event_id_generator(Id_generator):
    def __init__(self):
        Id_generator.__init__(self)
        self._last_used_id = pygame.USEREVENT

    def get_id(self):
        self._last_used_id += 1
        assert self._last_used_id <= pygame.NUMEVENTS, "Pygame event id overload!"
        return self._last_used_id


class Usual_id_generator(Id_generator):
    def __init__(self):
        Id_generator.__init__(self)
        self._last_used_id = -1

    def get_id(self):
        self._last_used_id += 1
        return self._last_used_id