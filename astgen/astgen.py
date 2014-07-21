
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
    def getNodeName(cls):
        cls.getAllAttributes()
        return cls.__attrib_table__["cls"]

    @classmethod
    def getAllAttributes(cls):
        if not hasattr(cls, "__attrib_table__") or cls.__attrib_table__["cls"] is not cls.__name__:
            cls.__attrib_table__ = {"cls": cls.__name__, "attributes": {}}
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
    """
    def __init__(self, backend):
        """
        Creates a new code generator with the given backend.
        """
        self.backend = backend

    def generateCode(self, astnodes):
        self.backend.generationStarted(astnodes)
        generated = {}
        for node in astnodes:
            self.generateCodeForNode(node, generated)
        self.backend.generationFinished(astnodes)

    def generateCodeForNode(self, node, generated):
        if node in generated and generated[node]: return

        generated[node] = True
        if issubclass(node.__base__, ASTNode) and node.__base__ is not ASTNode:
            self.generateCodeForNode(node.__base__, generated)

        self.backend.nodeStarted(node)
        self.backend.renderNode(node)
        self.backend.nodeFinished(node)

class ASTBackend(object):
    def __init__(self, *args, **kwargs):
        pass

    def generationStarted(self, astnodes):
        """
        Called before starting node generation for any of the nodes.
        """
        pass

    def generationFinished(self, astnodes):
        """
        Called after the code generation of all nodes has completed.
        """
        pass

    def nodeStarted(self, node):
        """
        Called before the generation of code for a particular node.
        """
        pass

    def renderNode(self, node):
        print "Node Class: ", node.__class__, node.__class__.__name__, node.getNodeName(), node.getAllAttributes()
        pass

    def nodeFinished(self, node):
        """
        Called after the generation of code for a particular node.
        """
        pass

