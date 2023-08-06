from PyQt5 import QtWidgets

from mauspaf.generated.dl_partinfo import Ui_Dialog


class PartInfoWindow(QtWidgets.QDialog):
    def __init__(self, part_name='', mass_text='', cg_text=''):
        super(PartInfoWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.tl_title.setText(part_name)
        self.ui.tl_mass_text.setText(mass_text)
        self.ui.tl_cg_text.setText(cg_text)
        self.exec_()
