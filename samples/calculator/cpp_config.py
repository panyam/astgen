
LAYOUT_BACKEND = "astgen.layouts.TwoFilesPerNodeLayout"

FWDDEFS_OUTPUT = "CalculatorASTFwds.h"
PUBLIC_OUTPUT = "CalculatorAST.h"
ENUMS_OUTPUT = "CalculatorASTEnums.h"

"""
Name of the namespace underwhich all the node definitions will be generated.
"""
NAMESPACE = "Calculator"

"""
Templates for the header and implementation respectively
"""
HEADER_OUTPUT = "CalculatorAST.h"
IMPL_OUTPUT = "CalculatorAST.cpp"

INITIAL_HEADERS = """
#include <list>
#include <map>
#include <string>
#include <vector>
#include <iterator>
#include <algorithm>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
"""

"""
The preamble that gets included *before* any code is generated.
"""
NAMESPACE_PREAMBLE = """
"""

IMPL_PREAMBLE = """
#include "%s"
""" % HEADER_OUTPUT

def headerFilenameForNode(node): return node.nodeName() + ".h"
def implFilenameForNode(node): return node.nodeName() + ".cpp"
