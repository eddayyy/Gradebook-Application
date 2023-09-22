import csv
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox


class Gradebook(object):
    def __init__(self):
        self.output = 'exported_student_data.csv'

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setWindowTitle("My Gradebook")

        # Central Widget
        central_widget = QtWidgets.QWidget(MainWindow)
        main_layout = QtWidgets.QGridLayout(central_widget)  # Main layout

        # Buttons Layout
        buttons_layout = QtWidgets.QHBoxLayout()  # Layout for the buttons

        # Import Button
        self.pushButton = QtWidgets.QPushButton("Import Data")
        self.pushButton.clicked.connect(self.read_in)
        buttons_layout.addWidget(self.pushButton)

        # Add Button
        self.addButton = QtWidgets.QPushButton("Add Student")
        self.addButton.clicked.connect(self.add_student)
        buttons_layout.addWidget(self.addButton)

        # Delete Button
        self.deleteButton = QtWidgets.QPushButton("Delete Student")
        self.deleteButton.clicked.connect(self.delete_student)
        buttons_layout.addWidget(self.deleteButton)

        # Export Button
        self.exportButton = QtWidgets.QPushButton('Export Data')
        self.exportButton.clicked.connect(self.write_out)
        buttons_layout.addWidget(self.exportButton)

        # Add buttons layout to the main layout at the top
        main_layout.addLayout(buttons_layout, 0, 0, 1, 2)

        # Table
        self.tableWidget = QtWidgets.QTableWidget()
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

        # Add table to the main layout below the buttons
        main_layout.addWidget(self.tableWidget, 1, 0, 1, 2)

        MainWindow.setCentralWidget(central_widget)

    def read_in(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(
            None, "Open CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if not filePath:  # If no file is selected, return
            return

        # Confirmation Dialog
        if self.tableWidget.rowCount() != 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText(
                "Do you want to clear the existing data in the table?")
            msgBox.setWindowTitle("Confirmation")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Yes:
                # Clear the existing rows in the table
                self.tableWidget.setRowCount(0)

        with open(filePath, mode='r') as f:
            csv_readin = csv.reader(f)
            next(csv_readin)  # Skip the header row
            for row_index, row_data in enumerate(csv_readin):
                self.tableWidget.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    self.tableWidget.setItem(
                        row_index, col_index, QTableWidgetItem(str(col_data)))

    def write_out(self):
        with open(self.output, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['SID', 'FirstName', 'LastName', 'Email', 'HW1', 'HW2',  # Write the header before the data
                            'HW3', 'Quiz1', 'Quiz2', 'Quiz3', 'Quiz4', 'MidtermExam', 'FinalExam'])
            for row_index in range(self.tableWidget.rowCount()):
                row_data = []
                for col_index in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row_index, col_index)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)

    def add_student(self):
        row_position = self.tableWidget.rowCount()
        select_indeces = self.tableWidget.insertRow(row_position)

    def delete_student(self):
        select_indices = self.tableWidget.selectionModel().selectedRows()
        for index in sorted(select_indices, reverse=True):
            self.tableWidget.removeRow(index.row())

    def search_by_sid(self, sid):


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Gradebook()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
