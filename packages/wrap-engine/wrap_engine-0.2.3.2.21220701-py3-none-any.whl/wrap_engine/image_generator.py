from wrap_engine import image_modifier
import pygame


class TextImageGenerator(image_modifier.ImageModifier):

    def __init__(self, text, font_name="Arial", font_size=20,
                 bold=False, italic=False, underline=False,
                 text_color=(0, 0, 0),
                 back_color=None, pos=None, angle=None, callback=None):

        image_modifier.ImageModifier.__init__(self, None, callback)

        if pos is not None:
            pos = [*pos]

        # create font
        font_data = {
            'name': font_name,
            'size': font_size,
            'bold': bold,
            'italic': italic,
            'underline': underline
        }
        font = TextImageGenerator._get_font_by_data(font_data)

        self._modification_data = {
            "font_data": font_data,
            'font': font,
            'text': text,
            "text_color": text_color,
            "back_color": back_color,
            "pos": pos,
            "angle": angle
        }

        super().update()

    @staticmethod
    def _get_font_by_data(font_options):
        font = pygame.font.SysFont(font_options["name"], font_options["size"], font_options["bold"],
                                   font_options["italic"])
        font.set_underline(font_options["underline"])
        font.set_bold(font_options["bold"])
        font.set_italic(font_options["italic"])
        return font

    @staticmethod
    def _modify(orig_image, orig_pos, orig_angle, modification_data):
        if 'font' in modification_data:
            f = modification_data['font']
        else:
            f = TextImageGenerator._get_font_by_data(modification_data['font_data'])

        im = f.render(modification_data['text'], True, modification_data['text_color'], modification_data['back_color'])

        # prepare pos
        pos = modification_data["pos"] if "pos" in modification_data else None
        if pos is None:
            w, h = im.get_size()
            pos = [w / 2, h / 2]
        else:
            pos = [*pos]

        # prepare angle
        if "angle" in modification_data and modification_data['angle'] is not None:
            angle = modification_data["angle"]
        else:
            angle = 0

        return [im, pos, angle]

    def get_font_name(self):
        return self._modification_data['font_data']['name']

    def get_font_size(self):
        return self._modification_data['font_data']['size']

    def get_font_bold(self):
        return self._modification_data['font_data']['bold']

    def get_font_italic(self):
        return self._modification_data['font_data']['italic']

    def get_font_underline(self):
        return self._modification_data['font_data']['underline']

    def get_text(self):
        return self._modification_data['text']

    def get_text_color(self):
        return self._modification_data['text_color']

    def get_back_color(self):
        return self._modification_data['back_color']

    def get_pos(self):
        res = self._modification_data['pos']
        if res is not None:
            res = [*res]
        return res

    def get_angle(self):
        return self._modification_data['angle']

    def change_data(self, text=None, font_name=None, font_size=None,
                    bold=None, italic=None, underline=None,
                    text_color=None):

        recreate_font = False
        if font_name is not None:
            self._modification_data['font_data']['name'] = font_name
            recreate_font = True

        if font_size is not None:
            self._modification_data['font_data']['size'] = font_size
            recreate_font = True

        if bold is not None:
            self._modification_data['font_data']['bold'] = bold
            recreate_font = True

        if italic is not None:
            self._modification_data['font_data']['italic'] = italic
            recreate_font = True

        if recreate_font:
            self._modification_data['font'] = TextImageGenerator._get_font_by_data(self._modification_data['font_data'])

        if underline is not None:
            self._modification_data['font_data']['underline'] = underline
            self._modification_data['font'].set_underline(underline)

        if text is not None:
            self._modification_data['text'] = text

        if text_color is not None:
            self._modification_data['text_color'] = [*text_color]

        super().update()

    def change_back_color(self, color):
        if color is not None:
            color = [*color]
        self._modification_data['back_color'] = color
        super().update()

    def change_pos(self, pos):
        if pos is not None:
            pos = [*pos]
        self._modification_data['pos'] = pos
        super().update()

    def change_angle(self, angle):
        self._modification_data['angle'] = angle
        super().update()
