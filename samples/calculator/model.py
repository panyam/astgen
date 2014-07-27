
from astgen.astgen import *

Operator = EnumType("Operator", "PLUS", "MINUS", "MUL", "DIV")

class Expression(ASTNode): pass
                      
class BinaryExpression(Expression):
    properties = dict(op = Operator,
                      lhs = "Expression",
                      rhs = "Expression")
                      
class UnaryExpression(Expression):
    properties = dict(op = Operator,
                      child = "Expression")
    
class LiteralExpression(Expression):
    properties = dict(valueType = EnumType("Literal", "INT", "FLOAT"),
                      value = UnionType(intValue = BasicType("int"),
                                        floatValue = BasicType("float")))
                                        
