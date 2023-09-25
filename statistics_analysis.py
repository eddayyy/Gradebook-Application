import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QMessageBox, QGridLayout, QSplitter
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont


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

        # Create a Group Box for Control Panel
        control_panel_group_box = QtWidgets.QGroupBox("Fields:")
        control_panel_layout = QVBoxLayout(control_panel_group_box)
        self.setupControlPanel(control_panel_layout)
        main_layout.addWidget(control_panel_group_box)  # Control panel at the top

        # Horizontal layout for statistics and graph
        horizontal_layout = QHBoxLayout()
        
        # Create a Group Box for Statistics Display
        statistics_display_group_box = QtWidgets.QGroupBox("Statistics Display")
        statistics_display_layout = QVBoxLayout(statistics_display_group_box)
        self.setupStatisticsDisplay(statistics_display_layout)
        horizontal_layout.addWidget(statistics_display_group_box)

        # Create a Group Box for Graph Display
        graph_display_group_box = QtWidgets.QGroupBox("Graph Display")
        graph_display_layout = QVBoxLayout(graph_display_group_box)
        self.setupGraphDisplay(graph_display_layout)
        horizontal_layout.addWidget(graph_display_group_box)

        # Add horizontal layout to the main layout
        main_layout.addLayout(horizontal_layout)

        # Set size policies to make widgets expandable
        control_panel_group_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        statistics_display_group_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        graph_display_group_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Optionally, use QSplitter for user-adjustable sizes between statistics and graph
        splitter = QSplitter()
        splitter.addWidget(statistics_display_group_box)
        splitter.addWidget(graph_display_group_box)
        horizontal_layout.addWidget(splitter)

        self.statAnalysis.setCentralWidget(central_widget)

    def initializeMainWindow(self):
        self.statAnalysis = QtWidgets.QMainWindow()
        self.statAnalysis.setObjectName('StatisticalAnalysisWindow')
        self.statAnalysis.resize(1280, 960)
        self.statAnalysis.setWindowTitle('Statistical Analysis')

    def setupControlPanel(self, control_panel_layout):
        self.comboBox = QComboBox()
        self.comboBox.addItems([
            'HW1', 'HW2', 'HW3', 'Quiz1', 'Quiz2', 'Quiz3', 'Quiz4', 'MidtermExam', 'FinalExam'
        ])
        self.comboBox.currentIndexChanged.connect(
            self.updateStatisticsAndGraph)
        control_panel_layout.addWidget(self.comboBox)

    def setupStatisticsDisplay(self, statistics_display_layout):
        self.statisticsLabel = QLabel()
        font = QFont()
        font.setPointSize(14)
        self.statisticsLabel.setFont(font)
        statistics_display_layout.addWidget(self.statisticsLabel)

    def setupGraphDisplay(self, graph_display_layout):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        graph_display_layout.addWidget(self.canvas)

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

        # Set font size for the statistics label
        font = QFont()
        font.setPointSize(14)
        self.statisticsLabel.setFont(font)

        # Structured and formatted statistics text
        statistics_text = (
            f"<b>Statistics:</b><br>"
            f"<table>"
            f"<tr><td>Maximum Score:</td><td align='right'>{maxVal}</td></tr>"
            f"<tr><td>Minimum Score:</td><td align='right'>{minVal}</td></tr>"
            f"<tr><td>Mean:</td><td align='right'>{mean}</td></tr>"
            f"<tr><td>Median:</td><td align='right'>{median}</td></tr>"
            f"<tr><td>Standard Deviation:</td><td align='right'>{std}</td></tr>"
            f"<tr><td>Passing:</td><td align='right'>{passing} ({passingRate})</td></tr>"
            f"<tr><td>Failing:</td><td align='right'>{failing} ({failingRate})</td></tr>"
            f"<tr><td>Missing Assignments:</td><td align='right'>{missing_assignments}</td></tr>"
            f"</table>"
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
        self.ax.set_title('Distribution of Student Grades',
                          fontsize=18, fontweight='bold', color='darkblue')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_xlabel('Student Grades', fontsize=16,
                           fontweight='bold', color='darkgreen')
        self.ax.set_ylabel('Student Count', fontsize=16,
                           fontweight='bold', color='darkgreen')
        self.ax.tick_params(axis='both', which='major',
                            labelsize=10, colors='darkred')
        self.ax.legend(loc='upper right')

    def calculateStats(self, column_index, stat_type):
        values = self.getValuesFromColumn(column_index)
        if not values:  # If the list is empty, return None
            return self.dataError
        stat_function = getattr(np, stat_type)
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
                    value = float(item.text())
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
            return self.dataError

        return minVal, maxVal

    # ------------------- Display Methods -------------------

    def displayWindow(self):
        self.statAnalysis.show()
