
astgen - A tool for generating Abstract Syntaxt Trees
=====================================================

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
To try out the /alculator example:

```
cd samples/calculator
astgen -o /tmp/calculator -m model.py -c cpp_config.py
```

This would now generate all the files for the various AST nodes
associated with the sample in the folder /tmp/calculator

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

Config
------

The config file (specified with the -c parameter) contains overrides and other data used by the various parts of astgen while generating the AST code.  The different parameters depend on the layout and platform backends used and will be described in the respective sections.

Types
------

In the Models section, nodes and properties were discussed.  Each property must have a type.  The type value of a property can be a String which indicates a reference to a value of another defined class (in the above case an "Expression") or it can be one of the following types:


#### BasicType("type")

Defines a native type that is platform specific and will resolved by the PlatformBackend object.  For instance:

```
Integer = BasicType("int")
```

defines a type called Integer which will is of type "int" and can be equal to an int variable in C/C++ or in Java.  

Note that this does not mean that only primitive types can be defined in this manner.  The use of BasicType is only a hint that the underlying type (and its string representation that is rendered in the final output) is determined by the PlatformBackend.  For a more complicated examle the following can also be defined:

```
PointListPtr = BasicType("PointListPtr")
```

and in return, this could be resolved to (in C++) as:

```
std::shared_ptr<std::list<Point>>
```

How these types are resolved will be discussed in the PlatformBackend section.

#### EnumType(TypeName, EnumVal1, EnumVal2, EnumVal3....)

Defines an Enum type similar to the following:

```
enum TypeName
{
    EnumVal1,
    EnumVal2,
    EnumVal3
    ...
}
```

#### PairOf(Type1, Type2, TypeName = '')

Defines a Pair type over the given two sub types.  In C++ this would be similar to:

```
typedef std::pair<Type1, Type2> TypeName
```

If the TypeName is not specified, a name is automatically generated and used.

#### ListOf(BaseType, TypeName = '')

Defines a type that is the List of a BaseType typed values.  In C++ this would be similar to:

```
typedef std::list<Type1, Type2> TypeName
```

If the TypeName is not specified, a name is automatically generated and used.

#### MapOf(KeyType, ValueType)


Defines a type that is the Map with the key and value types given by KeyType and ValueType respectively.  In C++ this would be similar to:

```
typedef std::map<KeyType, ValueType> TypeName
```

If the TypeName is not specified, a name is automatically generated and used.

Platforms
---------

The Platform objects are responsible for handling and delegating all concerns related to the specific platform the ASTs are being generated for (eg C++, Java etc).   For now a Platform object only provides one method:

```
def evalType(self, typeobj): pass
```

This method is responsible for returning the string representation of a type object (eg those discussed in the Types section) specific to the platform.  To achieve the results above, the astgen.platforms.CPlusPlus backend looks like this:

```
class CPlusPlus(astgen.ASTPlatform):
    def evalType(self, typeobj):
        if type(typeobj) is str:
            return typeobj + "Ptr"
        elif type(typeobj) is astgen.BasicType:
            if typeobj.typename == "boolean": return "bool"
            if typeobj.typename == "string": return "std::string"
            return typeobj.typename
        elif type(typeobj) is astgen.ListOf:
            return "std::list<%s>" % self.evalType(typeobj.base_type)
        elif type(typeobj) is astgen.PairOf:
            return "std::pair<%s,%s>" % (self.evalType(typeobj.type1), self.evalType(typeobj.type2))
        elif type(typeobj) is astgen.MapOf:
            return "std::map<%s,%s>" % (self.evalType(typeobj.key_type), self.evalType(typeobj.value_type))
        elif type(typeobj) is astgen.EnumType:
            return typeobj.enum_name
        return super(CPlusPlus, self).evalType(typeobj)
```

Custom platform backends can be provided to the astgen script with the -p parameter.

Alternatively, it can be defined in the Config(.py) file itself.

So far the following (hopefully self explanatory) platforms are defined:

#### astgen.platforms.CPlusPlus

#### astgen.platforms.Java

Layouts
-------

Regardless of the platform, there would be several ways to layout the generate nodes.  For instance, for C++ alone, the following (and several more) layouts are possible:

 - Monolithic header file: A single .h file that would contain all class definitions along with their implementations.
 - Two files: Broken down into one header file (containing all the interface/class declarations) and an implementation file (containing all the class/implementation definitions).
 - Two files per class: Each class with its own header and implementation files.

There could be several other layouts depending on the needs of the project.  All these layouts inherit from the ASTLayout base.  The ASTLayout base has the following methods:

```
class ASTLayout(object):
    """
    Given an AST node generates the code for the node.  This can be used to 
    generate AST code for different languages or platforms.
    """

    def orderNodes(self, nodes):
        """
        Called to order all nodes in any way as deemed necessary.
        """
        pass

    def generationStarted(self, nodelist):
        """
        Called before starting node generation for any of the nodes.
        """
        pass

    def generationFinished(self, nodelist):
        """
        Called after the code generation of all nodes has completed.
        """
        pass

    def nodeStarted(self, node):
        """
        Called before the generation of code for a particular node.
        """
        pass

    def renderNodes(self, nodelist):
        """
        Called to render all nodes
        """
        pass

    def renderNode(self, node):
        """
        Called to render a particular node.
        """
        pass

    def nodeFinished(self, node):
        """
        Called after the generation of code for a particular node.
        """
        pass

```

Shown below are the laout classes that are defined so far (along with the parameters they accept in the config file):

##### astgen.layouts.OneFileLayout

The monolithic one file layout where all class are declared and defined in the same file.  The following options in the config file are accepted:

- HEADER_OUTPUT:    The output file to which all classes will be written to.
- HEADER_TEMPLATE:  The (jinja2) template file that will be used to render all the classes (defaults to "cpp_header").

##### astgen.layouts.TwoFilesLayout

The two files layout where all class interface declarations are written to a header and implementations/definitions are written to an implementation file (eg .cpp, .m etc).  The following options in the config file are accepted:

- HEADER_OUTPUT:            The output file to which all classes declarations will be written to.
- HEADER_TEMPLATE:          The (jinja2) template file that will be used to render all the classes (defaults to "cpp_header").
- IMPLEMENTATION_OUTPUT:    The output file to which all classes definitions/implementations will be written to.
- IMPLEMENTATION_TEMPLATE:  The (jinja2) template file that will be used to render all the classes implementaitons/definitions (defaults to "cpp_implementation").

##### astgen.layouts.TwoFilesPerNodeLayout

In this layout, each node is written to its own file (typical
<NodeName>.h and <NodeName.cpp>).  Additionally, a forward defs file, a
public headers file and a header file for all enums is also generated.
These are denoted by:

- FWDDEFS_OUTPUT:           The output file to which all forward definitions are written (optional).
- ENUMS_OUTPUT:             The output file to which all enums are written (optional).
- PUBLIC_OUTPUT:            The output file to which all include headers are written to (optional).

- FWDDEFS_TEMPLATE:         The (jinja2) template file that will be used to render the forward definitions (if used).
- ENUMS_TEMPLATE:           The (jinja2) template file that will be used to render the enum definitions (if used).
- PUBLIC_TEMPLATE:          The (jinja2) template file that will be used to render the public header includes (if used).

Note that the above are all optional and not required in all cases (for
instance for Java none of the above are required).

