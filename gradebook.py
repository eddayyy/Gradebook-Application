import csv
import sys
import numpy as np

from statistics_analysis import StatisticalAnalysis
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt


class Gradebook(object):
    def __init__(self):
        self.output = 'exported_student_data.csv'
        self.prev_selected_row = -1  # Initialize to -1 as no row is selected initially

    # ------------------- Setup/UI Initialization Methods -------------------
    def __init__(self):
        self.output = 'exported_student_data.csv'
        self.prev_selected_row = -1  # Initialize to -1 as no row is selected initially

    def setupUi(self, MainWindow):
        self.initializeMainWindow(MainWindow)
        central_widget = QtWidgets.QWidget(MainWindow)
        main_layout = QtWidgets.QVBoxLayout(central_widget)  # Main layout

        # Import / Export Buttons
        self.setupFileToolbar(MainWindow, main_layout)
        # Add, Delete, and Search Buttons
        self.setupStudentToolbar(MainWindow, main_layout)
        # Search Text Entry
        self.setupSearchLayout(main_layout)
        # Data Representation
        self.setupTable(main_layout)
        # Initialize StatisticalAnalysis class
        self.initStats()

        MainWindow.setCentralWidget(central_widget)

    def initializeMainWindow(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setWindowTitle("My Gradebook")

    def setupFileToolbar(self, MainWindow, main_layout):
        file_toolbar = QtWidgets.QToolBar("File Operations", MainWindow)
        MainWindow.addToolBar(file_toolbar)

        # Import Button
        import_action = QtWidgets.QAction("Import Data", MainWindow)
        import_action.triggered.connect(self.read_in)
        file_toolbar.addAction(import_action)

        # Export Button
        export_action = QtWidgets.QAction('Export Data', MainWindow)
        export_action.triggered.connect(self.write_out)
        file_toolbar.addAction(export_action)

    def setupStudentToolbar(self, MainWindow, main_layout):
        student_toolbar = QtWidgets.QToolBar("Student Operations", MainWindow)
        MainWindow.addToolBar(student_toolbar)

        # Add Button
        add_action = QtWidgets.QAction("Add Student", MainWindow)
        add_action.triggered.connect(self.add_student)
        student_toolbar.addAction(add_action)

        # Delete Button
        delete_action = QtWidgets.QAction("Delete Student", MainWindow)
        delete_action.triggered.connect(self.delete_student)
        student_toolbar.addAction(delete_action)

        # Search Button
        stat_action = QtWidgets.QAction('Statistical Analysis', MainWindow)
        stat_action.triggered.connect(self.displayStats)
        student_toolbar.addAction(stat_action)

    def setupSearchLayout(self, main_layout):
        # Search Text Entry
        search_layout = QtWidgets.QHBoxLayout()
        self.searchLineEdit = QtWidgets.QLineEdit()
        self.searchLineEdit.setAlignment(Qt.AlignRight)  # Right-align text
        self.searchLineEdit.setLayoutDirection(
            Qt.RightToLeft)  # Set layout direction to RTL
        search_layout.addWidget(self.searchLineEdit)

        self.searchButton = QtWidgets.QPushButton("Search by SID")
        self.searchButton.clicked.connect(self.search_by_sid)
        search_layout.addWidget(self.searchButton)

        main_layout.addLayout(search_layout)

    def setupTable(self, main_layout):
        # Table Data
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

        bold_font = QFont()
        bold_font.setBold(True)
        self.tableWidget.horizontalHeader().setFont(bold_font)

        self.tableWidget.itemChanged.connect(self.on_item_changed)
        main_layout.addWidget(self.tableWidget)

    def initStats(self):
        self.statAnalysis = StatisticalAnalysis(
            self.tableWidget  # Pass the tableWidget object
        )

    def displayStats(self):
        self.statAnalysis.displayWindow()

    # ------------------- Mathematical/Calculation Methods -------------------

    def calculate_student_grades(self):
        for row_index in range(self.tableWidget.rowCount()):
            scores = self.retrieve_scores(row_index)
            hw_average, quiz_average = self.calculate_averages(scores)
            final_score = self.calculate_final_score(
                hw_average, quiz_average, scores)
            grade = self.determine_final_grade(final_score)
            self.update_table_with_grades(row_index, final_score, grade)

    def retrieve_scores(self, row_index):
        scores = {'HW': [], 'Quiz': [], 'Midterm': 0, 'Final': 0}

        # For Homework and Quiz scores
        for i in range(4, 11):  # Columns 4 to 10 inclusive
            item = self.tableWidget.item(row_index, i)
            if item:
                value = item.text()
                if value:  # Check if the text is not empty
                    try:
                        value = float(value)
                        if i < 7:  # Columns 4, 5, 6 for HW
                            scores['HW'].append(value)
                        else:  # Columns 7, 8, 9, 10 for Quiz
                            scores['Quiz'].append(value)
                    except ValueError:
                        continue  # Skip non-numeric values

        # For Midterm and Final scores
        for key, col in {'Midterm': 11, 'Final': 12}.items():
            item = self.tableWidget.item(row_index, col)
            if item:
                value = item.text()
                if value:  # Check if the text is not empty
                    try:
                        scores[key] = float(value)
                    except ValueError:
                        continue  # Skip non-numeric values

        return scores

    def calculate_averages(self, scores):
        hw_average = np.mean(scores['HW']) if scores['HW'] else 0
        quiz_average = np.mean(scores['Quiz']) if scores['Quiz'] else 0
        return hw_average, quiz_average

    def calculate_final_score(self, hw_average, quiz_average, scores):
        weights = {'HW': 0.2, 'Quiz': 0.2, 'Midterm': 0.3, 'Final': 0.3}
        final_score = (hw_average * weights['HW'] +
                       quiz_average * weights['Quiz'] +
                       scores['Midterm'] * weights['Midterm'] +
                       scores['Final'] * weights['Final'])
        return round(final_score, 2)

    def determine_final_grade(self, final_score):
        if final_score >= 90:
            return 'A'
        elif final_score >= 80:
            return 'B'
        elif final_score >= 70:
            return 'C'
        elif final_score >= 60:
            return 'D'
        else:
            return 'F'

    def update_table_with_grades(self, row_index, final_score, grade):
        self.tableWidget.setItem(
            row_index, 13, QTableWidgetItem(f'{final_score}%'))
        self.tableWidget.setItem(row_index, 14, QTableWidgetItem(grade))

    # ------------------- Data Manipulation Methods -------------------
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
                    """
                    Set missing assignments as a dash '-'

                    IMPORTANT:
                    - Ensure proper formatting in the CSV file to avoid misinterpretation of missing assignments.
                    - If the CSV file does not leave commas to indicate missing assignments, the last assignment(s) 
                    will default to the '-' instead of the correct assignments.

                    Example of CSV Entry for Missing Assignments:
                   edu, 12314,John,Doe,jdoe@univ.,,10,100,90,60,100,80,68
                    (Keep commas when there are missing assignments / leave it blank)
                    """
                    cell_value = col_data if col_data else '-'
                    self.tableWidget.setItem(
                        row_index, col_index, QTableWidgetItem(str(cell_value)))
            self.calculate_student_grades()
        # Update the graph and statistics after importing data
        self.statAnalysis.updateStatisticsAndGraph()
        self.file_load = True

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

    # ------------------- Search and Display Methods -------------------
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
                    self.tableWidget, "Student Search", f"Student with SID {sid} has been found!")

                self.tableWidget.setRowHeight(
                    row_index, self.tableWidget.rowHeight(row_index) + 10)

                # Update the index of the currently selected row
                self.prev_selected_row = row_index
                return
        QMessageBox.information(
            self.tableWidget, "Student Search", f"Student with SID {sid} was NOT found!")
        return

    # ------------------- Event Handling Methods -------------------

    def on_item_changed(self, item):
        # Check if the changed item is in a grade column
        if item.column() in range(4, 13):  # Columns 4 to 12 inclusive are grade columns
            self.calculate_student_grades()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Gradebook()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
