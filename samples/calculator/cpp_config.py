
"""
Name of the namespace underwhich all the node definitions will be generated.
"""
NAMESPACE = "Calculator"

"""
Templates for the header and implementation respectively
"""
HEADER_OUTPUT = "CalculatorAST.h"
IMPLEMENTATION_OUTPUT = "CalculatorAST.cpp"

INITIAL_HEADERS = """
#include <list>
#include <map>
#include <string>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
"""

"""
The preamble that gets included *before* any code is generated.
"""
NAMESPACE_PREAMBLE = """
"""

IMPLEMENTATION_PREAMBLE = """
#include "%s"
""" % HEADER_OUTPUT

