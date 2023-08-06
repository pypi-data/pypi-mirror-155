import pygame
from wrap_engine import event_id_pool, condition_checker, environ_data, pygame_utils


class Event():
    def __init__(self, typeid, data):
        object.__init__(self)

        self.type = typeid

        for key in data:
            setattr(self, key, data[key])


class EventType(condition_checker.Condition_checker):
    def __init__(self):
        condition_checker.Condition_checker.__init__(self)

        self.id = event_id_pool.Event_id_pool.get_usual_pool().get_id()

    def confirms(self):
        assert False, "Method confirms() of class EventType is abstract and must be overriden"
        return False

    def make_event(self):
        assert False, "Method make_event() of class EventType is abstract and must be overriden"
        return None


class ConditionalEventType(EventType):
    def __init__(self, checkers):
        EventType.__init__(self)
        self._checkers = [*checkers]

    def confirms(self):
        for ch in self._checkers:
            if not ch.confirms():
                return False

        return True

    def make_event(self):
        assert self.confirms(), "EventType must confirm to generate event"

        event_data = {}

        # collect checkers classes
        types = []
        for ch in self._checkers:
            types.append(ch.__class__)

        # collect pygame keys pressed data
        event_data['keys'] = pygame_utils.key_list_of_pressed_keys(
            environ_data.get_data()['keys_pressed']
        )

        #collect pygame control keys pressed data
        event_data['control_keys'] = pygame_utils.control_key_list_of_pressed_keys(
            environ_data.get_data()['modifier_keys_pressed']
        )

        #collect pygame mouse buttons pressed data
        event_data['mouse_buttons'] = pygame_utils.mouse_button_list_of_pressed_buttons(
            environ_data.get_data()['mouse_buttons_pressed']
        )

        #collect pygame mouse position
        event_data['pos'] = pygame.mouse.get_pos()

        # collect pygame event data
        # it must override general event attributes if duplicates exists.
        # for example - pos on mouse move and general pos
        if condition_checker.Condition_checker_pygame_event in types and \
                environ_data.is_active_pygame_event_set():

            pygame_event = environ_data.get_active_pygame_event()
            pygame_event_data = vars(pygame_event)
            for attr in pygame_event_data:
                event_data[attr] = pygame_event_data[attr]

        #repeat some data in more simple way for those who dont know how to use lists yet
        event_data['pos_x'] = event_data['pos'][0]
        event_data['pos_y'] = event_data['pos'][1]

        return Event(self.id, event_data)
