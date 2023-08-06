""" Custom extensions of QComboBox for MauSPAF's GUI
"""


from PyQt5 import QtWidgets
from unitc import unit_conversion


class QComboBox_MassLibrary(QtWidgets.QComboBox):
    """ Custom combo box for the mass library
    """
    def __init__(self, Form):
        super(QtWidgets.QComboBox, self).__init__()

    def convert_le(self, new_unit):
        # Convert value in associated line edit (le)
        le_name = 'le' + self.objectName()[2:]
        try:
            le = self.parent().findChild(QtWidgets.QLineEdit, le_name)
            le_current_value = le.text()
            le_new_value = unit_conversion(float(le_current_value),
                                           self.unit, new_unit)
            le.setText(str(le_new_value))
            self.unit = new_unit
        except Exception:
            return


class QComboBox_Acceleration(QComboBox_MassLibrary):
    """ Custom combo box with acceleration units
    """
    def __init__(self, Form):
        super(QComboBox_MassLibrary, self).__init__()
        self.addItem("m/s²")
        self.addItem("ft/s²")
        self.unit = "m/s²"
        self.currentTextChanged.connect(self.convert_le)


class QComboBox_Angle(QComboBox_MassLibrary):
    """ Custom combo box with angle units
    """
    def __init__(self, Form):
        super(QComboBox_MassLibrary, self).__init__()
        self.addItem("rad")
        self.addItem("deg")
        self.unit = "rad"
        self.currentTextChanged.connect(self.convert_le)


class QComboBox_Area(QComboBox_MassLibrary):
    """ Custom combo box with area units
    """
    def __init__(self, Form):
        super(QComboBox_MassLibrary, self).__init__()
        self.addItem("m²")
        self.addItem("ft²")
        self.addItem("in²")
        self.unit = "m²"
        self.currentTextChanged.connect(self.convert_le)


class QComboBox_Density(QComboBox_MassLibrary):
    """ Custom combo box with density units
    """
    def __init__(self, Form):
        super(QComboBox_MassLibrary, self).__init__()
        self.addItem("kg/m³")
        self.addItem("g/cm³")
        self.addItem("lb/in³")
        self.addItem("lb/ft³")
        self.unit = "kg/m³"
        self.currentTextChanged.connect(self.convert_le)


class QComboBox_Distribution(QtWidgets.QComboBox):
    """ Custom combo box with distribution types for the
        UncertainValue class
    """
    def __init__(self, Form):
        super(QtWidgets.QComboBox, self).__init__()
        self.addItem("Constant")
        self.addItem("Uniform")
        self.addItem("Normal")
        self.addItem("Discrete")


class QComboBox_Inertia(QComboBox_MassLibrary):
    """ Custom combo box with mass moment of inertia units
    """
    def __init__(self, Form):
        super(QComboBox_MassLibrary, self).__init__()
        self.addItem("kg·m²")
        self.addItem("lb·ft²")  # Equivalent to "lbf·ft·s²"
        self.unit = "kg·m²"
        self.currentTextChanged.connect(self.convert_le)


class QComboBox_Length(QComboBox_MassLibrary):
    """ Custom combo box with length units
    """
    def __init__(self, Form):
        super(QComboBox_MassLibrary, self).__init__()
        self.addItem("m")
        self.addItem("cm")
        self.addItem("mm")
        self.addItem("ft")
        self.addItem("in")
        self.unit = "m"
        self.currentTextChanged.connect(self.convert_le)


class QComboBox_Mass(QComboBox_MassLibrary):
    """ Custom combo box with mass units
    """
    def __init__(self, Form):
        super(QComboBox_MassLibrary, self).__init__()
        self.addItem("kg")
        self.addItem("g")
        self.addItem("lb")
        self.addItem("oz")
        self.unit = "kg"
        self.currentTextChanged.connect(self.convert_le)


class QComboBox_Masstypes(QtWidgets.QComboBox):
    """ Custom combo box with the different mass types of a part
    """
    def __init__(self, Form):
        super(QtWidgets.QComboBox, self).__init__()
        self.addItem("Inherited")
        self.addItem("Estimated")
        self.addItem("Target")
        self.addItem("Budget")
        self.addItem("Custom")


class QComboBox_None(QComboBox_MassLibrary):
    """ Custom combo box for no units
    """
    def __init__(self, Form):
        super(QComboBox_MassLibrary, self).__init__()
        self.addItem("[unitless]")


class QComboBox_Pressure(QComboBox_MassLibrary):
    """ Custom combo box with pressure units
    """
    def __init__(self, Form):
        super(QComboBox_MassLibrary, self).__init__()
        self.addItem("Pa")
        self.addItem("MPa")
        self.addItem("psi")
        self.addItem("bar")
        self.addItem("atm")
        self.addItem("mmHg")
        self.addItem("lb/ft²")
        self.unit = "Pa"
        self.currentTextChanged.connect(self.convert_le)


class QComboBox_Speed(QComboBox_MassLibrary):
    """ Custom combo box with speed units
    """
    def __init__(self, Form):
        super(QComboBox_MassLibrary, self).__init__()
        self.addItem("m/s")
        self.addItem("kt")
        self.addItem("km/h")
        self.unit = "m/s"
        self.currentTextChanged.connect(self.convert_le)


class QComboBox_Volume(QComboBox_MassLibrary):
    """ Custom combo box with volume units
    """
    def __init__(self, Form):
        super(QComboBox_MassLibrary, self).__init__()
        self.addItem("m³")
        self.addItem("cm³")
        self.addItem("mm³")
        self.addItem("ft³")
        self.addItem("inch³")
        self.unit = "m³"
        self.currentTextChanged.connect(self.convert_le)
