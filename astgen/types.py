
class BasicType(object):
    def __init__(self, name): self.typename = name
    def __str__(self): return self.typename
    def __repr__(self): return str(self)

class RefTo(object):
    def __init__(self, name): self.ref_type = name
    def __str__(self): return "(* %s)" % self.typename
    def __repr__(self): return str(self)

class ListOf(object):
    def __init__(self, base_type = None, type_name = None):
        self.base_type = base_type
        self.type_name = type_name
    def __str__(self): return "[%s]" % str(self.base_type)
    def __repr__(self): return str(self)

class PairOf(object):
    def __init__(self, type1 = None, type2 = None, type_name = None):
        self.type1 = type1 
        self.type2 = type2
        self.type_name = type_name

    def __str__(self): return "<%s,%s>" % (str(self.type1), str(self.type2))
    def __repr__(self): return str(self)

class MapOf(object):
    def __init__(self, key_type = None, value_type = None, type_name = None):
        self.key_type = key_type
        self.value_type = value_type
        self.type_name = type_name

    def __str__(self): return "<%s,%s>" % (str(self.key_type), str(self.value_type))
    def __repr__(self): return str(self)

class EnumType(object):
    def __init__(self, enum_name, *enum_vals):
        self.enum_name = enum_name
        self.enum_vals = enum_vals

    def __repr__(self): return str(self)
    def __str__(self): return "[%s: %s]" % (self.enum_name, ",".join(self.enum_vals))

class UnionType(object):
    def __init__(self, type_name = None, **members):
        self.members = members 
        self.type_name = type_name

    def __repr__(self): return str(self)
    def __str__(self): return "{%s}" % (",".join(["%s = %s" % (k,v) for (k,v) in self.members.iteritems()]))

