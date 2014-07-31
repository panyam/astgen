from distutils.core import setup
import fnmatch, os.path
from astgen import version


def pdir():
    dirname, _ = os.path.split(__file__)
    return os.path.abspath(dirname)


def _fnmatch(name, patternList):
    for i in patternList:
        if fnmatch.fnmatch(name, i):
            return True
    return False


def _splitAll(path):
    parts = []
    h = path
    while 1:
        if not h:
            break
        h, t = os.path.split(h)
        parts.append(t)
    parts.reverse()
    return parts


def findPackages(path, dataExclude=[]):
    """
        Recursively find all packages and data directories rooted at path. Note
        that only data _directories_ and their contents are returned -
        non-Python files at module scope are not, and should be manually
        included.

        dataExclude is a list of fnmatch-compatible expressions for files and
        directories that should not be included in pakcage_data.

        Returns a (packages, package_data) tuple, ready to be passed to the
        corresponding distutils.core.setup arguments.
    """
    packages = []
    datadirs = []
    for root, dirs, files in os.walk(path, topdown=True):
        if "__init__.py" in files:
            p = _splitAll(root)
            packages.append(".".join(p))
        else:
            dirs[:] = []
            if packages:
                datadirs.append(root)

    # Now we recurse into the data directories
    package_data = {}
    for i in datadirs:
        if not _fnmatch(i, dataExclude):
            parts = _splitAll(i)
            module = ".".join(parts[:-1])
            acc = package_data.get(module, [])
            for root, dirs, files in os.walk(i, topdown=True):
                sub = os.path.join(*_splitAll(root)[1:])
                if not _fnmatch(sub, dataExclude):
                    for fname in files:
                        path = os.path.join(sub, fname)
                        if not _fnmatch(path, dataExclude):
                            acc.append(path)
                else:
                    dirs[:] = []
            package_data[module] = acc
    return packages, package_data


# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
# for scheme in INSTALL_SCHEMES.values(): scheme['data'] = scheme['purelib']

long_description = file(os.path.join(pdir(), "README.md")).read()
packages, package_data = findPackages("astgen")

print "Packages: ", packages
print "Datafiles: ", package_data

setup(name="astgen",
      version=version.VERSION,
      description="A generator for Abstract Syntax Trees.",
      long_description=long_description,
      author="Sri Panyam",
      author_email="sri.panyam@gmail.com",
      url="http://github.com/panyam/astgen/",
      scripts = ["./bin/astgen"],
      packages = packages,
      package_data = package_data,
      install_requires = [
        "jinja2>=2.7"
      ],
      classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
      ]
      )
