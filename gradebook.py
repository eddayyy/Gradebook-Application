import csv
import sys

from statistics_analysis import StatisticalAnalysis
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt


class Gradebook(object):
    def __init__(self):
        self.output = 'exported_student_data.csv'
        self.prev_selected_row = -1  # Initialize to -1 as no row is selected initially

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setWindowTitle("My Gradebook")

        # Central Widget
        central_widget = QtWidgets.QWidget(MainWindow)
        main_layout = QtWidgets.QVBoxLayout(central_widget)  # Main layout

        # File Operations Toolbar
        file_toolbar = QtWidgets.QToolBar("File Operations", MainWindow)
        MainWindow.addToolBar(file_toolbar)

        # Import Action
        import_action = QtWidgets.QAction("Import Data", MainWindow)
        import_action.triggered.connect(self.read_in)
        file_toolbar.addAction(import_action)

        # Export Action
        export_action = QtWidgets.QAction('Export Data', MainWindow)
        export_action.triggered.connect(self.write_out)
        file_toolbar.addAction(export_action)

        # Student Operations Toolbar
        student_toolbar = QtWidgets.QToolBar("Student Operations", MainWindow)
        MainWindow.addToolBar(student_toolbar)

        # Add Student Action
        add_action = QtWidgets.QAction("Add Student", MainWindow)
        add_action.triggered.connect(self.add_student)
        student_toolbar.addAction(add_action)

        # Delete Student Action
        delete_action = QtWidgets.QAction("Delete Student", MainWindow)
        delete_action.triggered.connect(self.delete_student)
        student_toolbar.addAction(delete_action)

        # Search Layout
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

        # Statistical Analysis Action
        stat_action = QtWidgets.QAction('Statistical Analysis', MainWindow)
        stat_action.triggered.connect(self.displayStats)
        student_toolbar.addAction(stat_action)

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
        self.initStats()

        # Listen for changes to the table
        self.tableWidget.itemChanged.connect(self.on_item_changed)

        # Bold the Column Titles
        bold_font = QFont()
        bold_font.setBold(True)
        self.tableWidget.horizontalHeader().setFont(bold_font)

        # Add table to the main layout below the buttons
        main_layout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(central_widget)

    def initStats(self):
        self.statAnalysis = StatisticalAnalysis(
            self.tableWidget  # Pass the tableWidget object
        )

    def displayStats(self):
        self.statAnalysis.displayWindow()

    def on_item_changed(self, item):
        # Check if the changed item is in a grade column
        if item.column() in range(4, 13):  # Columns 4 to 12 inclusive are grade columns
            self.calculate_student_grades()

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

    def calculate_student_grades(self):
        weights = {
            'HW': 0.2,  # 20%
            'Quiz': 0.2,  # 20%
            'Midterm': 0.3,  # 30%
            'Final': 0.3  # 30%
        }

        for row_index in range(self.tableWidget.rowCount()):
            scores = {
                'HW': [],
                'Quiz': [],
                'Midterm': 0,
                'Final': 0
            }

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

            # Calculate averages and final score
            hw_average = sum(scores['HW']) / \
                len(scores['HW']) if scores['HW'] else 0
            quiz_average = sum(scores['Quiz']) / \
                len(scores['Quiz']) if scores['Quiz'] else 0

            final_score = (hw_average * weights['HW'] +
                           quiz_average * weights['Quiz'] +
                           scores['Midterm'] * weights['Midterm'] +
                           scores['Final'] * weights['Final'])

            final_score = round(final_score, 2)

            # Determine the final grade
            if final_score >= 90:
                grade = 'A'
            elif final_score >= 80:
                grade = 'B'
            elif final_score >= 70:
                grade = 'C'
            elif final_score >= 60:
                grade = 'D'
            else:
                grade = 'F'

            # Update the table with the final score and grade
            self.tableWidget.setItem(
                row_index, 13, QTableWidgetItem(f'{final_score}%'))
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
                    self.tableWidget, "Student Search", f"Student with SID {sid} has been found!")

                self.tableWidget.setRowHeight(
                    row_index, self.tableWidget.rowHeight(row_index) + 10)

                # Update the index of the currently selected row
                self.prev_selected_row = row_index
                return
        QMessageBox.information(
            self.tableWidget, "Student Search", f"Student with SID {sid} was NOT found!")
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Gradebook()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
