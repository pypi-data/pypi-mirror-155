from wrap_engine import sprite
from wrap_engine.transl import translator as _
from wrap_engine import exception as exc


class Sprite_of_type(sprite.Sprite_image):
    def __init__(self, sprite_type, x, y, costume_name=None, visible=True):
        self.sprite_type = sprite_type

        #check that type have any costumes
        if len(self.sprite_type.get_costume_names()) == 0:
            err = _("Sprite type has no costumes")
            raise Exception(err)

        # if no costume - select first
        if costume_name is None:
            costume_name = self.sprite_type.get_costume_names()[0]

        # check costume existence
        if not self.sprite_type.has_costume_name(costume_name):
            err = _("Costume with name {costume_name} not found").format(costume_name=str(costume_name))
            raise Exception(err)

        # set initial costume
        c = self.sprite_type.get_costume_by_name(costume_name)
        self._active_costume_name = costume_name

        pos = c.get_pos()
        sprite.Sprite_image.__init__(self, c.get_image(), x, y, visible, pos[0], pos[1], c.get_angle())

    def _change_costume(self, image, pos_offset, orig_angle, save_moving_angle, apply_proc_size):

        #change angle to guarantee that new costume wil move to same direction as previous
        if save_moving_angle:
            angle_diff = self.get_start_angle() - orig_angle
            if self.get_flipx_reverse():
                angle_diff = -angle_diff
            if self.get_flipy_reverse():
                angle_diff = -angle_diff
            angle_modif = self.get_angle_modification()
            self.set_angle_modification(angle_modif + angle_diff)

        self.change_base_image(image, pos_offset, orig_angle, apply_proc_size)

    def _set_costume_by_name(self, name, save_moving_angle, apply_proc_size):
        # check costume existence
        if not self.sprite_type.has_costume_name(name):
            err = _("Costume with name {costume_name} not found")
            raise exc.WrapEngineExceprion(err.format(costume_name=name))

        c = self.sprite_type.get_costume_by_name(name)
        self._active_costume_name = name
        self._change_costume(c.get_image(), c.get_pos(), c.get_angle(), save_moving_angle, apply_proc_size)

    def set_costume(self, costume_name, save_moving_angle, apply_proc_size=True):
        self._set_costume_by_name(costume_name, save_moving_angle, apply_proc_size)

    def set_costume_by_offset(self, offset, save_moving_angle, apply_proc_size=True):
        # no effect if no costumes or no change
        names = self.sprite_type.get_costume_names()
        cost_count = len(names)
        if cost_count == 0 or offset == 0:
            return

        # correct offset
        if offset > 0:
            offset %= cost_count
        else:
            offset %= -cost_count

        # find current index
        try:
            ind = names.index(self._active_costume_name)
            new_index = ind + offset
        except:
            new_index = 0

        # make sure new index is in range
        if new_index < 0:
            new_index += cost_count
        elif new_index > cost_count - 1:
            new_index -= cost_count

        self._set_costume_by_name(names[new_index], save_moving_angle, apply_proc_size)

    def get_sprite_costume(self):
        return self._active_costume_name
