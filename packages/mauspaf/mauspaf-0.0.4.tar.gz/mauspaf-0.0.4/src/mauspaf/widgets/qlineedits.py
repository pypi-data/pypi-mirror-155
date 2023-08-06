""" Custom extensions of QLineEdit for MausPAF's GUI
"""

from PyQt5 import QtCore, QtWidgets

import mauspaf
import mauspaf.guifun.masslib as masslib


class QLineEdit_MassLib(QtWidgets.QLineEdit):
    """ Custom lineedit for the mass library
    """
    def __init__(self, Form):
        super(QtWidgets.QLineEdit, self).__init__()
        self.setAlignment(QtCore.Qt.AlignRight)
        self.setText('0')
        self.textEdited.connect(self.recompute_values)

    def recompute_values(self):
        # Iterate parent to find DockWidget
        dw_masslib = self.parent()
        while not isinstance(dw_masslib,
                             (mauspaf.ui.dw_masslibrary.DW_MassLibrary)):
            dw_masslib = dw_masslib.parent()
        main_window = dw_masslib.parent()

        # Convert value in associated line edit
        try:
            _, eqnr, varn = self.objectName().split('_')
        except Exception:
            pass
        # Update values
        try:
            masslib.update_frame(dw_masslib, int(eqnr),
                                 dw_masslib.mass_formula_priority[int(eqnr)])
        except BaseException as error:
            main_window.ui.statusbar.showMessage(
                'Mass properties calculation: An exception occurred: {}'
                .format(error), 4000)
