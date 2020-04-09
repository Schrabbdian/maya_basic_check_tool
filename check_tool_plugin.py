import sys
import maya.api.OpenMaya as om
from tool_window import *


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


# Initialize the plug-in
def initializePlugin(plugin):
    print "Hai"

    basic_tool = BasicCheckToolUI()
    basic_tool.



# Uninitialize the plug-in
def uninitializePlugin(plugin):
    print "Bai"