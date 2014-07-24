
import os, astgen, utils

DEFAULT_SINGLEFILE_TEMPLATE = "SingleFile/cpp"

DEFAULT_TWOFILES_HEADER_TEMPLATE = "TwoFiles/cpp_header"
DEFAULT_TWOFILES_IMPLEMENTATION_TEMPLATE = "TwoFiles/cpp_implementation"

class SingleFileLayout(astgen.ASTLayout):
    """
    This backend is used for langauges/frameworks where all the code related to *all* nodes
    are outputted into a single file.

    Examples of this are:

    1. A single c++ header containing both the class declaration and definition (dont do this!).
    2. A single java class with inner classes for each specific node type.
    """
    def __init__(self, *args, **kwargs):
        super(SingleFileLayout, self).__init__(self, *args, **kwargs)
        self.outputdir = kwargs.get("outdir") or "."
        self.outfileName = self.backendConfig.get("HEADER_OUTPUT") or None
        assert self.outfileName is not None, "HEADER_OUTPUT variable MUST be specified in the backend config.  This is the file to the generated code for all nodes will be written to."
        self.templateName = self.backendConfig.get("HEADER_TEMPLATE") or DEFAULT_SINGLEFILE_TEMPLATE 
        self.template = utils.load_template(self.templateName)

    def generationStarted(self, astnodes):
        """
        Called before starting node generation for any of the nodes.
        """
        self.outfile = open(self.outfileName, "w")

    def generationFinished(self, astnodes):
        """
        Called after the code generation of all nodes has completed.
        """
        # write the "conclusion" after the nodes are generated
        self.outfile.close()

    def renderNodes(self, nodes):
        self.outfile.write(self.template.render(nodes = nodes,
                                                backendConfig = self.backendConfig,
                                                platform = self.platformBackend))

class TwoFilesLayout(astgen.ASTLayout):
    """
    This backend is used where there is a concept of a header/implementation seperation (eg C/C++/ObjC).
    """
    def __init__(self, *args, **kwargs):
        super(TwoFilesLayout, self).__init__(self, *args, **kwargs)
        self.outputdir = kwargs.get("outdir") or "."
        self.header_filename = self.backendConfig.get("HEADER_OUTPUT") or None
        self.implementation_filename = self.backendConfig.get("IMPLEMENTATION_OUTPUT") or None
        assert self.header_filename is not None, "HEADER_OUTPUT variable MUST be specified in the backend config.  This is the file to the generated header code for all nodes will be written to."
        assert self.implementation_filename is not None, "IMPLEMENTATION_OUTPUT variable MUST be specified in the backend config.  This is the file to the generated implementation code for all nodes will be written to."
        self.headerTemplateName = self.backendConfig.get("HEADER_TEMPLATE") or DEFAULT_TWOFILES_HEADER_TEMPLATE 
        self.implementationTemplateName = self.backendConfig.get("IMPLEMENTATION_TEMPLATE") or DEFAULT_TWOFILES_IMPLEMENTATION_TEMPLATE 
        self.header_template = utils.load_template(self.headerTemplateName)
        self.implementation_template = utils.load_template(self.implementationTemplateName)


    def generationStarted(self, astnodes):
        """
        Called before starting node generation for any of the nodes.
        """
        print "Writing header to: ", self.header_filename
        print "Writing implementation to: ", self.implementation_filename
        self.header_file = open(self.header_filename, "w")
        self.implementation_file = open(self.implementation_filename, "w")

    def generationFinished(self, astnodes):
        """
        Called after the code generation of all nodes has completed.
        """
        # write the "conclusion" after the nodes are generated
        self.header_file.close()
        self.implementation_file.close()

    def renderNodes(self, nodes):
        self.header_file.write(self.header_template.render(nodes = nodes, backendConfig = self.backendConfig))
        self.implementation_file.write(self.implementation_template.render(nodes = nodes,
                                                                           backendConfig = self.backendConfig),
                                                                           platform = self.platformConfig)

