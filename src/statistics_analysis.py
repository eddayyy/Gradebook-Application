# Author: Eduardo Nunez
# Author email: eduardonunez.eng@gmail.com
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
        grid_layout.addWidget(self.fieldLabel, 0, 0)  # Add to row 0, column 0
        grid_layout.addWidget(self.comboBox, 0, 1)  # Add to row 0, column 1

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
        self.canvas = FigureCanvas(self.figure)
        graph_display_layout.addWidget(self.canvas)
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
        median = self.calculateStats(column_index, 'median')
        std = self.calculateStats(column_index, 'std')
        passing, failing, passingRate, failingRate = self.passFailingRate(
            column_index)
        missing_assignments = self.getMissingAssignments(column_index)
        minVal, maxVal = self.getMinMax(column_index)

        # Structured and formatted statistics text
        statistics_text = (
            f"Maximum Score: {maxVal}\n"
            f"Minimum Score:{minVal}\n"
            f"Mean: {mean}\n"
            f"Median: {median}\n"
            f"Standard Deviation: {std}\n"
            f"Passing: {passing} ({passingRate})\n"
            f"Failing: {failing} ({failingRate})\n"
            f"Missing Assignments: {missing_assignments}\n"
        )

        self.statisticsLabel.setText(statistics_text)

    def updateGraph(self, column_index):
        self.ax.clear()
        values = self.getValuesFromColumn(column_index)
        self.ax.hist(values, bins=10, color='skyblue',
                     edgecolor='black', label='Grades')
        self.customizeGraphAppearance()
        self.canvas.draw()

    def customizeGraphAppearance(self):
        self.ax.clear()
        self.ax.set_title('Distribution of Student Grades',
                          fontsize=18, fontweight='bold', color='darkblue')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_xlabel('Student Grades', fontsize=16,
                           fontweight='bold', color='darkgreen')
        self.ax.set_ylabel('Student Count', fontsize=16,
                           fontweight='bold', color='darkgreen')
        self.ax.tick_params(axis='both', which='major',
                            labelsize=10, colors='darkred')
        self.ax.set_xlim([0, 100])  # Set x-axis limits to represent grades
        # Set y-axis limits to represent student count
        self.ax.set_ylim([0, 10])
        self.canvas.draw()  # Draw the empty graph

    def calculateStats(self, column_index, stat_type):
        values = self.getValuesFromColumn(column_index)
        if not values:  # If the list is empty, return None
            return self.dataError

        stat_function = getattr(np, stat_type)
        if column_index == self.tableWidget.columnCount() - 1:
            return stat_function(values)
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
        for row_index in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_index, column_index)
            if item and item.text():
                try:
                    if type(item.text()) != float:
                        value = float(item.text())
                        values.append(value)
                    else:
                        values.append(item.text())
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
                    text_value = item.text().replace('%', '')  # Remove any percentage sign
                    value = float(text_value)
                    maxVal = max(value, maxVal)
                    minVal = min(value, minVal)
                    print(f'{value}\n')
                except ValueError:  # Skip non-numeric values
                    continue

        # Return None if no numeric value is found in the column
        if minVal == float('inf') or maxVal == float('-inf'):
            return self.dataError

        return minVal, maxVal

    def exportHistogram(self):
        self.figure.savefig("./exports/StudentDataGraph.png")

    # ------------------- Display Methods -------------------

    def displayWindow(self):
        self.statAnalysis.show()
