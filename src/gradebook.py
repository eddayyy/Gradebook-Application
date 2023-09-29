# Author: Eduardo Nunez
# Author email: eduardonunez.eng@gmail.com
import csv

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QDialog,
    QFileDialog,
    QMessageBox,
    QTableWidgetItem,
)

from statistics_analysis import StatisticalAnalysis
from student_dialogue import StudentDialog


class Gradebook(object):
    # ------------------- Setup/UI Initialization Methods -------------------
    def __init__(self):
        self.output = 'exported_student_data.csv'
        self.table_backup = []

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
        MainWindow.setWindowIcon(QIcon("./media/Gradebook2.png"))
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setWindowTitle("Gradebook")

    def setupFileToolbar(self, MainWindow, main_layout):
        file_toolbar = QtWidgets.QToolBar("File Operations", MainWindow)
        MainWindow.addToolBar(file_toolbar)

        # Import Button
        import_action = QtWidgets.QAction("Import Data", MainWindow)
        import_action.triggered.connect(self.readIn)
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
        add_action.triggered.connect(self.addStudent)
        student_toolbar.addAction(add_action)

        # Delete Button
        delete_action = QtWidgets.QAction("Delete Student", MainWindow)
        delete_action.triggered.connect(self.deleteStudent)
        student_toolbar.addAction(delete_action)

        # Search Button
        stat_action = QtWidgets.QAction('Statistical Analysis', MainWindow)
        stat_action.triggered.connect(self.displayStats)
        student_toolbar.addAction(stat_action)

    def setupSearchLayout(self, main_layout):
        search_layout = QtWidgets.QHBoxLayout()

        # Search Button
        self.searchButton = QtWidgets.QPushButton("Search by SID")
        self.searchButton.clicked.connect(self.searchBySID)
        self.searchButton.clicked.connect(self.displaySearchClear)
        search_layout.addWidget(self.searchButton)

        # Search Text Entry
        self.searchLineEdit = QtWidgets.QLineEdit()
        self.searchLineEdit.setAlignment(Qt.AlignLeft)  # Right-align text
        self.searchLineEdit.setLayoutDirection(
            Qt.LeftToRight)  # Set layout direction to RTL
        self.searchLineEdit.returnPressed.connect(self.searchBySID)
        search_layout.addWidget(self.searchLineEdit)

        # X Button (Clear Search)
        self.clearSearch = QtWidgets.QPushButton('X')
        self.clearSearch.clicked.connect(self.onSearchClear)
        search_layout.addWidget(self.clearSearch)
        self.clearSearch.hide()

        main_layout.addLayout(search_layout)

    def setupTable(self, main_layout):
        # Table Data
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(15)
        self.tableWidget.setHorizontalHeaderLabels([
            'SID', 'First Name', 'Last Name', 'Email',
            'HW 1', 'HW 2', 'HW 3', 'Quiz 1', 'Quiz 2',
            'Quiz 3', 'Quiz 4', 'Midterm Exam', 'Final Exam',
            'Final Score', 'Final Grade'
        ])
        self.tableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked)

        # Table Modified
        self.tableWidget.itemChanged.connect(self.onItemChanged)

        # Table Headers
        bold_font = QFont()
        bold_font.setBold(True)
        self.tableWidget.horizontalHeader().setFont(bold_font)
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.sortColumns)

        main_layout.addWidget(self.tableWidget)

    def initStats(self):
        self.statAnalysis = StatisticalAnalysis(
            self.tableWidget  # Pass the tableWidget object
        )

    def displayStats(self):
        self.statAnalysis.displayWindow()
        self.statAnalysis.statAnalysis.activateWindow()
        self.statAnalysis.statAnalysis.raise_()

    # ------------------- Mathematical/Calculation Methods -------------------

    def calculateStudentGrades(self):
        for row_index in range(self.tableWidget.rowCount()):
            scores = self.retrieveScores(row_index)
            hw_average, quiz_average = self.calculateAverages(scores)
            final_score = self.calculateFinalScore(
                hw_average, quiz_average, scores)
            grade = self.determineFinalGrade(final_score)
            self.updateTableWithGrades(row_index, final_score, grade)

    def retrieveScores(self, row_index):
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

    def calculateAverages(self, scores):
        hw_average = np.mean(scores['HW']) if scores['HW'] else 0
        quiz_average = np.mean(scores['Quiz']) if scores['Quiz'] else 0
        return hw_average, quiz_average

    def calculateFinalScore(self, hw_average, quiz_average, scores):
        weights = {'HW': 0.2, 'Quiz': 0.2, 'Midterm': 0.3, 'Final': 0.3}
        final_score = (hw_average * weights['HW'] +
                       quiz_average * weights['Quiz'] +
                       scores['Midterm'] * weights['Midterm'] +
                       scores['Final'] * weights['Final'])
        return round(final_score, 2)

    def determineFinalGrade(self, final_score):
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

    def updateTableWithGrades(self, row_index, final_score, grade):
        self.tableWidget.setItem(
            row_index, 13, QTableWidgetItem(f'{final_score}%'))
        self.tableWidget.setItem(row_index, 14, QTableWidgetItem(grade))

    # ------------------- Data Manipulation Methods -------------------

    def readIn(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(
            None, "Open CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if not filePath:  # If no file is selected, return
            return

        # Confirmation message for the user to clear the Table when it's not empty
        if self.tableWidget.rowCount() != 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText(
                "Do you want to clear the existing data in the table?")
            msgBox.setWindowTitle("Confirmation")
            msgBox.setStandardButtons(
                QMessageBox.Yes | QMessageBox.No)  # User options

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Yes:
                self.tableWidget.setRowCount(0)  # Clear the table

        with open(filePath, mode='r') as f:
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
            self.calculateStudentGrades()
        # Update the graph and statistics after importing data
        self.statAnalysis.updateStatisticsAndGraph()
        self.file_load = True

    def write_out(self):
        # Prompt user to save file
        options = QFileDialog.Options()
        save_file = QFileDialog.getSaveFileName(  # Get the filepath and name
            None, "Save Student Data", '', "CSV Files (*.csv)", options=options
        )

        file_path = save_file[0]
        if not file_path:  # If no file name / path was provided
            return

        with open(file_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['SID', 'Firs Name', 'Last Name', 'Email', 'HW1', 'HW2',
                            'HW3', 'Quiz 1', 'Quiz 2', 'Quiz 3', 'Quiz 4', 'Midterm Exam', 'Final sExam',
                             'Final Score', 'Final Grade'])
            for row_index in range(self.tableWidget.rowCount()):
                row_data = []
                for col_index in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row_index, col_index)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)
        self.statAnalysis.exportHistogram()

    def addStudent(self):
        dialog = StudentDialog(self.tableWidget)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            details_list = dialog.getDetails()
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

            # Populate the new row with the entered details
            for col_index, detail in enumerate(details_list):
                self.tableWidget.setItem(row_position, col_index, QTableWidgetItem(
                    detail) if detail else QTableWidgetItem('-'))

            # Check if any of the first four details are missing
            if any(not detail for detail in details_list[:4]):
                QMessageBox.information(self.tableWidget, "Add Student",
                                        "Incomplete Details Provided!\n"
                                        "The provided details have been added, but please note that some information is missing. "
                                        "Consider updating the student's information at your earliest convenience.")
            else:
                QMessageBox.information(
                    self.tableWidget, "Add Student", "Student Successfully Added")

    def deleteStudent(self):
        select_indices = self.tableWidget.selectionModel().selectedRows()

        # If no rows are selected, display a message and return
        if not select_indices:
            QMessageBox.information(
                self.tableWidget, "Delete Student", "Please select a student to delete.")
            return

        # Confirmation Dialog before deleting
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText(
            "Are you sure you want to delete the selected student(s)?")
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes:  # If user confirms, delete the student
            for index in sorted(select_indices, reverse=True):
                # Remove from the table
                self.tableWidget.removeRow(index.row())
                # Remove from the backup (if present)
                if self.table_backup:
                    # Assuming SID is in the first column
                    sid = self.table_backup[index.row()][0]
                    self.table_backup = [
                        student for student in self.table_backup if student[0] != sid]

    def sortColumns(self, column):
        # Determine the sorting order (Ascending or Descending) based on the state of the table header.
        is_ascending = self.tableWidget.horizontalHeader(
        ).sortIndicatorOrder() == Qt.AscendingOrder

        # Initialize a list to store tuples of (row_index, value) where value is the content of the cell in the sorted column.
        items_with_index = []

        # Iterate over each row in the table and populate the items_with_index list.
        row_count = self.tableWidget.rowCount()
        for row_index in range(row_count):
            item = self.tableWidget.item(row_index, column)
            # Assign the text of the item to value if the item is not None, else assign '-'.
            value = item.text() if item else '-'

            # Attempt to convert the value to a float, if it fails, keep it as is (string).
            try:
                value = float(value)
            except ValueError:
                pass

            # Append the tuple (row_index, value) to the items_with_index list.
            items_with_index.append((row_index, value))

        # Sort the items_with_index list based on the value.
        # If value is '-', treat it as negative infinity to ensure it goes to the end/beginning of the list depending on the sorting order.
        items_with_index.sort(key=lambda x: float(
            '-inf') if x[1] == '-' else x[1], reverse=not is_ascending)

        # Initialize a list to store the rows in their new sorted order.
        # Each element of sorted_rows will be a list representing a row, where each element of that list is a QTableWidgetItem.
        sorted_rows = [None] * row_count

        # Populate the sorted_rows list with the items in their new sorted order.
        for new_index, (row_index, _) in enumerate(items_with_index):
            # For each tuple in items_with_index, create a new list in sorted_rows at the index corresponding to its sorted position.
            sorted_rows[new_index] = []

            # Iterate over each column in the table.
            for col_index in range(self.tableWidget.columnCount()):
                # For each cell in the row, take the item from its current position in the table.
                # The takeItem method retrieves and removes the item from the table.
                item = self.tableWidget.takeItem(row_index, col_index)

                # Append the item to the new list in sorted_rows, effectively moving the row to its new sorted position in sorted_rows.
                sorted_rows[new_index].append(item)

        # Now, sorted_rows contains all the rows in their sorted order, and the table is empty.
        # The next step is to place the sorted rows back into the table.
        for row_index, row_items in enumerate(sorted_rows):
            # Iterate over each list (representing a row) in sorted_rows.
            for col_index, item in enumerate(row_items):
                # For each item in the list, set the item back into its corresponding cell in the table.
                # This places each row back into the table in its sorted position.
                self.tableWidget.setItem(row_index, col_index, item)

    # ------------------- Search and Display Methods -------------------

    def backupTable(self):
        # Store the current state of the table
        self.table_backup = []
        for row_index in range(self.tableWidget.rowCount()):
            row_data = {}
            for col_index in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row_index, col_index)
                row_data[col_index] = item.text() if item else ""
            self.table_backup.append(row_data)

    def focusSearch(self, sid):
        self.backupTable()
        # Clear the table
        self.tableWidget.setRowCount(0)

        # Display only the searched student
        for row_data in self.table_backup:
            if row_data[0] == str(sid):  # Assuming SID is in the first column
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                for col_index, cell_value in row_data.items():
                    self.tableWidget.setItem(
                        row_position, col_index, QTableWidgetItem(cell_value))
                break

    def resetSearch(self):
        # Restore the table to its previous state
        self.tableWidget.setRowCount(0)

        for row_data in self.table_backup:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for col_index, cell_value in row_data.items():
                self.tableWidget.setItem(
                    row_position, col_index, QTableWidgetItem(cell_value))
        self.table_backup = []  # Clear the backup
        self.clearSearch.hide()
        self.searchLineEdit.setText('')

    def searchBySID(self):
        sid = self.searchLineEdit.text()
        if not sid:
            QMessageBox.information(
                self.tableWidget, "Student Search", "Please enter a Student ID (SID) to search.")
            return
        self.focusSearch(sid)
        self.displaySearchClear()

    # ------------------- Event Handling Methods -------------------

    def onItemChanged(self, item):
        # Check if the changed item is in a grade column
        if item.column() in range(4, 13):  # Columns 4 to 12 inclusive are grade columns
            self.calculateStudentGrades()

    def displaySearchClear(self):
        self.clearSearch.show()

    def onSearchClear(self):
        self.searchLineEdit.setText('')
        self.resetSearch()
        self.clearSearch.hide()
