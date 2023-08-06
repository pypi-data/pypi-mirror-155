import pygame

_data = {
    'active_pygame_event':None,
    'keys_pressed': [],
    'modifier_keys_pressed': 0,
    'mouse_buttons_pressed':[]
}

def update_data():
    _data['keys_pressed'] = pygame.key.get_pressed()
    _data['modifier_keys_pressed'] = pygame.key.get_mods()
    _data['mouse_buttons_pressed'] = pygame.mouse.get_pressed(num_buttons=5)

def get_data():
    return _data

def set_active_pygame_event(pygame_event):
    _data['active_pygame_event'] = pygame_event

def is_active_pygame_event_set():
    return _data['active_pygame_event'] is not None

def get_active_pygame_event():
    return _data['active_pygame_event']