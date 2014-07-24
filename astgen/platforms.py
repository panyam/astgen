
import os, astgen, utils

class CPlusPlus(astgen.ASTPlatform):
    def getType(self, typeobj):
        if type(typeobj) is str:
            return typeobj + "Ptr"
        elif type(typeobj) is astgen.BasicType:
            if typeobj.typename == "boolean": return "bool"
            if typeobj.typename == "string": return "std::string"
            return typeobj.typename
        elif type(typeobj) is astgen.ListOf:
            return "std::list<%s>" % self.getType(typeobj.base_type)
        elif type(typeobj) is astgen.EnumType:
            return typeobj.enum_name
        return str(typeobj)

class Java(astgen.ASTPlatform): pass
class Python(astgen.ASTPlatform): pass

