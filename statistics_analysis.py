import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont


class StatisticalAnalysis:
    def __init__(self, tableWidget):
        self.tableWidget = tableWidget
        self.setupUI()

    # ------------------- Setup/UI Initialization Methods -------------------
    def setupUI(self):
        self.initializeMainWindow()
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        self.setupControlPanel(main_layout)
        self.setupStatisticsDisplay(main_layout)
        self.setupGraphDisplay(main_layout)

        self.statAnalysis.setCentralWidget(central_widget)

    def initializeMainWindow(self):
        self.statAnalysis = QtWidgets.QMainWindow()
        self.statAnalysis.setObjectName('StatisticalAnalysisWindow')
        self.statAnalysis.resize(1280, 960)
        self.statAnalysis.setWindowTitle('Statistical Analysis')

    def setupControlPanel(self, main_layout):
        control_panel_layout = QHBoxLayout()
        control_panel_layout.setContentsMargins(10, 10, 10, 10)

        self.comboBox = QComboBox()
        self.comboBox.addItems([
            'HW1', 'HW2', 'HW3', 'Quiz1', 'Quiz2', 'Quiz3', 'Quiz4', 'MidtermExam', 'FinalExam'
        ])
        self.comboBox.currentIndexChanged.connect(
            self.updateStatisticsAndGraph)
        control_panel_layout.addWidget(self.comboBox)

        main_layout.addLayout(control_panel_layout)

    def setupStatisticsDisplay(self, main_layout):
        self.statisticsLabel = QLabel()
        font = QFont()
        font.setPointSize(14)
        self.statisticsLabel.setFont(font)
        main_layout.addWidget(self.statisticsLabel)

    def setupGraphDisplay(self, main_layout):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

    # ------------------- Mathematical/Calculation Methods -------------------

    def updateStatisticsAndGraph(self):
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

        # Set font size for the statistics label
        font = QFont()
        font.setPointSize(14)
        self.statisticsLabel.setFont(font)
        self.statisticsLabel.setText(
            f'Mean: {mean}\n'
            f'Median: {median}\n'
            f'Standard Deviation: {std}\n'
            f'Passing: {passing} ({passingRate})\n'
            f'Failing: {failing} ({failingRate})\n'
            f'Missing Assignments: {missing_assignments}\n'
            f'Max: {maxVal}\n'
            f'Min: {minVal}\n'
        )

    def updateGraph(self, column_index):
        self.ax.clear()
        values = self.getValuesFromColumn(column_index)
        self.ax.hist(values, bins=10, color='skyblue',
                     edgecolor='black', label='Grades')
        self.customizeGraphAppearance()
        self.canvas.draw()

    def customizeGraphAppearance(self):
        self.ax.set_title('Distribution of Student Grades',
                          fontsize=18, fontweight='bold')

        self.ax.grid(True, linestyle='--', alpha=0.7)

        self.ax.set_xlabel('Student Grades', fontsize=16, fontweight='bold')
        self.ax.set_ylabel('Student Count', fontsize=16, fontweight='bold')

        self.ax.tick_params(axis='both', which='major', labelsize=10)
        self.ax.legend(loc='upper right')

    def calculateStats(self, column_index, stat_type):
        values = self.getValuesFromColumn(column_index)
        if not values:  # If the list is empty, return None
            return "No Available Data"
        stat_function = getattr(np, stat_type)
        return round(stat_function(values), 2)

    def passFailingRate(self, column_index):
        values = self.getValuesFromColumn(column_index)
        passing, failing = 0, 0
        if not values:
            return "No Available Data"
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
                    value = float(item.text())
                    values.append(value)
                except ValueError:
                    continue  # Skip non-numeric values
        return values

    def getMissingAssignments(self, column_index):
        missing = 0
        for row_index in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_index, column_index)
            if item and item.text() == '-' or '':
                missing += 1
        return missing

    def getMinMax(self, column_index):
        minVal = float('inf')  # recall A-B Pruning
        maxVal = float('-inf')
        temp = 0
        for row_index in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_index, column_index)
            if item and item.text():
                try:
                    temp = float(item.text())
                    maxVal = max(temp, maxVal)
                    minVal = min(temp, minVal)
                except ValueError:  # Skip non-numeric values
                    continue

        # Return None if no numeric value is found in the column
        if minVal == float('inf') or maxVal == float('-inf'):
            return "No Available Data"

        return minVal, maxVal

    # ------------------- Display Methods -------------------

    def displayWindow(self):
        self.statAnalysis.show()
