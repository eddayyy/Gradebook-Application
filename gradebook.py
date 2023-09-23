import csv
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtGui import QColor


class Gradebook(object):
    def __init__(self):
        self.output = 'exported_student_data.csv'
        self.prev_selected_row = -1  # Initialize to -1 as no row is selected initially

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setWindowTitle("My Gradebook")

        # Central Widget
        central_widget = QtWidgets.QWidget(MainWindow)
        main_layout = QtWidgets.QGridLayout(central_widget)  # Main layout

        # Buttons Layout
        buttons_layout = QtWidgets.QHBoxLayout()

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

        # Search Button and Line Edit
        self.searchLineEdit = QtWidgets.QLineEdit()
        self.searchButton = QtWidgets.QPushButton("Search by SID")
        self.searchButton.clicked.connect(self.search_by_sid)
        buttons_layout.addWidget(self.searchLineEdit)
        buttons_layout.addWidget(self.searchButton)

        # Add buttons layout to the main layout at the top
        main_layout.addLayout(buttons_layout, 0, 0, 1, 2)

        # Table
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(15)
        self.tableWidget.setHorizontalHeaderLabels([
            'SID', 'FirstName', 'LastName', 'Email',
            'HW1', 'HW2', 'HW3', 'Quiz1', 'Quiz2',
            'Quiz3', 'Quiz4', 'MidtermExam', 'FinalExam',
            'Final Score', 'Final Grade'
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

        with open('Student_data.csv', mode='r') as f:
            csv_readin = csv.reader(f)
            next(csv_readin)  # Skip the header row
            for row_index, row_data in enumerate(csv_readin):
                self.tableWidget.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    self.tableWidget.setItem(
                        row_index, col_index, QTableWidgetItem(str(col_data)))
            self.calculate_student_grades()

    def write_out(self):
        with open(self.output, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['SID', 'FirstName', 'LastName', 'Email', 'HW1', 'HW2',
                            'HW3', 'Quiz1', 'Quiz2', 'Quiz3', 'Quiz4', 'MidtermExam', 'FinalExam',
                             'FinalScore', 'FinalGrade'])
            for row_index in range(self.tableWidget.rowCount()):
                row_data = []
                for col_index in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row_index, col_index)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)

    def add_student(self):
        self.reset_search()
        row_position = self.tableWidget.rowCount()
        select_indeces = self.tableWidget.insertRow(row_position)

    def delete_student(self):
        self.reset_search()
        select_indices = self.tableWidget.selectionModel().selectedRows()
        for index in sorted(select_indices, reverse=True):
            self.tableWidget.removeRow(index.row())

    def calculate_student_grades(self):
        weights = {
            'HW': 0.2,  # 20%
            'Quiz': 0.2,  # 20%
            'Midterm': 0.3,  # 30%
            'Final': 0.3  # 30%
        }

        for row_index in range(self.tableWidget.rowCount()):
            scores = {
                'HW': [float(self.tableWidget.item(row_index, i).text()) for i in range(4, 7)],
                'Quiz': [float(self.tableWidget.item(row_index, i).text()) for i in range(7, 11)],
                'Midterm': float(self.tableWidget.item(row_index, 11).text()),
                'Final': float(self.tableWidget.item(row_index, 12).text())
            }

            hw_average = sum(scores['HW']) / len(scores['HW'])
            quiz_average = sum(scores['Quiz']) / len(scores['Quiz'])

            final_score = (hw_average * weights['HW'] +
                           quiz_average * weights['Quiz'] +
                           scores['Midterm'] * weights['Midterm'] +
                           scores['Final'] * weights['Final'])

            final_score = round(final_score, 2)

            if final_score >= 90:
                grade = 'A'
            elif final_score >= 80:
                grade = 'B'
            elif final_score >= 70:
                grade = 'C'
            elif final_score >= 60:
                grade = 'D'
            elif final_score >= 50:
                grade = 'F'

            self.tableWidget.setItem(
                row_index, 13, QTableWidgetItem(f'{str(final_score)}%'))
            self.tableWidget.setItem(row_index, 14, QTableWidgetItem(grade))

    def reset_search(self):
        # Reset the properties of the previously selected row
        if self.prev_selected_row != -1:
            default_color = QColor("white")  # Or whatever the default color is
            for col_index in range(self.tableWidget.columnCount()):
                self.tableWidget.item(
                    self.prev_selected_row, col_index).setBackground(default_color)
            self.tableWidget.setRowHeight(
                self.prev_selected_row, self.tableWidget.rowHeight(self.prev_selected_row) - 10)

    def search_by_sid(self):
        sid = self.searchLineEdit.text()
        self.tableWidget.clearSelection()
        self.reset_search()
        for row_index in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_index, 0)
            if item and item.text() == str(sid):
                self.tableWidget.selectRow(row_index)
                self.tableWidget.scrollToItem(
                    self.tableWidget.item(row_index, 0))

                highlight_color = QColor("yellow")
                for col_index in range(self.tableWidget.columnCount()):
                    self.tableWidget.item(
                        row_index, col_index).setBackground(highlight_color)

                QMessageBox.information(
                    self.tableWidget, "Student Found", f"Student with SID {sid} has been found!")

                self.tableWidget.setRowHeight(
                    row_index, self.tableWidget.rowHeight(row_index) + 10)

                # Update the index of the currently selected row
                self.prev_selected_row = row_index
                return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Gradebook()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
