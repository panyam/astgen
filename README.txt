

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


The MODEL_FILE and BACKEND_CONFIG parameters are mandatory while the Platform parameter defaults to C++ (ie outputs are C++ classes) and a two file layout is used where all node declarations are writen to the header (.h) file and the definitions are written to the implementation file (.cpp).

Sample Usage
------------

To try out the calculator example:

```
cd samples/calculator
astgen -m model.py -c config.py
```

This would now generate the files CalculatorAST.h and CalculatorAST.cpp.

Models
------

Models define the structure of AST nodes that are to be generated.   A model looks similar to:

```
class NodeClass(ASTNode):
    properties = dict(member1 = MemberType1,
                      member2 = MemberType2,...)
```

Nodes can also inherit from other defined nodes, eg:

```

Operator = EnumType("Operator", "PLUS", "MINUS", "MUL", "DIV")

class Expression(ASTNode): pass

class BinaryExpression(Expresssion):
    """
    Has a binary operator and left and right sub expressions.
    """
    properties = dict(op = Operator, 
                      lhs = "Expression",
                      rhs = "Expression")

class UnaryExpression(Expression):
    """
    Has a prefix operator and an expression
    """
    properties = dict(op = Operator, 
                      child = "Expression")
```

Types will be discussed in next section.

Types
------

In the Models section, nodes and properties were discussed.  Each property must have a type.  The type value of a property can be a String to be a reference to a value of another defined class (in the above case an "Expression") or it can be one of the following types:


BasicType("type")

EnumType(TypeName, EnumVal1, EnumVal2, EnumVal3....)

PairOf(Type1, Type2)

ListOf(BaseType)

MapOf(KeyType, ValueType)


License
----

MIT

