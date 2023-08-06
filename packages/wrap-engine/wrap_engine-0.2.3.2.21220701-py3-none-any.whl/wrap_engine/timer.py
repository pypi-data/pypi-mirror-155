import pygame
from wrap_engine import condition_checker as cc, event_id_pool

TIMER_STATE_PAUSE = 0
TIMER_STATE_ACTIVE = 1
TIMER_STATE_FINISHED = 2


class Timer(cc.Condition_checker):
    def __init__(self, delay, count, start):
        cc.Condition_checker.__init__(self)

        assert delay > 0, "Timer delay must be greater than 0"
        assert count >= 0, "Timer count must be 0 or greater"

        self._pygame_event_id = event_id_pool.Event_id_pool.get_pygame_pool().get_id()

        self.delay = delay
        self.count = count
        self._real_count = 0

        self._state = TIMER_STATE_PAUSE
        self._active_is_on = False

        if start:
            self.start()

    def start(self):
        assert self._state != TIMER_STATE_FINISHED, "Finished timer can't be started!"
        if self._state == TIMER_STATE_ACTIVE: return

        self._state = TIMER_STATE_ACTIVE
        pygame.time.set_timer(self._pygame_event_id, self.delay)

    def pause(self):
        assert self._state != TIMER_STATE_FINISHED, "Finished timer can't be paused!"
        if self._state == TIMER_STATE_PAUSE: return

        self._state = TIMER_STATE_PAUSE
        pygame.time.set_timer(self._pygame_event_id, 0)

    def finish(self):
        if self._state == TIMER_STATE_ACTIVE:
            pygame.time.set_timer(self._pygame_event_id, 0)

        self._state = TIMER_STATE_FINISHED
        event_id_pool.Event_id_pool.get_pygame_pool().free_id(self._pygame_event_id)

    def get_state(self):
        return self._state

    def get_pygame_event_id(self):
        return self._pygame_event_id

    def on(self):
        if self._state in [TIMER_STATE_FINISHED, TIMER_STATE_PAUSE]:
            self._active_is_on = False
            return

        self._real_count += 1
        self._active_is_on = True

    def off(self):
        self._active_is_on = False
        if self.count != 0 and self._real_count >= self.count:
            self.finish()

    def confirms(self):
        return self._active_is_on
