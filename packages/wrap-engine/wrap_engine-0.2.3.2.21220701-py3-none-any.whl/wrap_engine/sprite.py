import pygame
from wrap_engine import image_modifier, math_utils


class Sprite_manager():
    def __init__(self, window, bkg):
        object.__init__(self)

        self._window = window
        self._bkg = bkg

        self._group = pygame.sprite.LayeredDirty()
        self._group.clear(None, self._bkg)

    def _set_background(self, bkg):
        if self._bkg is bkg: return

        self._bkg = bkg
        self._group.clear(None, self._bkg)
        self._group.repaint_rect(self._window.get_rect())

    def update_sprites(self):
        self._group.draw(self._window)

    def add_image_sprite(self, sprite):
        self._group.add(sprite)

    def remove_image_sprite(self, sprite):
        self._group.remove(sprite)

    def sprites_collide(self, sprite1, sprite2):
        if not sprite1.rect.colliderect(sprite2.rect):
            return False

        res = pygame.sprite.collide_mask(sprite1, sprite2)
        if not res:
            return False

        res = [*res]
        res[0] += sprite1.rect.left
        res[1] += sprite1.rect.top
        return res

    # returns [index, [x, y]]
    def sprite_collide_any(self, sprite, sprite_list):
        gr = pygame.sprite.Group(sprite_list)
        res = pygame.sprite.spritecollideany(sprite, gr, pygame.sprite.collide_mask)

        return res

    # returns list of collided sprites
    def sprite_collide_all(self, sprite, sprite_list):
        gr = pygame.sprite.Group(sprite_list)
        res = pygame.sprite.spritecollide(sprite, gr, False, pygame.sprite.collide_mask)
        return res


class Sprite_image(pygame.sprite.DirtySprite):
    def __init__(self, image, x, y, visible=True, posx=0, posy=0, base_angle=0):
        pygame.sprite.DirtySprite.__init__(self)

        self._pos = [x, y]

        # original image
        self._orig_modifier = image_modifier.ImageSource(image, [posx, posy], -base_angle)
        self._size_modifier = image_modifier.ImageResizer(self._orig_modifier, None, None, None)
        self._flipper_angle = image_modifier.ImageFlipper(self._size_modifier, None)
        self._rotator = image_modifier.ImageRotator(self._flipper_angle, None)

        self._final_modifier = self._rotator
        self._final_modifier.change_callback(self._update_sprite_data)
        self._final_modifier.update()

        self.visible = visible

    def _update_rect_from_pos(self):
        # calc correct rect position
        posx, posy = self._final_modifier.get_modified_pos()
        self.rect.topleft = [self._pos[0] - posx, self._pos[1] - posy]
        self.dirty = 1

    def _update_pos_from_rect(self):
        posx, posy = self._final_modifier.get_modified_pos()
        self._pos[0] = self.rect.x + posx
        self._pos[1] = self.rect.y + posy
        self.dirty = 1

    def _update_sprite_data(self):
        if not hasattr(self, '_final_modifier'):
            return

        # get changed image
        self.image = self._final_modifier.get_modified_image()
        self.rect = self.image.get_rect()
        self.dirty = 1

        # update mask
        self.mask = pygame.mask.from_surface(self.image, 0)

        # calc correct rect position
        self._update_rect_from_pos()

    @staticmethod
    def normalize_angle(angle):
        if angle > 360:
            angle %= 360
        if angle < -360:
            angle %= -360
        if angle > 180:
            angle -= 360
        if angle <= -180:
            angle += 360

        return angle

    def change_image(self, image, apply_proc_size=True):
        if apply_proc_size is not None:
            self._size_modifier.change_size_priority(not apply_proc_size)

        self._orig_modifier.change_image(image)

        self._update_inactive_size_from_reality()

    def change_pos_offset(self, posx, posy):
        self._orig_modifier.change_pos([posx, posy])

    def change_base_angle(self, angle):
        self._orig_modifier.change_angle(-angle)

    def change_base_image(self, image=None, pos=None, angle=None, apply_proc_size=True):
        if angle is not None:
            angle = -angle

        if apply_proc_size is not None:
            self._size_modifier.change_size_priority(not apply_proc_size)

        self._orig_modifier.change_all(image, pos, angle)

        self._update_inactive_size_from_reality()

    def get_original_width(self):
        oi = self._orig_modifier.get_modified_image()
        return oi.get_width()

    def get_original_height(self):
        oi = self._orig_modifier.get_modified_image()
        return oi.get_height()

    def get_original_size(self):
        oi = self._orig_modifier.get_modified_image()
        return oi.get_size()

    def get_real_width(self):
        return self.image.get_width()

    def get_real_height(self):
        return self.image.get_height()

    def get_real_size(self):
        return self.image.get_size()

    def _update_size_pix_from_reality(self):
        w_pix, h_pix = self._size_modifier.get_modified_image().get_size()
        self._size_modifier.change_size_pix(w_pix, h_pix)

    def _update_size_proc_from_reality(self):
        w_pix, h_pix = self._size_modifier.get_modified_image().get_size()
        w_orig, h_orig = self._orig_modifier.get_modified_image().get_size()

        w_proc = 100 * w_pix / w_orig
        h_proc = 100 * h_pix / h_orig
        self._size_modifier.change_size_proc(w_proc, h_proc)

    def _set_size_pix(self, width, height):
        self._size_modifier.change_size_priority(True)
        self._size_modifier.change_size_pix(width, height)
        self._update_size_proc_from_reality()

    def _set_size_proc(self, width, height):
        self._size_modifier.change_size_priority(False)
        self._size_modifier.change_size_proc(width, height)
        self._update_size_pix_from_reality()

    def _update_inactive_size_from_reality(self):
        if self._size_modifier.is_size_priority_pix():
            self._update_size_proc_from_reality()
        else:
            self._update_size_pix_from_reality()

    # methods get_applied_width_pix/height/size returns sizes which image should be modified to
    # None means no modification should be applied
    def get_applied_width_pix(self):
        return self._size_modifier.get_size_pix()[0]

    def get_applied_height_pix(self):
        return self._size_modifier.get_size_pix()[1]

    def get_applied_size_pix(self):
        return self._size_modifier.get_size_pix()

    # methods get_width_pix/height/size returns sizes of image after resize but before rotatino and next modifications
    # None value never returned
    def get_width_pix(self):
        return self._size_modifier.get_modified_image().get_width()

    def get_height_pix(self):
        return self._size_modifier.get_modified_image().get_height()

    def get_size_pix(self):
        return self._size_modifier.get_modified_image().get_size()

    def set_original_size(self):
        self._set_size_pix(None, None)

    def change_width_pix(self, width):
        h = self._size_modifier.get_size_pix()[1]
        self._set_size_pix(width, h)

    def change_height_pix(self, height):
        w = self._size_modifier.get_size_pix()[0]
        self._set_size_pix(w, height)

    def change_size_pix(self, width, height):
        self._set_size_pix(width, height)

    def change_width_pix_proportionally(self, width, from_modified=False):
        if from_modified:
            cur_w, cur_h = self._size_modifier.get_modified_image().get_size()
        else:
            oi = self._orig_modifier.get_modified_image()
            cur_w, cur_h = oi.get_size()

        width, height = math_utils.get_sizes_proportionally(cur_w, cur_h, width, None)
        self._set_size_pix(width, height)

    def change_height_pix_proportionally(self, height, from_modified=False):
        if from_modified:
            cur_w, cur_h = self._size_modifier.get_modified_image().get_size()
        else:
            oi = self._orig_modifier.get_modified_image()
            cur_w, cur_h = oi.get_size()

        width, height = math_utils.get_sizes_proportionally(cur_w, cur_h, None, height)
        self._set_size_pix(width, height)

    def get_width_proc(self):
        return self._size_modifier.get_size_proc()[0]

    def get_height_proc(self):
        return self._size_modifier.get_size_proc()[1]

    def get_size_proc(self):
        return self._size_modifier.get_size_proc()

    def change_width_proc(self, width):
        h = self._size_modifier.get_size_proc()[1]

        self._set_size_proc(width, h)

    def change_height_proc(self, height):
        w = self._size_modifier.get_size_proc()[0]
        self._set_size_proc(w, height)

    def change_size_proc(self, width, height):
        self._set_size_proc(width, height)

    def change_size_by_proc(self, proc):
        orig_w, orig_h = self._size_modifier.get_size_proc()
        orig_w = orig_w if orig_w is not None else 100
        orig_h = orig_h if orig_h is not None else 100

        width = proc * orig_w / 100
        height = proc * orig_h / 100
        self._set_size_proc(width, height)

    def get_flipx_reverse(self):
        return self._flipper_angle.get_flipx()

    def get_flipy_reverse(self):
        return self._flipper_angle.get_flipy()

    def set_flipx_reverse(self, flipx):
        curr_flip = self._flipper_angle.get_flipx()

        self._flipper_angle.set_flipx(flipx, True)

        if curr_flip != flipx:
            self._rotator.reflect_flip_once(True, False)

    def set_flipy_reverse(self, flipy):
        curr_flip_y = self._flipper_angle.get_flipy()

        self._flipper_angle.set_flipy(flipy, True)

        if curr_flip_y != flipy:
            self._rotator.reflect_flip_once(False, True)

    def get_start_angle(self):
        return Sprite_image.normalize_angle(-self._orig_modifier.get_angle())

    def set_angle_modification(self, angle):
        self._rotator.change_angle(-angle)

    def get_angle_modification(self):
        return Sprite_image.normalize_angle(-self._rotator.get_angle())

    def get_final_angle(self):
        return Sprite_image.normalize_angle(-self._final_modifier.get_modified_angle())

    def get_sprite_pos(self):
        return [*self._pos]

    def move_sprite_to(self, x, y):
        self._pos[0] = x
        self._pos[1] = y
        self._update_rect_from_pos()

    def move_sprite_by(self, dx, dy):
        self._pos[0] += dx
        self._pos[1] += dy
        self._update_rect_from_pos()

    def get_sprite_rect(self):
        return pygame.Rect(self.rect)

    def set_left_to(self, left):
        self.rect.left = left
        self._update_pos_from_rect()

    def set_right_to(self, right):
        self.rect.right = right
        self._update_pos_from_rect()

    def set_top_to(self, top):
        self.rect.top = top
        self._update_pos_from_rect()

    def set_bottom_to(self, bottom):
        self.rect.bottom = bottom
        self._update_pos_from_rect()

    def set_centerx_to(self, centerx):
        self.rect.centerx = centerx
        self._update_pos_from_rect()

    def set_centery_to(self, centery):
        self.rect.centery = centery
        self._update_pos_from_rect()

    def get_visible(self):
        return self.visible

    def set_visible(self, visible):
        self.visible = visible
        self.dirty = 1

    def calc_point_by_angle_and_distance(self, angle, distance):
        res = math_utils.get_point_by_angle([*self._pos], -angle, distance)
        return [int(res[0]), int(res[1])]

    def calc_angle_by_point(self, point):
        """Returns current angle if point is same as current position"""
        # can't move to same point
        if point[0] == self._pos[0] and point[1] == self._pos[1]:
            return None

        return Sprite_image.normalize_angle(-math_utils.get_angle_by_point(self._pos, point))

    def calc_angle_modification_by_angle(self, angle_to_look_to):
        angle_to_look_to = -angle_to_look_to

        orig_angle = self._flipper_angle.get_modified_angle()
        res = angle_to_look_to - orig_angle
        return -res

    ######### Methods below are sintax sugar for user.
    #           Only user methods must be called in body of these functions.
    def move_sprite_at_angle(self, angle, distance):
        res = self.calc_point_by_angle_and_distance(angle, distance)
        self.move_sprite_to(res[0], res[1])

    def move_sprite_to_angle(self, distance):
        an = self.get_final_angle()
        res = self.calc_point_by_angle_and_distance(an, distance)
        self.move_sprite_to(res[0], res[1])

    def move_sprite_to_point(self, point, distance):
        an = self.calc_angle_by_point(point)
        if an is None:
            return

        res = self.calc_point_by_angle_and_distance(an, distance)
        self.move_sprite_to(res[0], res[1])

    def rotate_to_angle(self, angle_to_look_to):
        angle_modif = self.calc_angle_modification_by_angle(angle_to_look_to)
        self.set_angle_modification(angle_modif)

    def rotate_to_point(self, point):
        angle_to_look_to = self.calc_angle_by_point(point)
        if angle_to_look_to is None:
            return

        angle_modif = self.calc_angle_modification_by_angle(angle_to_look_to)

        self.set_angle_modification(angle_modif)

    ######### Collision methods
    def collide_point_rect(self, x, y):
        return self.rect.collidepoint(x, y)

    def collide_point_mask(self, x, y):
        if not self.rect.collidepoint(x, y):
            return False
        x -= self.rect.x
        y -= self.rect.y
        return bool(self.mask.get_at([x, y]))
