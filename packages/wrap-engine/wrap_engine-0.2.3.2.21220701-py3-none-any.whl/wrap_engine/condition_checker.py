from wrap_engine import environ_data


class Condition_checker():
    def confirms(self):
        assert False, "Condition_checker class confirms() method is abstract and must be overriden"
        return False


class Condition_checker_pygame_event(Condition_checker):


    #pygame event filter:
    #{pygame_event_attr: pygame_event_attr_val, ...} or
    #{pygame_event_attr: [pygame_event_attr_val], ...}
    #if attr not exists in event - filter not passed
    #if attr value not equals event value - filter not passed OR
    # if attr value not in event value list - filter not passed
    #
    # example:
    #{'type': pygame.KEYDOWN, 'key': [pygame.K_UP, pygame.K_w]}
    # filter only will work on keydown of key Up or 'w'
    def __init__(self, pygame_event_filter):
        Condition_checker.__init__(self)
        self._filter = pygame_event_filter

    def confirms(self):

        if not environ_data.is_active_pygame_event_set():
            return False

        event = environ_data.get_active_pygame_event()
        for attr in self._filter:
            filter_val = self._filter[attr]

            if not hasattr(event, attr): return False

            event_val = getattr(event, attr)

            # check if filter is iterable and val not in sequence
            if hasattr(filter_val, "__iter__") and event_val not in filter_val:
                return False
            # check if filter is simple value and not equal event value
            if (not hasattr(filter_val, "__iter__")) and event_val != filter_val:
                return False

        return True


class Condition_checker_pressed_keys(Condition_checker):
    def __init__(self, pressed_keys_list):
        Condition_checker.__init__(self)
        self._pressed_keys_filter = pressed_keys_list

    def confirms(self):
        # get list of pressed keys
        pressed_keys = environ_data.get_data()['keys_pressed']

        # check allowed keys among pressed
        keys_len = len(pressed_keys)
        for f in self._pressed_keys_filter:
            # check if key exists

            #we should not check existence of key. Because in pygame 2.0.1 key number
            #could be very big like 37473865234.
            #No problem with that because pressed_keys is not list but special iterable object.
            # if f < 0 or f >= keys_len:
            #     continue

            # check if key pressed
            if pressed_keys[f]: return True

        return False


class Condition_checker_pressed_control_keys(Condition_checker):
    def __init__(self, pressed_keys_list):
        Condition_checker.__init__(self)
        self._pressed_keys_filter = pressed_keys_list

    def confirms(self):
        # get bitmask of pressed control keys
        pressed_keys_bitmask = environ_data.get_data()['modifier_keys_pressed']
        for k in self._pressed_keys_filter:
            if k & pressed_keys_bitmask:
                return True

        return False

class Condition_checker_mouse_buttons_pressed(Condition_checker):
    def __init__(self, _pressed_buttons_list):
        Condition_checker.__init__(self)
        self._pressed_buttons_filter = _pressed_buttons_list

    def confirms(self):
        # get list of pressed mouse buttons
        pressed_buttons = environ_data.get_data()['mouse_buttons_pressed']
        for k in self._pressed_buttons_filter:
            if k<0 or k>=len(pressed_buttons):
                continue
            if pressed_buttons[k]: return True
        return False