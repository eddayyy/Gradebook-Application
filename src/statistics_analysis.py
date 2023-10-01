# Author: Eduardo Nunez
# Author email: eduardonunez.eng@gmail.com

import statistics as st
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QComboBox,
    QVBoxLayout,
    QLabel,
    QWidget,
    QHBoxLayout,
    QMessageBox,
    QGridLayout
)
from PyQt5.QtGui import QIcon, QFont


class StatisticalAnalysis:
    def __init__(self, tableWidget):
        self.tableWidget = tableWidget
        self.pltMin = 0  # initially the histograms x axis will start from 0
        self.setupUI()

    # ------------------- Setup/UI Initialization Methods -------------------

    def setupUI(self):
        self.dataError = "No Available Data"

        self.initializeMainWindow()
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)  # Main layout is vertical

        # Horizontal layout for statistics, graph, and drop down menu (combo box)
        horizontal_layout = QHBoxLayout()

        # Create a Group Box for Statistics Display
        statistics_display_group_box = QtWidgets.QGroupBox(
            "Statistics")
        statistics_display_layout = QVBoxLayout(
            statistics_display_group_box)  # Sub layout is vertical
        self.setupStatisticsDisplay(statistics_display_layout)

        horizontal_layout.addWidget(statistics_display_group_box)

        # Create a Group Box for Graph Display
        graph_display_group_box = QtWidgets.QGroupBox("Graph")
        graph_display_layout = QVBoxLayout(graph_display_group_box)
        self.setupGraphDisplay(graph_display_layout)
        horizontal_layout.addWidget(graph_display_group_box)

        # Add horizontal layout to the main layout
        main_layout.addLayout(horizontal_layout)

        self.statAnalysis.setCentralWidget(central_widget)

    def initializeMainWindow(self):
        self.statAnalysis = QtWidgets.QMainWindow()
        self.statAnalysis.setObjectName('StatisticalAnalysisWindow')
        self.statAnalysis.setWindowIcon(
            QIcon("./media/StatisticalAnalysis.png"))
        self.statAnalysis.resize(1200, 700)
        self.statAnalysis.setWindowTitle('Statistical Analysis')

    def setupStatisticsDisplay(self, statistics_display_layout):
        # Create a QGridLayout
        grid_layout = QGridLayout()

        # Create and add a label and the QComboBox to the grid layout
        self.fieldLabel = QLabel("Fields:")
        self.comboBox = QComboBox()
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems([
            'HW1', 'HW2', 'HW3', 'Quiz1', 'Quiz2', 'Quiz3', 'Quiz4', 'MidtermExam', 'FinalExam', 'Course Grades'
        ])

        self.comboBox.currentIndexChanged.connect(
            self.updateStatisticsAndGraph)
        # Put the field label and dropdown menu side-by-side
        grid_layout.addWidget(self.fieldLabel, 0, 0)
        grid_layout.addWidget(self.comboBox, 0, 1)

        # Set up the statistics label
        self.statisticsLabel = QLabel()
        self.statisticsLabel.setObjectName("statisticsLabel")
        stat_font = QFont()
        stat_font.setPointSize(16)
        self.statisticsLabel.setFont(stat_font)
        # Add the statistics label to the grid layout
        # Add to row 1, span 2 columns
        grid_layout.addWidget(self.statisticsLabel, 1, 0, 1, 2)

        # Add the grid layout to the statistics display layout
        statistics_display_layout.addLayout(grid_layout)

    def setupGraphDisplay(self, graph_display_layout):
        self.figure, self.ax = plt.subplots()
        # FigureCanvas allows for the graph to be placed on the Qt Window by adding it to the layout
        self.canvas = FigureCanvas(self.figure)
        graph_display_layout.addWidget(self.canvas)
        # Create and setup Export All Graphs Button
        self.exportAllGraphsButton = QtWidgets.QPushButton("Export All Graphs")
        self.exportAllGraphsButton.clicked.connect(self.exportAllGraphs)
        graph_display_layout.addWidget(self.exportAllGraphsButton)

        self.customizeGraphAppearance()

    # ------------------- Mathematical/Calculation Methods -------------------

    def updateStatisticsAndGraph(self):
        # Check if the table is empty
        if self.tableWidget.rowCount() == 0:
            QMessageBox.information(
                self.statAnalysis, "No Data", "The table is empty. Please add data first.")
            return

        column_index = self.comboBox.currentIndex() + 4

        self.updateStatistics(column_index)
        self.updateGraph(column_index)

    def updateStatistics(self, column_index):
        # Calculate statistics

        mean = self.calculateStats(column_index, 'mean')
        std = self.calculateStats(column_index, 'std')
        median = self.calculateStats(column_index, 'median')
        mode = self.calculateStats(column_index, 'mode')
        passing, failing, passingRate, failingRate = self.passFailingRate(
            column_index)
        missing_assignments = self.getMissingAssignments(column_index)
        minVal, maxVal = self.getMinMax(column_index)
        self.pltMin = minVal

        # Structured and formatted statistics text
        statistics_text = (
            f"Maximum Score: {maxVal}\n"
            f"Minimum Score:{minVal}\n"
            f"Mean: {mean}\n"
            f"Standard Deviation: {std}\n"
            f"Median: {median}\n"
            f"Mode:{mode}\n"
            f"Passing: {passing} ({passingRate} of students)\n"
            f"Failing: {failing} ({failingRate} of students)\n"
            f"Missing Assignments/Grades: {missing_assignments}\n"
        )

        self.statisticsLabel.setText(statistics_text)

    def updateGraph(self, column_index):
        self.ax.clear()
        values = self.getValuesFromColumn(column_index)
        self.ax.hist(values, bins=(10), color='skyblue',
                     edgecolor='black', label='Grades')
        self.customizeGraphAppearance()
        self.canvas.draw()

    def customizeGraphAppearance(self):
        self.ax.set_title('Distribution of Student Grades',
                          fontsize=18, fontweight='bold', color='darkblue')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_xlabel('Student Grades', fontsize=16,
                           fontweight='bold', color='black')
        self.ax.set_ylabel('Student Count', fontsize=16,
                           fontweight='bold', color='black')
        self.ax.tick_params(axis='both', which='major',
                            labelsize=10, colors='darkred')
        # Set x-axis limits to represent grades
        self.ax.set_xlim([self.pltMin, 100])
        # Set y-axis limits to represent student count
        self.ax.set_ylim([0, 10])
        self.canvas.draw()

    def calculateStats(self, column_index, stat_type):
        # This function "dynamically" uses NumPy by taking advantage of the getattr function.
        # instead of calling np.function we can pass in the func we want to call each time and simplify the code
        values = self.getValuesFromColumn(column_index)
        if not values:  # If the list is empty, return None
            return self.dataError

        if stat_type == 'mode':
            return st.mode(values)  # calaculate mode

        stat_function = getattr(np, stat_type)  # "np.stat_type"
        return round(stat_function(values), 2)

    def passFailingRate(self, column_index):
        values = self.getValuesFromColumn(column_index)
        passing, failing = 0, 0
        if not values:
            return self.dataError, self.dataError, self.dataError, self.dataError
        for val in values:
            if val < 60:
                failing += 1
            else:
                passing += 1

        total = passing + failing

        passing_rate = passing / total
        failing_rate = failing / total

        passing_rate = f"{passing_rate * 100:.2f}%"
        failing_rate = f"{failing_rate * 100:.2f}%"
        return passing, failing, passing_rate, failing_rate

    # ------------------- Data Retrieval Methods -------------------

    def getValuesFromColumn(self, column_index):
        values = []
        row_count = self.tableWidget.rowCount()
        for row_index in range(row_count):
            item = self.tableWidget.item(row_index, column_index)
            if item and item.text():
                # Strip the percentage sign from the text - specifically for column 13 (course percentage)
                text_value = item.text().strip('%')
                try:
                    value = float(text_value)  # Convert the text to a float
                    values.append(value)
                except ValueError:
                    continue  # Skip non-numeric values
        return values

    def getMissingAssignments(self, column_index):
        missing = 0
        for row_index in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_index, column_index)
            if item and (item.text() == '-' or item.text() == ''):
                missing += 1
        return missing

    def getMinMax(self, column_index):
        minVal = float('inf')
        maxVal = float('-inf')
        for row_index in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_index, column_index)
            if item and item.text():
                try:
                    text_value = item.text().replace('%', '')  # Remove any percent sign
                    value = float(text_value)
                    maxVal = max(value, maxVal)
                    minVal = min(value, minVal)
                except ValueError:  # Skip non-numeric values
                    continue

        # Return None if no numeric value is found in the column
        if minVal == float('inf') or maxVal == float('-inf'):
            return self.dataError
        return minVal, maxVal

    def exportHistogram(self):
        self.exportAllGraphs()

    def exportAllGraphs(self):
        if self.tableWidget.rowCount() != 0:
            for index in range(self.comboBox.count()):
                # Set the current index to update the graph and statistics
                self.comboBox.setCurrentIndex(index)
                # Update the graph and statistics based on the current index
                self.updateStatisticsAndGraph()
                # Get the current text of the ComboBox
                column_name = self.comboBox.currentText()
                # Create a unique file name based on the ComboBox text
                file_name = f"./exports/graphs/{column_name}_Graph.png"
                # Save the figure with the unique file name
                self.figure.savefig(file_name)
        else:
            QMessageBox.information(
                self.statAnalysis, "No Data", "The table is empty. Please add data first.")
            return
    # ------------------- Display Methods -------------------

    def displayWindow(self):
        self.statAnalysis.show()
