import pygame
from wrap_engine import sprite, image_generator


class Sprite_text(sprite.Sprite_image, image_generator.TextImageGenerator):
    def __init__(self, x, y, visible, text, font_name="Arial", font_size=20,
                 bold=False, italic=False, underline=False,
                 text_color=(0, 0, 0),
                 back_color=None, pos=None, angle=None):

        im = pygame.Surface([1, 1])
        sprite.Sprite_image.__init__(self, im, x, y, visible, 0, 0, 0)

        image_generator.TextImageGenerator.__init__(self, text, font_name, font_size, bold, italic, underline,
                                                    text_color, back_color,
                                                    pos, angle, self._on_text_image_change)

    def _on_text_image_change(self):
        self.change_base_image(self.get_modified_image(), self.get_modified_pos(), self.get_modified_angle())

