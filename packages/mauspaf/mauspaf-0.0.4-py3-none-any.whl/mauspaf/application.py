import sys
from PyQt5 import QtWidgets
# sys.path.insert(0, './src/mauspaf/')
from mauspaf.ui.mainwindow import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    app.exec_()


if __name__ == "__main__":
    main()
