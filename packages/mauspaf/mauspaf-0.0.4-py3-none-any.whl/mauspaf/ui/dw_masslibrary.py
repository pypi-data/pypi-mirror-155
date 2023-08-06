from PyQt5 import QtWidgets
import sympy as sym
import mauspaf
from mauspaf.generated.dw_masslibrary import Ui_DockWidget
import mauspaf.guifun.masslib as masslib
import mauspaf.masslibrary.solids as solids
import mauspaf.masslibrary.aircraft as aircraft
import mauspaf.masslibrary.misc as misc


class DW_MassLibrary(QtWidgets.QDockWidget):
    def __init__(self):
        super(DW_MassLibrary, self).__init__()
        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)
        # # # Initialise input sets
        formulas_list = mauspaf.guifun.masslib.ML_FUNCTIONS
        self.mass_formula_priority = {}
        self.mass_formula_symbols = {}
        self.mass_formula_status = {}
        self.mass_formula_sets = {}
        for i_id, i_fun, i_prio in formulas_list[1:]:
            i_idi = int(i_id)
            self.mass_formula_priority[i_idi] = [
                sym.sympify(x) for x in i_prio]
            self.mass_formula_symbols[i_idi] = set(
                self.mass_formula_priority[i_idi])
            self.mass_formula_status[i_idi] = {
                symbol: getattr(self.ui, "pb_" + str(i_idi) + "_"
                                + str(symbol)).isChecked()
                for symbol in self.mass_formula_symbols[i_idi]}
            self.mass_formula_sets[i_idi] = list(eval(
                i_fun + "(calc_mode='sets')"))
        # Show
        self.ui.stackedWidget.setCurrentIndex(8)
        self.show()

    def show_frame(self, item, column):
        if item.text(0) == 'Full' and item.parent().text(0) == 'Cylinder':
            self.ui.stackedWidget.setCurrentIndex(0)
        elif item.text(0) == 'Hollow' and item.parent().text(0) == 'Cylinder':
            self.ui.stackedWidget.setCurrentIndex(1)
        elif item.text(0) == 'Cube' and item.parent().text(0) == 'Solids':
            self.ui.stackedWidget.setCurrentIndex(3)
        elif item.text(0) == 'Raymer' and item.parent().text(0) == 'Wing' \
                and item.parent().parent().text(0) == 'GA-Aircraft':
            self.ui.stackedWidget.setCurrentIndex(2)
        elif item.text(0) == 'Rectangular prism':
            self.ui.stackedWidget.setCurrentIndex(5)
        elif item.text(0) == 'Full' and item.parent().text(0) == 'Sphere':
            self.ui.stackedWidget.setCurrentIndex(6)
        elif item.text(0) == 'Hollow' and item.parent().text(0) == 'Sphere':
            self.ui.stackedWidget.setCurrentIndex(7)
        elif item.childCount() > 0:
            self.ui.stackedWidget.setCurrentIndex(9)
        else:
            self.ui.stackedWidget.setCurrentIndex(4)
