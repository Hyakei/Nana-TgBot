import importlib

from nana import Load, NoLoad, log

def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob
    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [basename(f)[:-3] for f in mod_paths if isfile(f)
                   and f.endswith(".py")
                   and not f.endswith('__init__.py')]

    if Load or NoLoad:
        to_Load = Load
        if to_Load:
            if not all(any(mod == module_name for module_name in all_modules) for mod in to_Load):
                log.error("Nama Muatan Pesan Tidak Valid. Berhenti.")
                quit(1)

        else:
            to_Load = all_modules

        if NoLoad:
            log.info("Tidak Memuat: {}".format(NoLoad))
            return [item for item in to_Load if item not in NoLoad]

        return to_Load

    return all_modules


ALL_MODULES = sorted(__list_all_modules())
log.info("Modul yang dijalankan: %s", str(ALL_MODULES))
__all__ = ALL_MODULES + ["ALL_MODULES"]
