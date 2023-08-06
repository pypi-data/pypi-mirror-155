from PyQt5 import QtGui, QtCore, QtWidgets

from mauspaf.generated.aboutwindow import Ui_Dialog


class AboutWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.exec_()
