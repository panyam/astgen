
class BasicType(object):
    def __init__(self, name): self.typename = name
    def __str__(self): return self.typename
    def __repr__(self): return str(self)

class RefTo(object):
    def __init__(self, name): self.typename = name
    def __str__(self): return "(* %s)" % self.typename
    def __repr__(self): return str(self)

class ListOf(object):
    def __init__(self, base_type = None): self.base_type = base_type
    def __str__(self): return "[%s]" % str(self.base_type)
    def __repr__(self): return str(self)

class MapOf(object):
    def __init__(self, key_type = None, value_type = None):
        self.key_type = key_type
        self.base_type = base_type

    def __str__(self): return "<%s,%s>" % (str(self.key_type), str(self.value_type))
    def __repr__(self): return str(self)

class ASTNode(object):
    """
    A class that represents an AST node that is generated to be useable by 
    a parser for building the AST
    """
    attributes = {}

    @classmethod
    def getAllAttributes(cls):
        if not hasattr(cls, "__attrib_table__") or cls.__attrib_table__["cls"] is not cls:
            cls.__attrib_table__ = {"cls": cls, "attributes": {}}
            if cls.__base__ and hasattr(cls.__base__, "getAllAttributes"):
                for key,value in cls.__base__.getAllAttributes().items():
                    cls.__attrib_table__["attributes"][key] = value
            for key,value in cls.attributes.items():
                cls.__attrib_table__["attributes"][key] = value
        return cls.__attrib_table__["attributes"]

class ASTCodeGen(object):
    """
    Given an AST node generates the code for the node.  This can be used to 
    generate AST code for different languages or platforms.

    The code generator needs to the following:
    1. Resolve native types for the types we have specified in the input file
    2. Resolve paths to files where output is to be written.  This is highly
       language and framework specific.  It can range from: 
          a. everything going into a single file, eg:
              1. Individual C++ classes with implementation and interface in the .h file
              2. Individual .java files with all nodes as inner classes
              3. .py files with all nodes as proper classes in the module
          b. everything going into multiple files with interface and implementation files
              1. eg .h and .cpp (or .m or .c) files with interface and implementation respectively
          c. each node going to a seperate file - this may or may not require different folder 
             structures depending on namespaces and packages
              1. eg as .java files or .py files
          d. each node having its own interface and implementation file, eg:
              1. eg as .h and .c/.cpp/.m respectively
    3. Use the templates based on above options to generate the code.

    def generate(node, astnodes):
        generated = {}
        for node in astnodes:
            generateCodeForNode(node, generated)

    def generateCodeForNode(node, generated = {}):
        if node in generated and generated[node]: return

        if node.parent: generateCodeForNode(node.parent, generated)
        sendEvent("nodeStarted", node)
        sendEvent("nodeFinished", node)
        generated[node] = True
    """
    def generateCode(self, astnodes):
        generated = {}
        for node in astnodes:
            self.generateCodeForNode(node, generated)

    def generateCodeForNode(self, node, generated):
        if node in generated and generated[node]: return

        generated[node] = True
        if issubclass(node.__base__, ASTNode):
            self.generateCodeForNode(node.__base__, generated)

        print "Node Class: ", node.__class__

