from PyQt5 import QtCore, QtWidgets
import csv

import mauspaf
from mauspaf.generated.mainwindow import Ui_MainWindow
from mauspaf.ui.aboutwindow import AboutWindow
from mauspaf.ui.dw_maintree import DW_MainTree
from mauspaf.ui.dw_masslibrary import DW_MassLibrary
from mauspaf.ui.dw_parteditor import DW_PartEditor
from mauspaf.guifun import inner
from mauspaf.guifun import io

status_msg_time = 4000


class MainWindow(QtWidgets.QMainWindow):
    """ Main window for the MauSPAF GUI.
    """
    def __init__(self):
        _translate = QtCore.QCoreApplication.translate
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        #
        self.setWindowTitle(_translate("MainWindow",
                                       "MauSPAF " + str(mauspaf.__version__)))
        # - Dock widgets & toggle view
        # Main tree DW
        self.ui.mainTree = DW_MainTree()
        self.ui.mainTree.setObjectName("mainTree")
        self.ui.mainTree.setWindowTitle(_translate("MainWindow", "Main tree"))
        self.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.ui.mainTree)
        self.ui.actionMainTree = self.ui.mainTree.toggleViewAction()
        self.ui.actionMainTree.setObjectName("Main tree")
        self.ui.actionMainTree.setText(_translate("MainWindow", "Main tree"))
        self.ui.menuView.addAction(self.ui.actionMainTree)

        # Mass library DW
        self.ui.massLibrary = DW_MassLibrary()
        self.ui.massLibrary.setObjectName("massLibrary")
        self.ui.massLibrary.setWindowTitle(_translate("MainWindow",
                                                      "Mass library"))
        self.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.ui.massLibrary)
        self.ui.actionMassLibrary = self.ui.massLibrary.toggleViewAction()
        self.ui.actionMassLibrary.setObjectName("Mass library")
        self.ui.actionMassLibrary.setText(_translate("MainWindow",
                                                     "Mass library"))
        self.ui.menuView.addAction(self.ui.actionMassLibrary)

        # # Part editor DW
        # self.ui.partEditor = DW_PartEditor()
        # self.ui.partEditor.setObjectName("partEditor")
        # self.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.ui.partEditor)
        # self.ui.actionPartEditor = self.ui.partEditor.toggleViewAction()
        # self.ui.actionPartEditor.setObjectName("Mass library")
        # self.ui.actionPartEditor.setText(_translate("MainWindow",
        #                                             "Part Editor"))
        # self.ui.menuView.addAction(self.ui.actionPartEditor)

        # Tabify dock widgets
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas,
                            QtWidgets.QTabWidget.West)
        # self.tabifyDockWidget(self.ui.mainTree, self.ui.partEditor)
        self.tabifyDockWidget(self.ui.mainTree, self.ui.massLibrary)
        self.ui.mainTree.raise_()

    # Dialog calls
    def call_save_dialog(self):
        """ Saves currently opened file.
        """
        self.ui.statusbar.showMessage('Save function not yet implemented.'
                                      + ' Use "Save as..." instead.',
                                      status_msg_time)

    def call_save_as_dialog(self):
        """ Saves the main tree to a desired file.

        If no file extension is given, the default one (`*.mspf`) is used.
        """
        save_dialog = QtWidgets.QFileDialog()
        save_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        file_name = save_dialog.getSaveFileName(
            self, 'Save as... file', './',
            filter='Mauspaf Files(*.mspf);; All Files(*.*)')
        if file_name[1] == 'Mauspaf Files(*.mspf)' \
                and file_name[0][-5:] != '.mspf':
            file_path = file_name[0]+'.mspf'
        elif file_name[1] == 'Mauspaf Files(*.mspf)' \
                and file_name[0][-5:] == '.mspf':
            file_path = file_name[0]
        elif file_name[1] == 'All Files(*.*)':
            file_path = file_name[0]

        try:
            io.save2file(self.ui.mainTree.ui.tw_mainPartTree, file_path)
            self.ui.statusbar.showMessage('Tree saved to file '+file_path,
                                          status_msg_time)
        except BaseException as error:
            self.ui.statusbar.showMessage(
                'An exception occurred: {}'.format(error), status_msg_time)

    def call_open_dialog(self):
        """ Call dialog to open an `*.mspf` file.

        Its content gets loaded to the main tree.
        """
        open_dialog = QtWidgets.QFileDialog()
        open_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        file_name = open_dialog.getOpenFileName(
            self,
            'Open file', './',
            filter='Mauspaf Files(*.mspf);; All Files(*.*)')[0]
        if file_name == '':
            self.ui.statusbar.showMessage(
                'No file selected.', status_msg_time)
            return
        tree_table = []
        with open(file_name) as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                tree_table.append(row)
        read_tree = inner.table2qttree(tree_table)
        self.ui.mainTree.ui.tw_mainPartTree.clear()
        self.ui.mainTree.ui.tw_mainPartTree.addTopLevelItem(read_tree)
        iterator = QtWidgets.QTreeWidgetItemIterator(
            self.ui.mainTree.ui.tw_mainPartTree)
        while True:
            item = iterator.value()
            if item is not None:
                item.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
                    | QtCore.Qt.ItemIsDragEnabled
                    | QtCore.Qt.ItemIsUserCheckable
                    | QtCore.Qt.ItemIsEnabled)
                iterator += 1
            else:
                break
        self.ui.statusbar.showMessage('Tree read from file '+file_name,
                                      status_msg_time)

    def call_export_tree_dialog(self):
        """ Saves the main tree to a desired file as a python object.
        """
        export_dialog = QtWidgets.QFileDialog()
        export_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        file_name = export_dialog.getSaveFileName(
            self, 'Save as... file', './',
            filter='Pickle object (*.pkl);; All Files(*.*)')[0]
        try:
            tree_object = inner.table2masstree(
                inner.qttree2table(
                    self.ui.mainTree.ui.tw_mainPartTree))
            io.export2file(tree_object, file_name)
            self.ui.statusbar.showMessage('Tree exported to file '+file_name,
                                          status_msg_time)
        except BaseException as error:
            self.ui.statusbar.showMessage(
                'An exception occurred: {}'.format(error), status_msg_time)

    # Window calls
    def call_about_window(self):
        AboutWindow()
        self.ui.statusbar.showMessage('About window has been closed.',
                                      status_msg_time)
