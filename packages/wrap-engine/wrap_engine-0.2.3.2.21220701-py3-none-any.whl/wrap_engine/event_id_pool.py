from wrap_engine.id_generator import Pygame_event_id_generator, Usual_id_generator


class Event_id_pool():
    def __init__(self, use_pygame=False):
        object.__init__(self)

        if use_pygame:
            self._generator = Pygame_event_id_generator()
        else:
            self._generator = Usual_id_generator()

        self._free_ids = []
        self._busy_ids = []

    def get_id(self):
        if len(self._free_ids) == 0:
            self._free_ids.append(self._generator.get_id())

        id = self._free_ids.pop(0)

        assert id not in self._busy_ids, "Event id is already in use!"
        self._busy_ids.append(id)
        return id

    def free_id(self, id):
        self._busy_ids = [el for el in self._busy_ids if el != id]
        if id not in self._free_ids:
            self._free_ids.append(id)

    def is_id_used_free_or_busy(self, id):
        return id in self._free_ids or \
               id in self._busy_ids

    @classmethod
    def get_usual_pool(cls):
        if not hasattr(cls, "_usual_pool"):
            cls._usual_pool = cls(False)

        return cls._usual_pool

    @classmethod
    def get_pygame_pool(cls):
        if not hasattr(cls, "_pygame_pool"):
            cls._pygame_pool = cls(True)

        return cls._pygame_pool


