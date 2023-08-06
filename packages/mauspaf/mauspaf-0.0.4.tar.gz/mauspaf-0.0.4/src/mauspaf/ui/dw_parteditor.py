from PyQt5 import QtGui, QtCore, QtWidgets
from mauspaf.generated.dw_parteditor import Ui_DockWidget


class DW_PartEditor(QtWidgets.QDockWidget):
    def __init__(self):
        super(DW_PartEditor, self).__init__()
        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)
        self.show()
