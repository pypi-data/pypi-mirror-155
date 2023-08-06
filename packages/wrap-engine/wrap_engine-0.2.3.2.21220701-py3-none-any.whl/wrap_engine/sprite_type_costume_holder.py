from wrap_engine import math_utils, image_modifier
from wrap_engine.sprite_type_costume import Sprite_type_costume
from wrap_engine.transl import translator as _


class Sprite_type_costume_loader(Sprite_type_costume):
    def __init__(self, data_source, sprite_type_id, sprite_costume_id, load_later=True):
        self._data_source = data_source
        self.sprite_type_id = sprite_type_id
        self.sprite_costume_id = sprite_costume_id

        self._data_loaded = False
        self._image = None
        self._pos = None
        self._angle = None

        if not load_later:
            self._try_load()

    @staticmethod
    def _prepare_image(orig_image, orig_pos, orig_angle, prepare_data):
        # print(prepare_data)

        # change size
        if ('width' in prepare_data and prepare_data['width'] is not None) or \
                ('height' in prepare_data and prepare_data['height'] is not None):
            w_mod = prepare_data['width'] if 'width' in prepare_data else None
            h_mod = prepare_data['height'] if 'height' in prepare_data else None
            w_orig, h_orig = orig_image.get_size()
            w_mod, h_mod = math_utils.get_sizes_proportionally(w_orig, h_orig, w_mod, h_mod)

            orig_image, orig_pos, orig_angle = image_modifier.ImageResizer.modify(orig_image, orig_pos, orig_angle,
                                                                                  int(w_mod), int(h_mod))

        # remove color
        if 'remove_color' in prepare_data and prepare_data['remove_color']:
            orig_image, orig_pos, orig_angle = image_modifier.ImageColorRemover.modify(orig_image, orig_pos, orig_angle,
                                                                                       prepare_data['remove_color_rgb'],
                                                                                       prepare_data['remove_color_thr'])

        return [orig_image, orig_pos, orig_angle]

    @staticmethod
    def _extract_costume_data(cost_data):
        # extract data
        image = cost_data['image']
        posx = cost_data['posx'] if cost_data['posx'] is not None else image.get_width() / 2
        posy = cost_data['posy'] if cost_data['posy'] is not None else image.get_height() / 2
        pos = [posx, posy]
        angle = cost_data['angle']

        # prepare image
        if 'process' in cost_data:
            image, pos, angle = Sprite_type_costume_loader._prepare_image(image, pos, angle, cost_data['process'])

        return [image, pos, angle]

    def _load_data(self, force_reload=False):
        if self._data_loaded and not force_reload:
            return True

        # try to load costume data. It could be time expensive
        cost_data = self._data_source.get_sprite_type_costume_data(self.sprite_type_id, self.sprite_costume_id)
        if not cost_data:
            return False
        self._costume_data = cost_data

        #extract and save costume data
        self._image, self._pos, self._angle = self._extract_costume_data(cost_data)

        #mark data as loaded
        self._data_loaded = True
        return True

    def _try_load(self):
        if not self._load_data():
            raise Exception(_("Costume loading failed({costume_id})!").format(costume_id=self.sprite_costume_id))

    def get_image(self):
        self._try_load()
        return self._image.copy()

    def get_pos(self):
        self._try_load()
        return [*self._pos]

    def get_angle(self):
        self._try_load()
        return self._angle