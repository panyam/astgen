
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

class PairOf(object):
    def __init__(self, type1 = None, type2 = None):
        self.type1 = type1 
        self.type2 = type2

    def __str__(self): return "<%s,%s>" % (str(self.type1), str(self.type2))
    def __repr__(self): return str(self)

class MapOf(object):
    def __init__(self, key_type = None, value_type = None):
        self.key_type = key_type
        self.value_type = value_type

    def __str__(self): return "<%s,%s>" % (str(self.key_type), str(self.value_type))
    def __repr__(self): return str(self)

class EnumType(object):
    def __init__(self, *enumvals):
        self.enumvals = enumvals

    def __repr__(self): return str(self)
    def __str__(self): return "[%s]" % (",".join(self.enumvals))

class UnionType(object):
    def __init__(self, **members):
        self.members = members 

    def __repr__(self): return str(self)
    def __str__(self): return "{%s}" % (",".join(["%s = %s" % (k,v) for (k,v) in self.members.iteritems()]))

