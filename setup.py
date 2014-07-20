from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
import os, sys

VERSION = "0.0.1"
install_requires = [
    "jinja2"
]

CLASSIFIERS = [
    'Intended Audience :: Language Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Parser and Compiler Development',
]

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

def get_all_sub_folders(parent):
    packages, data_files, scripts = [], [], []
    root_dir = os.path.dirname(__file__)
    if root_dir != '':
        os.chdir(root_dir)
    for dirpath, dirnames, filenames in os.walk(parent):
        # Ignore dirnames that start with '.'
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'):
                del dirnames[i]
        if '__init__.py' in filenames:
            packages.append('.'.join(fullsplit(dirpath)))
        elif filenames:
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
    return packages, data_files, scripts

packages, data_files, scripts = get_all_sub_folders(".")

print "Packages: ", packages
print "Datafiles: ", data_files
print "Scripts: ", scripts

setup(name="astgen",
      version=VERSION,
      classifiers = CLASSIFIERS,
      description="A generic code generators for AST for use in parsers.",
      author="Sri Panyam",
      author_email="sri.panyam@gmail.com",
      url="http://github.com/panyam/astgen/",
      scripts = scripts,
      packages = packages,
      data_files = data_files,
      install_requires = install_requires
      )
