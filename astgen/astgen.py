
import os, sys, importlib, imp

class ASTCodeGenerator(object):
    """
    Given an AST node generates the code for the node.  This can be used to 
    generate AST code for different languages or platforms.
    """
    def geenerateCode(self, astnode): pass

class BasicType(object):
    def __init__(self, name): self.typename = name
    def __str__(self): return self.typename
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

    def getConstructors(self):
        """
        Returns all possible constructors for this type of AST Node.   
        Each "constructor" corresponds on particular production of a rule in the grammar.
        Eg:

        expr ::=  binary_expressionj
              |   unary_expression

        would typically have 2 different constructors for the "expr" node.
        """
        pass

    def generatePreamble(self):
        pass


if __name__ == "__main__":
    the_module = imp.load_source("", sys.argv[1])
    for attrname in dir(the_module):
        try:
            attr = getattr(the_module, attrname)
            if attrname != "ASTNode" and any(map(lambda x: x.__name__ == "ASTNode", attr.__mro__)):
                print "Generating code for: ", attr, attrname, attr.getAllAttributes()
        except (TypeError, AttributeError):
            pass

