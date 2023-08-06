from PyQt5 import QtWidgets
import mauspaf
import sympy as sym


class QPushButton_MassLib(QtWidgets.QPushButton):
    """ Custom QPushButton for the mass library.
    """
    def __init__(self, Form):
        super(QtWidgets.QPushButton, self).__init__()
        self.setFlat(True)
        self.setCheckable(True)

        # Align left and prepend a space
        self.setStyleSheet("QPushButton { padding: 5px; text-align: left; }")
        self.toggled.connect(self.toggle_state)
        self.clicked.connect(self.update_inputs)

    def toggle_state(self):
        """ Change style and enable/disable related QLineEdit
        """
        # TODO: can the eqnr and var be saved as class arguments? Would be more
        #     efficient than calculating it every time again. Same in
        #     update_inputs function.
        try:
            _, eqnr, var = self.objectName().split('_')
        except Exception:
            pass

        if self.isChecked():
            # Change style
            self.setStyleSheet(
                "QPushButton { padding: 3px;"
                + " text-align: left; font-weight: bold; }")
            # Enable QLineEdit
            try:
                for x in self.parent().children():
                    if x.objectName() == '_'.join(['le', eqnr, var]):
                        x.setEnabled(True)
            except AttributeError:
                # Happens when the push button is initialized
                pass
        elif not self.isChecked():
            # Change style
            self.setStyleSheet(
                "QPushButton { padding: 3px; text-align: left; }")
            # Disable QLineEdit
            try:
                for x in self.parent().children():
                    if x.objectName() == 'le_' + eqnr + '_' + var:
                        x.setEnabled(False)
            except AttributeError:
                # Happens when the push button is initialized
                pass

    def update_inputs(self):
        """ Activate a new, valid combination of input variables

        After changing the state of the pushbutton, search for a new
        combination of valid inputs according to the current variables priority
        list, and change the other pushbuttons.

        """
        try:
            _, eqnr, var = self.objectName().split('_')
            eqnr = int(eqnr)
            sym_var = sym.sympify(var)
        except Exception:
            pass

        try:
            dw_masslib = self.parent()
            while not isinstance(dw_masslib,
                                 (mauspaf.ui.dw_masslibrary.DW_MassLibrary)):
                dw_masslib = dw_masslib.parent()
            main_window = dw_masslib.parent()
            changed_status = dw_masslib.mass_formula_status[eqnr].copy()
            changed_status[sym_var] = not(dw_masslib.mass_formula_status[eqnr][sym_var])
            dw_masslib.mass_formula_priority[eqnr].remove(sym_var)
            dw_masslib.mass_formula_priority[eqnr] += [sym_var]
            new_status = mauspaf.masslibrary.misc.status_changed(
                changed_status,
                dw_masslib.mass_formula_priority[eqnr],
                dw_masslib.mass_formula_sets[eqnr])
            for symbol in dw_masslib.mass_formula_symbols[eqnr]:
                str1 = f"dw_masslib.ui.pb_{eqnr}_{var}.isChecked()"
                if changed_status[symbol] != new_status[symbol]:
                    i_pb = eval(f"dw_masslib.ui.pb_{eqnr}_{symbol}")
                    i_pb.toggle()
            dw_masslib.mass_formula_status[eqnr] = new_status

        except Exception:
            pass


class QPushButton_MassLib_Enabled(QtWidgets.QPushButton):
    """ Custom QPushButton for the mass library.
    """
    def __init__(self, Form):
        super(QtWidgets.QPushButton, self).__init__()
        self.setFlat(True)
        self.setCheckable(False)
        self.setEnabled(True)

        # Align left and prepend a space
        self.setStyleSheet("QPushButton { padding: 5px; text-align:"
                           + " left; font-weight: bold; }")
        self.toggled.connect(self.toggle_state)


class QPushButton_MassLib_Disabled(QtWidgets.QPushButton):
    """ Custom QPushButton for the mass library.
    """
    def __init__(self, Form):
        super(QtWidgets.QPushButton, self).__init__()
        self.setFlat(True)
        self.setCheckable(False)
        self.setEnabled(False)

        # Align left and prepend a space
        self.setStyleSheet("QPushButton { padding: 5px; text-align: left; }")
        self.toggled.connect(self.toggle_state)
