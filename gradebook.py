import csv
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Gradebook(object):
    def __init__(self):
        self.input = 'Student_data.csv'
        self.output = 'processed_student_data.csv'

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 700)
        self.pushButton
        self.retranslateUi(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "My Gradebook"))

    def read_in(self):
        with open(self.input, mode='r') as f:
            csv_readin = csv.reader(f)
            for row_index, row_data in enumerate(csv_readin):
                # Assuming you have a table defined somewhere to insert rows
                self.table.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(col_data))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Gradebook()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
