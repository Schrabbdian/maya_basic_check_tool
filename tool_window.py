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

import pymel.core.uitypes as uit


class BasicCheckToolUI:

    def __init__(self):

        self.__load_ui_file()
        self.findButton.clicked.connect(self.on_find_button_clicked)

        self.shelf_buttons = {}
        self.__setup_shelf()

        self.tool_window.show()

    @staticmethod
    def get_main_window():
        main_window_pointer = omui.MQtUtil.mainWindow()
        return wrapInstance(long(main_window_pointer), QWidget)

    def __load_ui_file(self):
        loader = QUiLoader()
        ui_file = QFile("F:/Development/Maya/Playerium_tests/basic_check_tool/testqt.ui")
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, parentWidget=self.get_main_window())
        ui_file.close()

        # save references to important UI elements
        assert isinstance(ui, QDialog)
        self.tool_window = ui
        assert isinstance(ui.toolBox, QToolBox)
        self.toolBox = ui.toolBox
        assert isinstance(ui.findButton, QPushButton)
        self.findButton = ui.findButton

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
        self.tool_window.show()


    def on_find_button_clicked(self):
        idx = self.toolBox.currentIndex()

        # Find non-manifold
        if idx == 0:
            findNonManifoldObjects()
            return
        # Find default material
        if idx == 1:
            findDefaultShaded()
            return
        # Find same name
        if idx == 2:
            assert isinstance(self.tool_window.rb_sn_selection, QRadioButton)
            rb = self.tool_window.rb_sn_selection

            findNameDuplicates(use_selection=rb.isChecked())
            return
        # Find empty groups
        if idx == 3:
            assert isinstance(self.tool_window.checkBox_casc, QCheckBox)
            check = self.tool_window.checkBox_casc
            casc = check.checkState() is Qt.Checked

            assert isinstance(self.tool_window.checkBox_rm, QCheckBox)
            check = self.tool_window.checkBox_rm
            rm = check.checkState() is Qt.Checked

            findEmptyGroups(include_cascading=casc, remove=rm)
            return

basic_tool = BasicCheckToolUI()
