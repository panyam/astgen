
import os, astgen, utils

class CPlusPlus(astgen.ASTPlatform):
    def evalType(self, typeobj):
        if type(typeobj) is str:
            return typeobj + "Ptr"
        elif type(typeobj) is astgen.BasicType:
            if typeobj.typename == "boolean": return "bool"
            if typeobj.typename == "string": return "std::string"
            return typeobj.typename
        elif type(typeobj) is astgen.ListOf:
            return "std::list< %s >" % self.evalType(typeobj.base_type)
        elif type(typeobj) is astgen.PairOf:
            return "std::pair< %s,%s >" % (self.evalType(typeobj.type1), self.evalType(typeobj.type2))
        elif type(typeobj) is astgen.MapOf:
            return "std::map< %s,%s >" % (self.evalType(typeobj.key_type), self.evalType(typeobj.value_type))
        elif type(typeobj) is astgen.EnumType:
            return typeobj.enum_name
        return super(CPlusPlus, self).evalType(typeobj)

class Java(astgen.ASTPlatform):
    def evalType(self, typeobj):
        if type(typeobj) is astgen.BasicType:
            if typeobj.typename == "boolean": return typeobj.typename
            if typeobj.typename == "string": return "String"
            return typeobj.typename
        elif type(typeobj) is astgen.ListOf:
            return "List<%s>" % self.evalType(typeobj.base_type)
        elif type(typeobj) is astgen.MapOf:
            return "Map<%s,%s>" % (self.evalType(typeobj.key_type), self.evalType(typeobj.value_type))
        elif type(typeobj) is astgen.EnumType:
            return typeobj.enum_name
        elif type(typeobj) is astgen.PairOf:
            return "Pair<%s,%s>" % (self.evalType(typeobj.type1), self.evalType(typeobj.type2))
        elif type(typeobj) is astgen.UnionType:
            return "Object"
        return super(Java, self).evalType(typeobj)

class Python(astgen.ASTPlatform): pass

