
import os, sys

def import_module(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def import_file(full_path_to_module):
    try:
        module_dir, module_file = os.path.split(full_path_to_module)
        module_name, module_ext = os.path.splitext(module_file)
        save_cwd = os.getcwd()
        if module_dir:
            os.chdir(module_dir)
        sys.path.insert(0, "./")
        module_obj = __import__(module_name)
        del sys.path[0]
        module_obj.__file__ = full_path_to_module
        globals()[module_name] = module_obj
        os.chdir(save_cwd)
        return module_obj
    except Exception, e:
        raise e
