from importlib import import_module
from os import listdir
from os.path import dirname

filenames = filter(lambda f: not f.startswith("_") and f.endswith(".py"), listdir(dirname(__file__)))
collectors = []
for filename in filenames:
    module = import_module(__name__ + "." + filename[:-3])
    funcs = filter(lambda func: func.startswith("collect_"), dir(module))
    collectors += map(lambda f: getattr(module, f), funcs)
