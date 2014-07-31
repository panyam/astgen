
import os, astgen, utils

DEFAULT_ONEFILE_TEMPLATE = "cpp_header"
DEFAULT_TWOFILES_HEADER_TEMPLATE = DEFAULT_ONEFILE_TEMPLATE
DEFAULT_TWOFILES_IMPL_TEMPLATE = "cpp_impl"

DEFAULT_ONEFILE_PER_NODE_TEMPLATE = "cpp_node_header"
DEFAULT_TWOFILES_PER_NODE_HEADER_TEMPLATE = DEFAULT_ONEFILE_PER_NODE_TEMPLATE
DEFAULT_TWOFILES_PER_NODE_IMPL_TEMPLATE = "cpp_node_impl"

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
        self.templateName = self.backendConfig.get("HEADER_TEMPLATE") or DEFAULT_ONEFILE_TEMPLATE 
        self.template = utils.load_template(self.templateName)

    def generationStarted(self, astnodes):
        """
        Called before starting node generation for any of the nodes.
        """
        self.outfile = self.openOutputFile(self.outfileName)

    def generationFinished(self, astnodes):
        """
        Called after the code generation of all nodes has completed.
        """
        # write the "conclusion" after the nodes are generated
        self.outfile.close()

    def renderNodes(self, nodelist):
        self.outfile.write(self.template.render(nodelist = nodelist,
                                                layout = self,
                                                backendConfig = self.backendConfig,
                                                platform = self.platformBackend))

class TwoFilesLayout(astgen.ASTLayout):
    """
    This backend is used where there is a concept of a header/impl seperation (eg C/C++/ObjC).
    """
    def __init__(self, *args, **kwargs):
        super(TwoFilesLayout, self).__init__(*args, **kwargs)
        self.header_filename = self.backendConfig.get("HEADER_OUTPUT") or None
        self.impl_filename = self.backendConfig.get("IMPL_OUTPUT") or None
        assert self.header_filename is not None, "HEADER_OUTPUT variable MUST be specified in the backend config.  This is the file to the generated header code for all nodes will be written to."
        assert self.impl_filename is not None, "IMPL_OUTPUT variable MUST be specified in the backend config.  This is the file to the generated impl code for all nodes will be written to."
        self.header_template_path = self.backendConfig.get("HEADER_TEMPLATE") or DEFAULT_TWOFILES_HEADER_TEMPLATE 
        self.impl_template_path = self.backendConfig.get("IMPL_TEMPLATE") or DEFAULT_TWOFILES_IMPL_TEMPLATE 
        self.header_template = utils.load_template(self.header_template_path)
        self.impl_template = utils.load_template(self.impl_template_path)


    def generationStarted(self, nodelist):
        """
        Called before starting node generation for any of the nodes.
        """
        print "Writing header to: ", self.header_filename
        self.header_file = self.openOutputFile(self.header_filename)
        print "Writing impl to: ", self.impl_filename
        self.impl_file = self.openOutputFile(self.impl_filename)

    def generationFinished(self, nodelist):
        """
        Called after the code generation of all nodes has completed.
        """
        # write the "conclusion" after the nodes are generated
        self.header_file.close()
        self.impl_file.close()

    def renderNodes(self, nodelist):
        self.header_file.write(self.header_template.render(nodelist = nodelist, 
                                                           layout = self,
                                                           platform = self.platformBackend,
                                                           no_impl = True,
                                                           backendConfig = self.backendConfig))
        self.impl_file.write(self.impl_template.render(nodelist = nodelist,
                                                       layout = self,
                                                       backendConfig = self.backendConfig,
                                                       platform = self.platformBackend))

class OneFilePerNodeLayout(astgen.ASTLayout):
    def __init__(self, *args, **kwargs):
        super(OneFilePerNodeLayout, self).__init__(*args, **kwargs)

class TwoFilesPerNodeLayout(astgen.ASTLayout):
    """
    This backend is used where there is a concept of a header/impl seperation (eg C/C++/ObjC).
    """
    def __init__(self, *args, **kwargs):
        super(TwoFilesPerNodeLayout, self).__init__(*args, **kwargs)
        self.fwddefs_filename = self.backendConfig.get("FWDDEFS_OUTPUT", DEFAULT_FWDDEFS_OUTPUT)
        self.public_filename = self.backendConfig.get("PUBLIC_OUTPUT", DEFAULT_PUBLIC_OUTPUT)
        self.enums_filename = self.backendConfig.get("ENUMS_OUTPUT", DEFAULT_ENUMS_OUTPUT)

        self.fwddefs_template_path = self.backendConfig.get("FWDDEFS_TEMPLATE") or DEFAULT_FWDDEFS_TEMPLATE
        self.public_template_path = self.backendConfig.get("PUBLIC_TEMPLATE") or DEFAULT_PUBLIC_TEMPLATE
        self.enums_template_path = self.backendConfig.get("ENUMS_TEMPLATE") or DEFAULT_ENUMS_TEMPLATE

        self.fwddefs_template = utils.load_template(self.fwddefs_template_path)
        self.public_template = utils.load_template(self.public_template_path)
        self.enums_template = utils.load_template(self.enums_template_path)

        self.nodeHeader_template_path = self.backendConfig.get("NODE_HEADER_TEMPLATE", DEFAULT_TWOFILES_PER_NODE_HEADER_TEMPLATE)
        self.nodeImpl_template_path = self.backendConfig.get("IMPL_TEMPLATE", DEFAULT_TWOFILES_PER_NODE_IMPL_TEMPLATE)
        self.node_header_template = utils.load_template(self.nodeHeader_template_path)
        self.node_impl_template = utils.load_template(self.nodeImpl_template_path)

    def generationStarted(self, nodelist):
        """
        Called before starting node generation for any of the nodes.
        """
        # First create a single header file for all enums
        # we *could* do this as one file per enum but its an overkill
        # 
        # First create the "Fwds", "Enums" and "Main" header files
        print "Writing forward defs to: ", self.fwddefs_filename
        print "Writing public includes to: ", self.public_filename
        print "Writing enums includes to: ", self.enums_filename

        self.fwddefs_file = self.openOutputFile(self.fwddefs_filename)
        self.public_file = self.openOutputFile(self.public_filename)
        self.enums_file = self.openOutputFile(self.enums_filename)

        self.fwddefs_file.write(self.fwddefs_template.render(nodelist = nodelist,
                                                             layout = self,
                                                             backendConfig = self.backendConfig,
                                                             platform = self.platformBackend))
        self.public_file.write(self.public_template.render(nodelist = nodelist,
                                                           layout = self,
                                                           backendConfig = self.backendConfig,
                                                           platform = self.platformBackend))
        self.enums_file.write(self.enums_template.render(nodelist = nodelist,
                                                         layout = self,
                                                         backendConfig = self.backendConfig,
                                                         platform = self.platformBackend))

    def headerFilenameForNode(self, node):
        if "headerFilenameForNode" in self.backendConfig:
            return self.backendConfig["headerFilenameForNode"](node)
        else:
            return node.nodeName() + "_Header"

    def implFilenameForNode(self, node):
        if "implFilenameForNode" in self.backendConfig:
            return self.backendConfig["implFilenameForNode"](node)
        else:
            return node.nodeName() + "_Impl"

    def generationFinished(self, nodelist):
        """
        Called after the code generation of all nodes has completed.
        """
        # write the "conclusion" after the nodes are generated
        self.fwddefs_file.close()
        self.public_file.close()
        self.enums_file.close()

    def nodeStarted(self, node):
        """
        Called before the generation of code for a particular node.
        """
        self.current_node = node
        self.node_header_file = self.openOutputFile(self.headerFilenameForNode(node))
        self.node_impl_file = self.openOutputFile(self.implFilenameForNode(node))
        print "Writing node to: ", self.headerFilenameForNode(node), self.implFilenameForNode(node)

    def renderNode(self, node):
        self.node_header_file.write(self.node_header_template.render(node = node,
                                                                     layout = self,
                                                                     no_impl = True,
                                                                     backendConfig = self.backendConfig,
                                                                     platform = self.platformBackend))
        self.node_impl_file.write(self.node_impl_template.render(node = node,
                                                                 layout = self,
                                                                 backendConfig = self.backendConfig,
                                                                 platform = self.platformBackend))

    def nodeFinished(self, node):
        """
        Called after the generation of code for a particular node.
        """
        self.node_header_file.close()
        self.node_impl_file.close()
        self.node_header_file = self.node_impl_file = self.current_node = None

