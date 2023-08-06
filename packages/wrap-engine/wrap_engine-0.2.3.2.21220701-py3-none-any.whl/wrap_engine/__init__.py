import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

#we can't translate here because user had not chance to set language yet
#from wrap_engine.transl import translator as _

from datetime import datetime
now = datetime.now()
last_allowed_day = datetime(2122, 7, 1)
period = last_allowed_day - now
if period.days<0:
    exit(0)


from wrap_engine import app, world, event_generator, message_broker, object_manager, sprite_type, sprite_of_type

