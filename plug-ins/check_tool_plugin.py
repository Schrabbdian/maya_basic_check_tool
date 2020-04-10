import sys
import sys
import os.path

import maya.api.OpenMaya as om
from tool_window import *


##########################################################
# Plug-in Commands
##########################################################
class FindNonManifold(om.MPxCommand):
    CmdName = 'findNonManifoldObjects'
    ShortFlag = '-so'
    LongFlag = '-selectObjects'
    FlagValue = True

    def __init__(self):
        ''' Constructor. '''
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        ''' Command execution. '''
        self.parseArguments(args)
        findNonManifoldObjects(select_objects=self.FlagValue)

    def parseArguments(self, args):
        syntax = self.syntaxCreator()
        argData = om.MArgParser(syntax, args)

        if argData.isFlagSet(self.ShortFlag):
            self.FlagValue = argData.flagArgumentBool(self.ShortFlag, 0)
        if argData.isFlagSet(self.LongFlag):
            self.FlagValue = argData.flagArgumentBool(self.LongFlag, 0)

    @staticmethod
    def cmdCreator():
        ''' Create an instance of our command. '''
        return FindNonManifold()

    @staticmethod
    def syntaxCreator():
        syntax = om.MSyntax()
        syntax.addFlag(FindNonManifold.ShortFlag, FindNonManifold.LongFlag, om.MSyntax.kBoolean)
        return syntax


class FindDefaultShaded(om.MPxCommand):
    CmdName = 'findDefaultShaded'
    ShortFlag = '-so'
    LongFlag = '-selectObjects'
    FlagValue = True

    def __init__(self):
        ''' Constructor. '''
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        ''' Command execution. '''
        self.parseArguments(args)
        findDefaultShaded(select_objects=self.FlagValue)

    def parseArguments(self, args):
        syntax = self.syntaxCreator()
        argData = om.MArgParser(syntax, args)

        if argData.isFlagSet(self.ShortFlag):
            self.FlagValue = argData.flagArgumentBool(self.ShortFlag, 0)
        if argData.isFlagSet(self.LongFlag):
            self.FlagValue = argData.flagArgumentBool(self.LongFlag, 0)

    @staticmethod
    def cmdCreator():
        ''' Create an instance of our command. '''
        return FindDefaultShaded()

    @staticmethod
    def syntaxCreator():
        syntax = om.MSyntax()
        syntax.addFlag(FindDefaultShaded.ShortFlag, FindDefaultShaded.LongFlag, om.MSyntax.kBoolean)
        return syntax


class FindNameDuplicates(om.MPxCommand):
    CmdName = 'findNameDuplicates'
    ShortFlag = '-us'
    LongFlag = '-useSelection'
    FlagValue = False

    def __init__(self):
        ''' Constructor. '''
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        ''' Command execution. '''
        self.parseArguments(args)
        findNameDuplicates(use_selection=self.FlagValue)

    def parseArguments(self, args):
        syntax = self.syntaxCreator()
        argData = om.MArgParser(syntax, args)

        if argData.isFlagSet(self.ShortFlag):
            self.FlagValue = argData.flagArgumentBool(self.ShortFlag, 0)
        if argData.isFlagSet(self.LongFlag):
            self.FlagValue = argData.flagArgumentBool(self.LongFlag, 0)

    @staticmethod
    def cmdCreator():
        ''' Create an instance of our command. '''
        return FindNameDuplicates()

    @staticmethod
    def syntaxCreator():
        syntax = om.MSyntax()
        syntax.addFlag(FindNameDuplicates.ShortFlag, FindNameDuplicates.LongFlag, om.MSyntax.kBoolean)
        return syntax


class FindEmptyGroups(om.MPxCommand):
    CmdName = 'findEmptyGroups'
    ShortFlags = ['-ic', '-rm']
    LongFlags = ['-includeCascading', '-remove']
    FlagValues = [True, False]

    def __init__(self):
        ''' Constructor. '''
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        ''' Command execution. '''
        self.parseArguments(args)
        findEmptyGroups(include_cascading=self.FlagValues[0], remove=self.FlagValues[1])

    def parseArguments(self, args):
        syntax = self.syntaxCreator()
        argData = om.MArgParser(syntax, args)

        if argData.isFlagSet(self.ShortFlags[0]):
            self.FlagValues[0] = argData.flagArgumentBool(self.ShortFlags[0], 0)

        if argData.isFlagSet(self.ShortFlags[1]):
            self.FlagValues[1] = argData.flagArgumentBool(self.ShortFlags[1], 0)

    @staticmethod
    def cmdCreator():
        ''' Create an instance of our command. '''
        return FindEmptyGroups()

    @staticmethod
    def syntaxCreator():
        syntax = om.MSyntax()
        syntax.addFlag(FindEmptyGroups.ShortFlags[0], FindEmptyGroups.LongFlags[0], om.MSyntax.kBoolean)
        syntax.addFlag(FindEmptyGroups.ShortFlags[1], FindEmptyGroups.LongFlags[1], om.MSyntax.kBoolean)
        return syntax


class ShowToolWindow(om.MPxCommand):
    CmdName = 'showBasicCheckWindow'
    ShortFlag = '-id'
    LongFlag = '-toolIndex'
    FlagValue = 0

    __window = None


    def __init__(self):
        ''' Constructor. '''
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        ''' Command execution. '''
        self.parseArguments(args)

        # Create a window if none exists
        if ShowToolWindow.__window is None:
            ShowToolWindow.__window = BasicCheckToolUI()

        ShowToolWindow.__window.show_tool_window(self.FlagValue)

    def parseArguments(self, args):
        syntax = self.syntaxCreator()
        argData = om.MArgParser(syntax, args)

        if argData.isFlagSet(self.ShortFlag):
            self.FlagValue = argData.flagArgumentInt(self.ShortFlag, 0)

    @staticmethod
    def cmdCreator():
        ''' Create an instance of our command. '''
        return ShowToolWindow()

    @staticmethod
    def syntaxCreator():
        syntax = om.MSyntax()
        syntax.addFlag(ShowToolWindow.ShortFlag, ShowToolWindow.LongFlag, om.MSyntax.kLong)
        return syntax


##########################################################
# Plug-in initialization
##########################################################

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass

# Initialize the plug-in
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)

    # Register Commands
    try:
        pluginFn.registerCommand(FindNonManifold.CmdName, FindNonManifold.cmdCreator, FindNonManifold.syntaxCreator)
        pluginFn.registerCommand(FindDefaultShaded.CmdName, FindDefaultShaded.cmdCreator, FindDefaultShaded.syntaxCreator)
        pluginFn.registerCommand(FindNameDuplicates.CmdName, FindNameDuplicates.cmdCreator, FindNameDuplicates.syntaxCreator)
        pluginFn.registerCommand(FindEmptyGroups.CmdName, FindEmptyGroups.cmdCreator, FindEmptyGroups.syntaxCreator)
        pluginFn.registerCommand(ShowToolWindow.CmdName, ShowToolWindow.cmdCreator, ShowToolWindow.syntaxCreator)
    except:
        sys.stderr.write("Failed to register commands.\n")
        raise

    # Create Shelf
    setup_shelf("BasicCheckTool")
    cmds.pluginInfo("check_tool_plugin.py", edit=True, autoload=True) # turn on auto-load by default

    print "Loaded Basic Check Tool plugin."


# Uninitialize the plug-in
def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)

    # Deregister Commands
    try:
        pluginFn.deregisterCommand(FindNonManifold.CmdName)
        pluginFn.deregisterCommand(FindDefaultShaded.CmdName)
        pluginFn.deregisterCommand(FindNameDuplicates.CmdName)
        pluginFn.deregisterCommand(FindEmptyGroups.CmdName)
        pluginFn.deregisterCommand(ShowToolWindow.CmdName)
    except:
        sys.stderr.write("Failed to deregister commands.\n")
        raise

    # Remove Shelf
    delete_shelf("BasicCheckTool")

    print "Unloaded Basic Check Tool plugin."
