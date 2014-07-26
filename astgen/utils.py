
import os, sys

def import_module(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def import_file(full_path_to_module):
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

def load_nodes_from_file(input_file):
    import astgen
    the_module = import_file(input_file)
    nodes = []
    for attrname, attr in the_module.__dict__.items():
        try:
            if issubclass(attr, astgen.ASTNode) and attr is not astgen.ASTNode:
                nodes.append(attr)
        except (TypeError, AttributeError):
            pass
    return nodes

def load_template(template_path):
    from jinja2 import Environment, PackageLoader
    kwargs = dict(trim_blocks = True,
                  lstrip_blocks = True,
                  extensions = [ "jinja2.ext.do" ])
    if not template_path.startswith("/"):
        kwargs["loader"] = PackageLoader("astgen", "templates")
    env = Environment(**kwargs)
    return env.get_template(template_path)

