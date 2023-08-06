""" Functions for the mass library window (DockWidget) of MauSPAF

"""

import mauspaf.masslibrary.solids as solids
import mauspaf.masslibrary.aircraft as aircraft

# Functions in masslibrary GUI
ML_FUNCTIONS = [
    ['ID', 'Function', 'Priority'],
    ['1', "solids.hollow_cylinder", ["t", "s", "v", "m", "rho", "le", "ri",
                                     "ro", "di", "do", "ix", "iy", "iz"]],
    ['2', "solids.cylinder_full", ["ix", "iy", "iz", "s", "v", "m", "rho",
                                   "le", "r", "d"]],
    ['3', "aircraft.ga_wing_raymer", ["ar", "mdg", "mf", "nz", "phi", "qc",
                                      "s", "tc", "tr", "mw"]],
    ['4', "solids.cube", ["ix", "iy", "iz", "s", "v", "m", "rho", "a"]],
    ['5', "solids.rectangular_prism", ["ix", "iy", "iz", "s", "v", "m", "rho",
                                       "a", "b", "h"]],
    ['6', "solids.sphere", ["ix", "iy", "iz", "s", "v", "m", "rho", "r", "d"]],
    ['7', "solids.hollow_sphere", ["ix", "iy", "iz", "s", "v", "m", "rho", "t",
                                   "ri", "di", "ro", "do"]]]


def update_frame(self, mo_id, symbols):
    """ Function used to update the line edit values in a mass library frame

    Args:
        mo_id (int): ID of the mass object to be calculated
        symbols (list): list of symbols used in the given object

    """
    func_dict = {int(ids): funct for ids, funct, _ in ML_FUNCTIONS[1:]}

    # Read values und units from lineedits and comboboxes
    values_dict = {}
    units_dict = {}
    for i in symbols:
        values_dict[str(i)] = eval(
            f"float(self.ui.le_{mo_id}_{i}.text())"
            + f" if self.ui.pb_{mo_id}_{i}.isChecked() else None")
        i_combobox = eval(f"self.ui.cb_{mo_id}_{i}")
        cb_text = i_combobox.currentText()
        units_dict[str(i)] = None if cb_text == "" else cb_text

    # Calculate new values
    command = func_dict[mo_id] + "(" \
        + ", ".join([f"{i}=values_dict['{i}']" for i in symbols]) \
        + f", units={units_dict})"
    res = eval(command)

    # Write calculated values
    for i in symbols:
        i_pushbutton = eval(f"self.ui.pb_{mo_id}_{i}")
        if not i_pushbutton.isChecked():
            i_lineedit = eval(f"self.ui.le_{mo_id}_{i}")
            i_value = res[str(i)]
            i_lineedit.setText(str(i_value))
        else:
            pass
        # eval(f"self.ui.le_{mo_id}_{i}"
        #      + f".setText(str(res['{i}'])) if not self.ui.pb_"
        #      + f"{mo_id}_{i}.isChecked() else True")
