import gettext
import os

TRANSL_DOMAIN = "wrap_engine"

#directory with translations
_translation_dir = None

#global translation function
_translate_func = None

def set_lang(lang=""):
    global _translate_func
    os.environ['LANG'] = lang
    _update_translation_func()

def set_translation_directory(dir):
    global _translation_dir
    _translation_dir=dir
    _update_translation_func()

def _update_translation_func():
    global _translate_func
    _tr = gettext.translation(domain=TRANSL_DOMAIN, localedir=_translation_dir, fallback=True)
    _translate_func = _tr.gettext


def translator(text):
    return _translate_func(text)

_update_translation_func()