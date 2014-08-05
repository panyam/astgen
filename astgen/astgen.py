
from types import *

class ASTNode(object):
    """
    A class that represents an AST node that is generated to be useable by 
    a parser for building the AST
    """
    properties = {}

    @classmethod
    def parent(cls):
        if issubclass(cls.__base__, ASTNode) and cls.__base__ is not ASTNode:
            return cls.__base__
        return None

    @classmethod
    def nodeName(cls):
        cls.allProperties()
        return cls.__property_table__["cls"]

    @classmethod
    def allProperties(cls):
        if not hasattr(cls, "__property_table__") or cls.__property_table__["cls"] is not cls.__name__:
            cls.__property_table__ = {"cls": cls.__name__, "properties": {}}
            if cls.__base__ and hasattr(cls.__base__, "allProperties"):
                for key,value in cls.__base__.allProperties().iteritems():
                    cls.__property_table__["properties"][key] = value
            for key,value in cls.properties.iteritems():
                cls.__property_table__["properties"][key] = value
        return cls.__property_table__["properties"]

    @classmethod
    def constructors(cls):
        return []

    @classmethod
    def gettersFor(cls, prop):
        # for a particular property the default getter would be:
        # of type const reference of the getter's value
        return []

    @classmethod
    def settersFor(cls, prop):
        return []

class ASTNodeList(object):
    def __init__(self, *nodes):
        if len(nodes) == 1 and type(nodes[0]) is list:
            nodes = nodes[0]
        self.nodes = nodes

    def allEnumTypes(self):
        for t in self.allBaseTypes():
            if t.__class__ == EnumType:
                yield t

    def allBaseTypes(self):
        """
        Yields all base types used across all nodes.
        This will exclude compound types such as Lists, Pairs and Maps.
        """
        visited = {}
        stack = []
        for node in self.nodes:
            for prop_name, prop_type in node.properties.iteritems():
                stack.append(prop_type)

        while stack:
            toptype = stack.pop()
            if toptype.__class__ == ListOf:
                stack.append(toptype.base_type)
            elif toptype.__class__ == PairOf:
                stack.append(toptype.type1)
                stack.append(toptype.type2)
            elif toptype.__class__ == MapOf:
                stack.append(toptype.key_type)
                stack.append(toptype.value_type)
            elif toptype.__class__ == UnionType:
                for mname, mtype in toptype.members.iteritems():
                    stack.append(mtype)
            elif toptype.__class__ == RefTo:
                stack.append(toptype.ref_type)
            else:
                if toptype.__class__ == EnumType:
                    if toptype.enum_name not in visited:
                        visited[toptype.enum_name] = toptype
                        yield toptype
                elif toptype.__class__ == BasicType:
                    if toptype.typename not in visited:
                        visited[toptype.typename] = toptype
                        yield toptype

class ASTPlatform(object):
    """
    The platform backend takes care of all language and platform specific details 
    like determining exact classes for the types, method signatures for one or more
    getters and/or setters for properties.
    """
    def __init__(self, *args, **kwargs):
        self.backendConfig = kwargs.get("backendConfig") or {}

    def evalType(self, typeobj):
        if type(typeobj) is BasicType:
            return typeobj.typename
        return str(typeobj)

class ASTLayout(object):
    """
    Given an AST node generates the code for the node.  This can be used to 
    generate AST code for different languages or platforms.

    The code generator needs to the following:
    1. Resolve paths to files where output is to be written.  This is highly
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
    2. Use the templates based on above options to generate the code.
    """
    def __init__(self, platformBackend, *args, **kwargs):
        self.platformBackend = platformBackend
        self.backendConfig = kwargs.get("backendConfig") or {}
        self.outputdir = self.backendConfig.get("OUTPUT_DIR") or kwargs.get("outdir") or "."

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

    def generateCode(self, nodelist):
        if type(nodelist) is list:
            nodelist = ASTNodeList(nodelist)
        ordered_nodelist = ASTNodeList(self.orderNodes(nodelist.nodes))
        self.generationStarted(nodelist)
        self.renderNodes(ordered_nodelist)
        self.generationFinished(nodelist)

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

    def renderNodes(self, nodelist):
        for node in nodelist.nodes:
            self.nodeStarted(node)
            self.renderNode(node)
            self.nodeFinished(node)

    def nodeStarted(self, node):
        """
        Called before the generation of code for a particular node.
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

    def openOutputFile(self, filepath):
        filepath = filepath.strip()
        if not filepath.startswith("/"):
            filepath = self.outputdir + "/" + filepath
        return open(filepath, "w")

