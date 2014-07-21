
import os, astgen

class SingleFileBackend(astgen.ASTBackend):
    """
    This backend is used for langauges/frameworks where all the code related to *all* nodes
    are outputted into a single file.

    Examples of this are:

    1. A single c++ header containing both the class declaration and definition (dont do this!).
    2. A single java class with inner classes for each specific node type.
    """
    def __init__(self, *args, **kwargs):
        self.outfileName = kwargs["outfile"]
        self.backendConfig = kwargs["backendConfig"]

    def generationStarted(self, astnodes):
        """
        Called before starting node generation for any of the nodes.
        """
        parent,child = os.path.split(self.outfileName)
        if not os.isdir(parent): os.makedirs(parent)
        self.outfile = open(self.outfileName, "w")
        # write the "preamble" before the nodes are generated

    def generationFinished(self, astnodes):
        """
        Called after the code generation of all nodes has completed.
        """
        # write the "conclusion" after the nodes are generated
        self.outfile.close()

    def nodeStarted(self, node):
        """
        Called before the generation of code for a particular node.
        """
        pass

    def renderNode(self, node):
        print "Node Class: ", node.__class__, node.__class__.__name__, node.getNodeName(), node.getAllAttributes()
        pass

    def nodeFinished(self, node):
        """
        Called after the generation of code for a particular node.
        """
        pass

