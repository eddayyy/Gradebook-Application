import csv
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem


class Gradebook(object):
    def __init__(self):
        self.input = 'Student_data.csv'
        self.output = 'processed_student_data.csv'

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)

        # Import Button
        self.pushButton = QtWidgets.QPushButton(
            "Import Student Data", MainWindow)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 150, 40))
        self.pushButton.clicked.connect(self.read_in)
        # Add Button
        self.addButton = QtWidgets.QPushButton("Add Student", MainWindow)
        self.addButton.setGeometry(QtCore.QRect(170, 10, 150, 40))
        self.addButton.clicked.connect(self.add_student)

        # Delete Button
        self.deleteButton = QtWidgets.QPushButton("Delete Student", MainWindow)
        self.deleteButton.setGeometry(QtCore.QRect(330, 10, 150, 40))
        self.deleteButton.clicked.connect(self.delete_student)

        # Table
        self.tableWidget = QtWidgets.QTableWidget(MainWindow)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 1100, 700))
        self.tableWidget.setColumnCount(13)
        self.tableWidget.setHorizontalHeaderLabels([
            'SID', 'FirstName', 'LastName', 'Email',
            'HW1', 'HW2', 'HW3', 'Quiz1', 'Quiz2',
            'Quiz3', 'Quiz4', 'MidtermExam', 'FinalExam'
        ])

        self.tableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.AllEditTriggers)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        self.pushButton.setText("Import")
        MainWindow.setWindowTitle("My Gradebook")

    def read_in(self):
        with open(self.input, mode='r') as f:
            csv_readin = csv.reader(f)

            # Skip the header row
            next(csv_readin)

            for row_index, row_data in enumerate(csv_readin):
                self.tableWidget.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    self.tableWidget.setItem(
                        row_index, col_index, QTableWidgetItem(str(col_data)))

    def add_student(self):
        row_position = self.tableWidget.rowCount()
        select_indeces = self.tableWidget.insertRow(row_position)

    def delete_student(self):
        select_indices = self.tableWidget.selectionModel().selectedRows()
        for index in sorted(select_indices, reverse=True):
            self.tableWidget.removeRow(index.row())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Gradebook()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
