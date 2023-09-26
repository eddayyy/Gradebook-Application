import sys
from PyQt5 import QtWidgets

from gradebook import Gradebook


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.show()
    ui = Gradebook()
    ui.setupUi(MainWindow)
    sys.exit(app.exec_())
