# Functionality Imports
from basic_check_tool import *


# GUI imports
from PySide2.QtCore import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import pymel.core.uitypes as uit

# Paths
SCRIPT_PATH = os.path.split(__file__)[0]
UI_PATH = os.path.normpath(SCRIPT_PATH + "/../ui/")


class BasicCheckToolUI(MayaQWidgetDockableMixin, QDialog):

    def __init__(self, parent=None):
        super(BasicCheckToolUI, self).__init__(parent=parent)

        # Create tool window UI
        self.main_layout = QVBoxLayout(self)
        self.__load_ui_file(self.main_layout)
        self.findButton.clicked.connect(self.on_find_button_clicked)

        self.setWindowTitle("Basic Check Tool")

    def __load_ui_file(self, main_layout):
        loader = QUiLoader()

        ui_file = QFile(UI_PATH + "/check_tool.ui")
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, parentWidget=self)
        ui_file.close()

        # save references to important UI elements
        self.toolBox = ui.toolBox
        self.findButton = ui.findButton

        main_layout.addWidget(ui)

    def show_tool_window(self, tool_idx=0):
        self.toolBox.setCurrentIndex(tool_idx)
        self.show(dockable=True)

    def on_find_button_clicked(self):
        idx = self.toolBox.currentIndex()

        # Find non-manifold
        if idx == 0:
            check = self.findChild(QCheckBox, "checkBox_selectGeom")
            s = check.checkState() is Qt.Unchecked

            findNonManifoldObjects(select_objects=s)
            return
        # Find default material
        if idx == 1:
            check = self.findChild(QCheckBox, "checkBox_selectFaces")
            s = check.checkState() is Qt.Unchecked

            findDefaultShaded(select_objects=s)
            return
        # Find same name
        if idx == 2:
            rb = self.findChild(QRadioButton, "rb_sn_selection")

            findNameDuplicates(use_selection=rb.isChecked())
            return
        # Find empty groups
        if idx == 3:
            check = self.findChild(QCheckBox, "checkBox_casc")
            casc = check.checkState() is Qt.Checked

            check = self.findChild(QCheckBox, "checkBox_rm")
            rm = check.checkState() is Qt.Checked

            findEmptyGroups(include_cascading=casc, remove=rm)
            return


# Shelf Management
def setup_shelf(name="Basic_Checks"):
    # Do nothing if the shelf already exists
    if shelfLayout(name, ex=True):
        return

    plugin_loaded_cmd = "if not maya.cmds.pluginInfo('check_tool_plugin.py', q=True, loaded=True): " \
                        "maya.cmds.loadPlugin('check_tool_plugin.py');\n"

    # Create a new shelf in the Maya main window
    main_window_shelf = mel.eval("global string $gShelfTopLevel;$tmp_1=$gShelfTopLevel;")
    shelf = shelfLayout(name, parent=main_window_shelf)

    # Add Buttons to the shelf for each function
    b1 = uit.ShelfButton(shelfButton(parent=shelf))
    b1.setCommand(plugin_loaded_cmd + "maya.cmds.findNonManifoldObjects(selectObjects=True)")
    b1.setDoubleClickCommand(plugin_loaded_cmd + "maya.cmds.showBasicCheckWindow(toolIndex=0)")
    b1.setAnnotation("Find all objects with non-manifold geometry in the scene.")
    b1.setImage("icon_geometry.png")

    b2 = uit.ShelfButton(shelfButton(parent=shelf))
    b2.setCommand(plugin_loaded_cmd + "maya.cmds.findDefaultShaded(selectObjects=True)")
    b2.setDoubleClickCommand(plugin_loaded_cmd + "maya.cmds.showBasicCheckWindow(toolIndex=1)")
    b2.setAnnotation("Find all objects using the default material in the scene.")
    b2.setImage("icon_shader.png")

    b3 = uit.ShelfButton(shelfButton(parent=shelf))
    b3.setCommand(plugin_loaded_cmd + "maya.cmds.findNameDuplicates(useSelection=False)")
    b3.setDoubleClickCommand(plugin_loaded_cmd + "maya.cmds.showBasicCheckWindow(toolIndex=2)")
    b3.setAnnotation("Find all objects that have the same name in the scene.")
    b3.setImage("icon_names.png")

    b4 = uit.ShelfButton(shelfButton(parent=shelf))
    b4.setCommand(plugin_loaded_cmd + "maya.cmds.findEmptyGroups(includeCascading=True, remove=True)")
    b4.setDoubleClickCommand(plugin_loaded_cmd + "maya.cmds.showBasicCheckWindow(toolIndex=3)")
    b4.setAnnotation("Remove all empty groups in the scene.")
    b4.setImage("icon_groups.png")


def delete_shelf(name="Basic_Checks"):
    if shelfLayout(name, ex=True):
        deleteUI(name, layout=True)

