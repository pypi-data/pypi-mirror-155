import os
from wrap_engine import sprite_type as st, sprite_type_costume_holder


class Sprite_type_factory():

    @staticmethod
    def create_sprite_type_from_data_source(name, data_source, preload_data = False):
        all_sprites = [*data_source.get_sprite_types_enumerator()]
        if name not in all_sprites:
            return False

        costumes = data_source.get_sprite_type_costumes_enumerator(name)

        # create sprite and costumes
        sprite_type = st.Sprite_type()
        for costume_id in costumes:
            cost = sprite_type_costume_holder.Sprite_type_costume_loader(data_source, name, costume_id, not preload_data)
            sprite_type.add_costume(costume_id, cost)

        return sprite_type

