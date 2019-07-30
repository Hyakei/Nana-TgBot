import importlib

from nana import SETTINGSBOT_LOAD, SETTINGSBOT_NOLOAD, log

def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob
    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [basename(f)[:-3] for f in mod_paths if isfile(f)
                   and f.endswith(".py")
                   and not f.endswith('__init__.py')]

    if SETTINGSBOT_LOAD or SETTINGSBOT_NOLOAD:
        to_Load = SETTINGSBOT_LOAD
        if to_Load:
            if not all(any(mod == module_name for module_name in all_modules) for mod in to_Load):
                log.error("Invalid Module name for settings bot!")
                quit(1)

        else:
            to_Load = all_modules

        if SETTINGSBOT_NOLOAD:
            log.info("Not loaded: {}".format(SETTINGSBOT_NOLOAD))
            return [item for item in to_Load if item not in SETTINGSBOT_NOLOAD]

        return to_Load

    return all_modules


ALL_SETTINGS = sorted(__list_all_modules())
log.info("Settings bot module loaded: %s", str(ALL_SETTINGS))
__all__ = ALL_SETTINGS + ["ALL_SETTINGS"]
