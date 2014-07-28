
import os, astgen, utils

DEFAULT_SINGLEFILE_TEMPLATE = "cpp_header"
DEFAULT_TWOFILES_HEADER_TEMPLATE = DEFAULT_SINGLEFILE_TEMPLATE
DEFAULT_TWOFILES_IMPLEMENTATION_TEMPLATE = "cpp_implementation"

DEFAULT_FWDDEFS_OUTPUT = "ForwardDefs.h"
DEFAULT_PUBLIC_OUTPUT = "Public.h"
DEFAULT_ENUMS_OUTPUT = "Enums.h"
DEFAULT_FWDDEFS_TEMPLATE = "cpp_fwddefs"
DEFAULT_PUBLIC_TEMPLATE = "cpp_public"
DEFAULT_ENUMS_TEMPLATE = "cpp_enums"

class OneFileLayout(astgen.ASTLayout):
    """
    This layout is used for langauges/frameworks where all the code related to *all* nodes
    are outputted into a single file.

    Examples of this are:

    1. A single c++ header containing both the class declaration and definition (dont do this!).
    2. A single java class with inner classes for each specific node type.
    """
    def __init__(self, *args, **kwargs):
        super(OneFileLayout, self).__init__(*args, **kwargs)
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

    def renderNodes(self, nodelist):
        self.outfile.write(self.template.render(nodelist = nodelist,
                                                backendConfig = self.backendConfig,
                                                platform = self.platformBackend))

class TwoFilesLayout(astgen.ASTLayout):
    """
    This backend is used where there is a concept of a header/implementation seperation (eg C/C++/ObjC).
    """
    def __init__(self, *args, **kwargs):
        super(TwoFilesLayout, self).__init__(*args, **kwargs)
        self.header_filename = self.backendConfig.get("HEADER_OUTPUT") or None
        self.implementation_filename = self.backendConfig.get("IMPLEMENTATION_OUTPUT") or None
        assert self.header_filename is not None, "HEADER_OUTPUT variable MUST be specified in the backend config.  This is the file to the generated header code for all nodes will be written to."
        assert self.implementation_filename is not None, "IMPLEMENTATION_OUTPUT variable MUST be specified in the backend config.  This is the file to the generated implementation code for all nodes will be written to."
        self.headerTemplateName = self.backendConfig.get("HEADER_TEMPLATE") or DEFAULT_TWOFILES_HEADER_TEMPLATE 
        self.implementationTemplateName = self.backendConfig.get("IMPLEMENTATION_TEMPLATE") or DEFAULT_TWOFILES_IMPLEMENTATION_TEMPLATE 
        self.header_template = utils.load_template(self.headerTemplateName)
        self.implementation_template = utils.load_template(self.implementationTemplateName)


    def generationStarted(self, nodelist):
        """
        Called before starting node generation for any of the nodes.
        """
        print "Writing header to: ", self.header_filename
        print "Writing implementation to: ", self.implementation_filename
        self.header_file = open(self.header_filename, "w")
        self.implementation_file = open(self.implementation_filename, "w")

    def generationFinished(self, nodelist):
        """
        Called after the code generation of all nodes has completed.
        """
        # write the "conclusion" after the nodes are generated
        self.header_file.close()
        self.implementation_file.close()

    def renderNodes(self, nodelist):
        self.header_file.write(self.header_template.render(nodelist = nodelist, 
                                                           platform = self.platformBackend,
                                                           no_implementation = True,
                                                           backendConfig = self.backendConfig))
        self.implementation_file.write(self.implementation_template.render(nodelist = nodelist,
                                                                           backendConfig = self.backendConfig,
                                                                           platform = self.platformBackend))

class OneFilePerNodeLayout(astgen.ASTLayout):
    def __init__(self, *args, **kwargs):
        super(OneFilePerNodeLayout, self).__init__(*args, **kwargs)

class TwoFilesPerNodeLayout(astgen.ASTLayout):
    """
    This backend is used where there is a concept of a header/implementation seperation (eg C/C++/ObjC).
    """
    def __init__(self, *args, **kwargs):
        super(TwoFilesPerNodeLayout, self).__init__(*args, **kwargs)
        self.fwddefs_filename = self.backendConfig.get("FWDDEFS_OUTPUT", DEFAULT_FWDDEFS_OUTPUT)
        self.public_filename = self.backendConfig.get("PUBLIC_OUTPUT", DEFAULT_PUBLIC_OUTPUT)

        self.fwddefsTemplateName = self.backendConfig.get("FWDDEFS_TEMPLATE") or DEFAULT_FWDDEFS_TEMPLATE
        self.publicTemplateName = self.backendConfig.get("PUBLIC_TEMPLATE") or DEFAULT_PUBLIC_TEMPLATE

        self.fwddefs_template = utils.load_template(self.fwddefsTemplateName)
        self.public_template = utils.load_template(self.publicTemplateName)

    def generationStarted(self, nodelist):
        """
        Called before starting node generation for any of the nodes.
        """
        # First create a single header file for all enums
        # we *could* do this as one file per enum but its an overkill
        # 
        # First create the "Fwds", "Enums" and "Main" header files
        print "Writing header to: ", self.header_filename
        print "Writing implementation to: ", self.implementation_filename
        self.header_file = open(self.header_filename, "w")
        self.implementation_file = open(self.implementation_filename, "w")

    def generationFinished(self, nodelist):
        """
        Called after the code generation of all nodes has completed.
        """
        # write the "conclusion" after the nodes are generated
        self.header_file.close()
        self.implementation_file.close()

    def renderNodes(self, nodelist):
        self.header_file.write(self.header_template.render(nodelist = nodelist,
                                                           platform = self.platformBackend,
                                                           no_implementation = True,
                                                           backendConfig = self.backendConfig))
        self.implementation_file.write(self.implementation_template.render(nodelist = nodelist,
                                                                           backendConfig = self.backendConfig,
                                                                           platform = self.platformBackend))

