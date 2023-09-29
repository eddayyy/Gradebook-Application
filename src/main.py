# Author: Eduardo Nunez
# Author email: eduardonunez.eng@gmail.com
import sys
from PyQt5 import QtWidgets

from gradebook import Gradebook


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    with open('src/stylesheet.css', mode='r') as css:
        app.setStyleSheet(css.read())

    MainWindow = QtWidgets.QMainWindow()
    MainWindow.show()
    ui = Gradebook()
    ui.setupUi(MainWindow)
    sys.exit(app.exec_())
