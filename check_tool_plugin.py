import sys
import maya.api.OpenMaya as om
from basic_check_tool import *

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


# command
class FindEmptyGroupsCmd(om.MPxCommand):
    kPluginCmdName = "findEmptyGroups"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return FindEmptyGroupsCmd()

    def doIt(self, args):
        findEmptyGroups(args)


# Initialize the plug-in
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
            FindEmptyGroupsCmd.kPluginCmdName, FindEmptyGroupsCmd.cmdCreator
        )
    except:
        sys.stderr.write(
            "Failed to register command: %s\n" % FindEmptyGroupsCmd.kPluginCmdName
        )
        raise


# Uninitialize the plug-in
def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(FindEmptyGroupsCmd.kPluginCmdName)
    except:
        sys.stderr.write(
            "Failed to unregister command: %s\n" % FindEmptyGroupsCmd.kPluginCmdName
        )
        raise