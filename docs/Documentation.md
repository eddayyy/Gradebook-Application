# Gradebook Documentation 

## Table of Contents

1. [Overview of Libraries Used](#Overview-of-libraries-used)   
2. [Library Usage Documentation](#Library-Usage-Documentation)
   1. [PyQt5](#pyqt5)
   2. [CSV](#csv)
   3. [Sys](#sys)
   4. [NumPy](#numpy)
   5. [Matplotlib](#matplotlib)
3. [Features and Demo](#Features-and-Demo)

## Overview of Libraries Used

### This library utilized the following libraries: 

1. [PyQt5](https://www.pythonguis.com/search/?q=PyQt5)
2. [CSV File Reading and Writing](https://docs.python.org/3/library/csv.html)
3. [Sys](https://docs.python.org/2/library/sys.html)
4. [NumPy](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)
5. [Matplotlib](https://matplotlib.org/cheatsheets/_images/cheatsheets-1.png)

## Library Usage Documentation

### PyQt5 

### Introduction 

PyQt5 is a set of Python bindings for Qt libraries which can be used to create modern graphical user interfaces.

#### Installation

'''pip install PyQt5```

### Usage

In this project, PyQt5 was used extensively to creaate the Graphical User Interface. PyQt5 was crucial to creating the buttons, search feature, table display, graphical display, and the statistical analysis. Thanks PyQt5's robust and thorough applications Gradebook has an intuitive user-friendly UI. 

In addition to rendering and formatting the GUI, PyQt5 also provided a robust table data structure that not only allowed student data to be displayed but modified, manipulated, replicated, and exported. This is thanks to PyQt5's QWidgets module. 

- How to display a Qt Window:

'''python

import sys
from PyQt5 import QtWidgets

from gradebook import Gradebook

if __name__ == "__main__"

    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    MainWindow.show()

    ui = Gradebook()
    ui.setupUi(MainWindow)

    sys.exit(app.exec_())
'''

- Declaration and usage of the Qt Table:

```python
def setupTable(self, main_layout):
    self.tableWidget = QtWidgets.QTableWidget()
    self.tableWidget.setColumnCount(15)
    self.tableWidget.setHorizontalHeaderLabels([
        'SID', 'FirstName', 'LastName', 'Email',
        'HW1', 'HW2', 'HW3', 'Quiz1', 'Quiz2',
        'Quiz3', 'Quiz4', 'MidtermExam', 'FinalExam',
        'Final Score', 'Final Grade'
    ])
```

#### Important Methods

