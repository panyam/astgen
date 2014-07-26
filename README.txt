
astgen - A tool for creating Abstract Syntaxt Trees
===================================================

Introduction
------------

This tools allows language and compiler developers to generate Abstract Syntax Trees that can be 
used by parsers (or parser generators) to record the result of a parse phase.   The input is a set
of python classes which describe the methods and members of the AST classes specific to the parser
and outputs language specific (so far Java and C++) classes with the definitions of the various
AST classes.

Installation
------------

```
pip install astgen
```

or from github

```
git clone [git-repo-url] astgen
cd astgen
python setup.py install
```

Getting Started
---------------

Upon installation, a script called "astgen" is created.  To see its usage, invoke it with the -h option:

```
bash-3.2$ astgen -h
Usage: astgen [options]

Options:
  -h, --help            show this help message and exit
  -o OUTPUTDIR, --outputdir=OUTPUTDIR
                        The output folder in which all generted files are
                        written to.
  -l LAYOUT_BACKEND, --layout_backend=LAYOUT_BACKEND
                        The backend to decide the package layout of the code
                        being generated, eg single file, multiple files etc
  -p PLATFORM_BACKEND, --platform_backend=PLATFORM_BACKEND
                        The backend to help with the platform to target code
                        genration for, eg java, python, stl, C etc
  -c BACKEND_CONFIG, --data=BACKEND_CONFIG
                        Data required any custom data that can be used/passed
                        to the platform or layout backends.
  -m MODEL_FILE, --modelfile=MODEL_FILE
                        Input model file containing AST definitions for which
                        AST code is to be generated.
```
