
from types import *

class ASTNode(object):
    """
    A class that represents an AST node that is generated to be useable by 
    a parser for building the AST
    """
    attributes = {}

    @classmethod
    def getParentNode(cls):
        if issubclass(cls.__base__, ASTNode) and cls.__base__ is not ASTNode:
            return cls.__base__.__name__
        return None

    @classmethod
    def getNodeName(cls):
        cls.getAllAttributes()
        return cls.__attrib_table__["cls"]

    @classmethod
    def getAllAttributes(cls):
        if not hasattr(cls, "__attrib_table__") or cls.__attrib_table__["cls"] is not cls.__name__:
            cls.__attrib_table__ = {"cls": cls.__name__, "attributes": {}}
            if cls.__base__ and hasattr(cls.__base__, "getAllAttributes"):
                for key,value in cls.__base__.getAllAttributes().iteritems():
                    cls.__attrib_table__["attributes"][key] = value
            for key,value in cls.attributes.iteritems():
                cls.__attrib_table__["attributes"][key] = value
        return cls.__attrib_table__["attributes"]

class ASTPlatform(object):
    def __init__(self, *args, **kwargs):
        self.backendConfig = kwargs.get("backendConfig") or {}

class ASTLayout(object):
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
    def __init__(self, *args, **kwargs):
        self.backendConfig = kwargs.get("backendConfig") or {}

    def orderNodes(self, nodes):
        """
        Given a bunch of nodes, sorts them so that their code is generated in this final order
        By default this orders nodes based on their parent dependancies.
        """
        visited = {}
        out = []
        def visit(node):
            if node in visited and visited[node]: return 
            visited[node] = True
            if issubclass(node.__base__, ASTNode) and node.__base__ is not ASTNode:
                visit(node.__base__)
            out.append(node)

        for node in nodes: visit(node)

        return out

    def generateCode(self, astnodes):
        nodes = self.orderNodes(astnodes)
        print "Transitive Closure of nodes:"
        for node in nodes: print node
        self.generationStarted(astnodes)
        self.renderNodes(nodes)
        self.generationFinished(astnodes)

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

    def renderNodes(self, nodes):
        for node in nodes:
            self.nodeStarted(node)
            self.renderNode(node)
            self.nodeFinished(node)

    def renderNode(self, node):
        print "Node Class: ", node.__class__, node.__class__.__name__, node.getNodeName(), node.getAllAttributes()
        pass

    def nodeFinished(self, node):
        """
        Called after the generation of code for a particular node.
        """
        pass

