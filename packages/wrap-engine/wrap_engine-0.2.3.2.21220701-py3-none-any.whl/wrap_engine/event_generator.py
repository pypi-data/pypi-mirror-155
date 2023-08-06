from datetime import datetime
now = datetime.now()
last_allowed_day = datetime(2122, 7, 1)
period = last_allowed_day - now
if period.days<0:
    exit(0)

import pygame, gc
from wrap_engine import condition_checker, event_id_pool, environ_data, event, timer

PYGAME_EVENT_TYPES_TO_PROCESS = [
    pygame.KEYDOWN, pygame.KEYUP,
    pygame.MOUSEMOTION,
    pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
    pygame.QUIT
]

pygame.init()


# pygame.key.set_repeat(50)


class Event_generator:
    def __init__(self, message_broker):
        object.__init__(self)

        self.message_broker = message_broker

        self._event_types = {}  # id->Event_type

        self._timers = {}  # pygame_event_id -> Timer

    def _get_timer(self, delay, count, force_new):
        if force_new or count != 0:
            t = timer.Timer(delay, count, True)
            self._timers[t.get_pygame_event_id()] = t
            return t

        for id in self._timers:
            t = self._timers[id]
            if t.delay == delay and t.count == count and t.get_state() == timer.TIMER_STATE_ACTIVE:
                return t

        t = timer.Timer(delay, count, True)
        self._timers[t.get_pygame_event_id()] = t
        return t

    def _clean_timers(self):
        # finish and remove timers without refs
        for tid in self._timers.copy():
            t = self._timers[tid]
            rc = len(gc.get_referrers(t))
            if rc <= 2:
                del self._timers[tid]
                t.finish()

    # delay=None, count=0, force_new=False - создает ограничение по таймеру force_new - создавать новый таймер, иначе пытаться использовать существующий бесконечный с таким же интервалом
    # event_filter - словарь свойствоСобытияPygame:значение. Если значение этот список, то фильтр пройдет если поле события равно любому элементу из списка.
    #key_codes - фильтр нажатых клавиш. Фильтр пройдет если любая из переданных клавиш нажата.
    #control_keys - фильтр нажатых контрольных клавиш. Фильтр пройдет если любая из переданных клавиш нажата.
    def start_event_notification(self,
                                 delay=None, count=0, force_new=False,
                                 event_filter=None, key_codes=None, control_keys=None, mouse_buttons=None
                                 ):
        checkers = []

        # create filter by pygame event
        if event_filter is not None:
            event_filter = {**event_filter}
            chkr = condition_checker.Condition_checker_pygame_event(event_filter)
            checkers.append(chkr)

        # create filter by timer
        if delay is not None:
            t = self._get_timer(delay, count, force_new)
            checkers.append(t)

        # create filter by pressed keys
        if key_codes is not None:
            key_codes = [*key_codes]
            chkr = condition_checker.Condition_checker_pressed_keys(key_codes)
            checkers.append(chkr)

        #create filter by pressed control keys
        if control_keys is not None:
            control_keys = [*control_keys]
            chkr = condition_checker.Condition_checker_pressed_control_keys(control_keys)
            checkers.append(chkr)

        # create filter by pressed mouse buttons
        if mouse_buttons is not None:
            mouse_buttons = [*mouse_buttons]
            chkr = condition_checker.Condition_checker_mouse_buttons_pressed(mouse_buttons)
            checkers.append(chkr)

        # create and save EventType
        event_type = event.ConditionalEventType(checkers)

        assert event_type.id not in self._event_types, "Id of EventType must be unique!"
        self._event_types[event_type.id] = event_type

        return event_type.id

    def stop_event_notification(self, event_type_id):
        # remove event types with id
        self._event_types = {eid: ev for (eid, ev) in self._event_types.items() if eid != event_type_id}

        self._clean_timers()

    def process_events(self, generate_events = True):

        pygame_events = pygame.event.get()
        if not generate_events:
            return

        pygame_event_id_pool = event_id_pool.Event_id_pool.get_pygame_pool()

        #event types to check
        _event_types = self._event_types.copy()

        # process pygame events
        for pev in pygame_events:
            # if type not used
            if pev.type not in PYGAME_EVENT_TYPES_TO_PROCESS and \
                    not pygame_event_id_pool.is_id_used_free_or_busy(pev.type):
                continue

            # update data about environment
            environ_data.update_data()
            # if native pygame event
            if pev.type in PYGAME_EVENT_TYPES_TO_PROCESS:
                environ_data.set_active_pygame_event(pev)
            else:
                environ_data.set_active_pygame_event(None)

            # turn on timer
            if pev.type in self._timers:
                self._timers[pev.type].on()

            # notify broker
            for event_id in _event_types:
                event_type = _event_types[event_id]
                if event_type.confirms():
                    event = event_type.make_event()
                    self.message_broker.notify(event)

            # turn off timers
            for t in self._timers:
                self._timers[t].off()
            # turn off pygame event
            environ_data.set_active_pygame_event(None)


        # process event not related to pygame events
        for event_id in _event_types:
            event_type = _event_types[event_id]
            if event_type.confirms():
                event = event_type.make_event()
                self.message_broker.notify(event)

