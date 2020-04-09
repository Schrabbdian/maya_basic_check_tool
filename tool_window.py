# Functionality Imports
import sys
sys.path.append('F:/Development/Maya/Playerium_tests/basic_check_tool') # TEMPORARY
from basic_check_tool import *


# GUI imports
from PySide2.QtCore import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *

from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
from functools import partial

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import pymel.core.uitypes as uit


class BasicCheckToolUI(MayaQWidgetDockableMixin, QDialog):

    def __init__(self, parent=None):
        super(BasicCheckToolUI, self).__init__(parent=parent)

        self.main_layout = QVBoxLayout(self)
        self.__load_ui_file(self.main_layout)
        self.findButton.clicked.connect(self.on_find_button_clicked)

        self.shelf_buttons = {}
        self.__setup_shelf()

        print "stuff man"

    def __load_ui_file(self, main_layout):
        loader = QUiLoader()
        ui_file = QFile("F:/Development/Maya/Playerium_tests/basic_check_tool/check_tool.ui")
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, parentWidget=self)
        ui_file.close()

        # save references to important UI elements
        self.toolBox = ui.toolBox
        self.findButton = ui.findButton

        main_layout.addWidget(ui)


    def __setup_shelf(self, name="Basic Checks"):

        # Create a new shelf in the Maya main window
        main_window_shelf = mel.eval("global string $gShelfTopLevel;$tmp_1=$gShelfTopLevel;")
        self.shelf = shelf = shelfLayout(name, parent=main_window_shelf)

        # Add Buttons to the shelf for each function
        self.shelf_buttons["non-manifold"] = b1 = uit.ShelfButton(shelfButton(parent=shelf, command=findNonManifoldObjects))
        b1.setDoubleClickCommand(partial(self.__show_tool_window, 0))
        b1.setAnnotation("Find all objects with non-manifold geometry in the scene.")
        b1.setImage("load.png")

        self.shelf_buttons["default_shader"] = b2 = uit.ShelfButton(shelfButton(parent=shelf, command=findDefaultShaded))
        b2.setDoubleClickCommand(partial(self.__show_tool_window, 1))
        b2.setAnnotation("Find all objects using the default material in the scene.")
        b2.setImage("undo.png")

        self.shelf_buttons["same_name"] = b3 = uit.ShelfButton(shelfButton(parent=shelf, command=findNameDuplicates))
        b3.setDoubleClickCommand(partial(self.__show_tool_window, 2))
        b3.setAnnotation("Find all objects that have the same name in the scene.")
        b3.setImage("back.png")

        self.shelf_buttons["empty_groups"] = b4 = uit.ShelfButton(shelfButton(parent=shelf, command=findEmptyGroups))
        b4.setDoubleClickCommand(partial(self.__show_tool_window, 3))
        b4.setAnnotation("Find all empty groups in the scene.")
        b4.setImage("redo.png")

    def __show_tool_window(self, tool_idx=0):
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

    def __del__(self):
        print('Me ded')

    def __cleanup(self):
        # Delete all shelf buttons
        for b in self.shelf_buttons.values():
            deleteUI(b)

        # Delete shelf itself
        deleteUI(self.shelf)
