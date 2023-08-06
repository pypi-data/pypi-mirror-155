class Sprite_type_costume():
    def get_image(self):
        assert False, "method is abstract and must be overriden"

    def get_pos(self):
        assert False, "method is abstract and must be overriden"

    def get_angle(self):
        assert False, "method is abstract and must be overriden"


class Sprite_type_costume_image(Sprite_type_costume):
    def __init__(self, image, pos, angle):
        self._image = image.copy()
        self._pos = [*pos]
        self._angle = angle

    def get_image(self):
        return self._image.copy()

    def get_pos(self):
        return [*self._pos]

    def get_angle(self):
        return self._angle
