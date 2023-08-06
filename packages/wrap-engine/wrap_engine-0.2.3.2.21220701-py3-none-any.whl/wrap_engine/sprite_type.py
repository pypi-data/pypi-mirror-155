class Sprite_types_manager():
    def __init__(self):
        self._sprite_types = {}  # sprite_type_name: sprite_type

    def get_sprite_type_names(self):
        return [*self._sprite_types.keys()]

    def has_sprite_type_name(self, name):
        return name in self._sprite_types

    def get_sprite_type_by_name(self, name):
        if name in self._sprite_types:
            return self._sprite_types[name]
        return None

    def add_sprite_type(self, sprite_type, name):
        self._sprite_types[name] = sprite_type

    def remove_sprite_type_by_name(self, name):
        if name in self._sprite_types:
            del self._sprite_types[name]


class Sprite_type():
    def __init__(self):
        self._costumes = {}  # name: Sprite_type_costume

    def get_costume_names(self):
        return [*self._costumes.keys()]

    def has_costume_name(self, name):
        return name in self._costumes

    def get_costume_by_name(self, name):
        if name in self._costumes:
            return self._costumes[name]
        return None

    def add_costume(self, name, costume):
        self._costumes[name] = costume

    def remove_costume_by_name(self, name):
        if name in self._costumes:
            del self._costumes[name]
