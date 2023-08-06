import os
import pygame
from wrap_engine import sprite


class World:
    def __init__(self):
        object.__init__(self)

        self.sprite_manager = None

        self._window = None

        self._bkg_color = [0, 0, 0]
        self._bkg_pic = None
        self._bkg = pygame.Surface([1000, 1000])

        self._icon_pic = pygame.Surface([32, 32])

        self._cap = ""

    def _is_world_created(self):
        return self._window is not None

    def _update_bkg(self):
        if self._window is None: return

        w, h = self._window.get_size()
        fon = pygame.Surface([w, h])
        fon.fill(self._bkg_color)

        if self._bkg_pic is not None:
            fon.blit(self._bkg_pic, [0, 0])

        self._bkg = fon
        self._window.blit(self._bkg, [0, 0])

    def _update_icon(self):
        if self._window is None: return
        pygame.display.set_icon(self._icon_pic)

    def _update_caption(self):
        if self._window is None: return
        pygame.display.set_caption(self._cap)

    def _update_sprite_manager(self):
        if self.sprite_manager is None and self._window is not None:
            self.sprite_manager = sprite.Sprite_manager(self._window, self._bkg)

        if self.sprite_manager is not None:
            self.sprite_manager._set_background(self._bkg)


    def create_world(self, width, height, start_pos_x:int = None, start_pos_y:int = None):

        #set start position if done
        if start_pos_x is not None and start_pos_y is not None and self._window is None:
            os.environ['SDL_VIDEO_WINDOW_POS'] = str(start_pos_x)+", "+str(start_pos_y)

        self._window = pygame.display.set_mode([width, height], 0)

        self._update_bkg()
        self._update_sprite_manager()
        self._update_caption()
        self._update_icon()

    def change_world(self, width, height):
        self.create_world(width, height)

    def create_world_fullscreen(self):
        self._window = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)

        self._update_bkg()
        self._update_sprite_manager()
        self._update_caption()
        self._update_icon()

    def change_world_fullscreen(self):
        self.create_world_fullscreen()

    def get_world_size(self):
        if not self._is_world_created():
            raise Exception()

        return self._window.get_size()

    def get_world_fullscreen(self):
        if not self._is_world_created():
            raise Exception()

        return bool(self._window.get_flags() & pygame.FULLSCREEN)

    def set_world_background_color(self, color):
        self._bkg_color = [*color]
        self._update_bkg()
        self._update_sprite_manager()

    def set_world_background_image(self, path_to_file, fill=False):
        if path_to_file is None:
            self._bkg_pic = None
        else:
            self._bkg_pic = pygame.image.load(path_to_file)

        self._update_bkg()
        self._update_sprite_manager()

    def set_icon(self, path_to_file):
        pic = pygame.image.load(path_to_file)
        self._icon_pic = pygame.transform.scale(pic, [32, 32])
        self._update_icon()

    def set_caption(self, cap):
        self._cap = str(cap)
        self._update_caption()

    def get_caption(self):
        return self._cap

    def update(self):
        if not self._is_world_created():
            return

        if self.sprite_manager is not None:
            self.sprite_manager.update_sprites()

        pygame.display.flip()
