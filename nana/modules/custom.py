import importlib
import glob

from os.path import dirname, basename, isfile

mod_paths = glob.glob("nana/modules/private/*.py")
all_modules = [basename(f)[:-3] for f in mod_paths if isfile(f)
                   and f.endswith(".py")
                   and not f.endswith('__init__.py')]

for x in all_modules:
	imported_module = importlib.import_module("nana.modules.private." + x)
