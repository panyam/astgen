
import os, astgen
from jinja2 import Environment, PackageLoader

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
        self.templateName = kwargs.get("template") or  "SingleFile/cpp"
        self.backendConfig = kwargs["backendConfig"]
        if self.templateName.startswith("/"):
            # use a loader that loads from absolute path
            self.env = Environment()
            self.template = self.env.get_template(self.templateName)
        else:
            self.env = Environment(loader=PackageLoader('astgen', 'templates'))
            self.template = self.env.get_template(self.templateName)


    def generationStarted(self, astnodes):
        """
        Called before starting node generation for any of the nodes.
        """
        parent,child = os.path.split(self.outfileName)
        if parent and not os.path.isdir(parent): os.makedirs(parent)
        self.outfile = open(self.outfileName, "w")
        # write the "preamble" before the nodes are generated

    def generationFinished(self, astnodes):
        """
        Called after the code generation of all nodes has completed.
        """
        # write the "conclusion" after the nodes are generated
        self.outfile.close()

    def renderNodes(self, nodes):
        print self.template.render(nodes = nodes, backendConfig = self.backendConfig)

