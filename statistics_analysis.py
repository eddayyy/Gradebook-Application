import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont


class StatisticalAnalysis:
    def __init__(self, tableWidget):
        self.tableWidget = tableWidget
        self.setupUI()

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

    def displayWindow(self):
        self.statAnalysis.show()

    def updateStatisticsAndGraph(self):
        # Adjust index according to your table
        column_index = self.comboBox.currentIndex() + 4
        # Calculate statistics
        mean = self.calculateMean(column_index)
        if mean is None:
            mean = "No Data Available"
        median = self.calculateMedian(column_index)
        if median is None:
            median = "No Data Available"

        # Set font size for the statistics label
        font = QFont()
        font.setPointSize(14)  # Set the desired font size
        self.statisticsLabel.setFont(font)

        # Update statistics label
        self.statisticsLabel.setText(f'Mean: {mean}\nMedian: {median}\n')

       # Update graph
        self.ax.clear()
        values = self.getValuesFromColumn(column_index)

        # Enhance Histogram Appearance
        self.ax.hist(values, bins=10, color='skyblue',
                     edgecolor='black', label='Grades')  # Adjust as needed

        # Add a Title
        self.ax.set_title('Distribution of Student Grades',
                          fontsize=18, fontweight='bold')

        # Add Grid Lines
        self.ax.grid(True, linestyle='--', alpha=0.7)

        # Customize Axis Labels
        self.ax.set_xlabel('Student Grades', fontsize=16, fontweight='bold')
        self.ax.set_ylabel('Student Count', fontsize=16, fontweight='bold')

        # Customize Ticks
        self.ax.tick_params(axis='both', which='major', labelsize=10)

        # If you want to show the legend uncomment the next line
        self.ax.legend(loc='upper right')

        self.canvas.draw()

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

    def calculateMean(self, column_index):
        total = 0
        count = 0
        for row_index in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_index, column_index)
            if item and item.text():
                try:
                    value = float(item.text())
                    total += value
                    count += 1
                except ValueError:
                    continue
        return round(total / count, 2) if count > 0 else None

    def calculateMedian(self, column_index):
        # Collect values from tableWidget
        values = []
        for row_index in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_index, column_index)
            if item and item.text():
                try:
                    value = float(item.text())
                    values.append(value)
                except ValueError:
                    continue

        # Find the median
        values.sort()
        size = len(values)
        if size == 0:
            return None
        elif size % 2 == 1:
            return values[size//2]
        elif size % 2 == 0:
            middle1, middle2 = values[size//2 - 1], values[size//2]
            return (middle1 + middle2) / 2

    def calculateStandardDeviation(self):
        