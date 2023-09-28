# Gradebook Documentation 

## Table of Contents
1. [Overview of Libraries Used](#Overview-of-libraries-used)   
2. [Library Usage Documentation](#Library-Usage-Documentation)
3. [Features and Demo](#Features-and-Demo)

## Overview of Libraries Used
This program utilized the following libraries: 
1. [PyQt5](#pyqt5)
2. [CSV](#csv)
3. [Sys](#sys)
4. [NumPy](#numpy)
5. [Matplotlib](#matplotlib)

# Library Usage Documentation

## [PyQt5](https://www.pythonguis.com/search/?q=PyQt5)
#### **Introduction** 

PyQt5 is a set of Python bindings for Qt libraries which can be used to create modern graphical user interfaces. PyQt5 was used extensively to create the Graphical User Interface. Throughout the codebase PyQt5 was crucial to creating the buttons, search feature, import/export feature, table display, graphical display, and the statistical analysis.
#### **Installation**

```shell
pip install PyQt5
```
#### **Modules Usage**
In addition to rendering and formatting the GUI, PyQt5 also provided a robust table data structure that not only allowed student data to be displayed but modified, manipulated, replicated, and exported. This is thanks to PyQt5's QWidgets module. 

- The following documentation was used to implement PyQt5 to the Gradebook program:
1. [QTable Widget](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QTableWidget.html#more)
    1. This was used to store the student data that the user imported. The documentation for that module is extensive and provides many useful methods for data manipulation. 
    2. The function setHorizontalHeaderLabels() was also used to label each column with the student info (SID, Name, Grades etc.)
    3. Another module used in combination with QTable Widget was QAbstractItemView. This was used in combination with the selection and editting behavior of the table. 
    4. There is also a connect feature which allowed for the interactions with the table to be connected to custom functions. An example of this is when the headers are clicked. This calls a function that I defined named sortColumns. This function allows the user to sort the students by SID, name, grades, etc.
2. [QAbstractItemView](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QAbstractItemView.html)
    1. The particular functions that were used in this program are "QAbstractItemView.SelectRows()" and QAbstractItemView.DoubleClick()" these were used to dictate the selection and editing behavior of the table. 
3. [QApplication](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QApplication.html)
    1. This clas was used to create an instance of Qt Application. This is necessary for any Python-based Qt Application. 
    2. Additionally the function .exec_() was used to begin the event loop for the Qt Application.
4. [Other QtWidgets used](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/)
    1. [QVBoxLayout](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QTableWidget.html#PySide6.QtWidgets.PySide6.QtWidgets.QTableWidget.cellWidget)
        1. Used to set the vertical layout that was rendered 
    2. [QToolBar](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QToolBar.html#qtoolbar)
        1. Used to set the layout for the buttons such as "Add Student", "Import", "Delete Student"

 
## **[CSV](https://docs.python.org/3/library/csv.html)**

#### **Introduction** 

#### **Installation**

#### **Usage**

## **[Sys](https://docs.python.org/2/library/sys.html)**

#### **Introduction** 

#### **Installation**

#### **Usage**

## **[NumPy](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)**

#### **Introduction** 

#### **Installation**

#### **Usage**

## **[Matplotlib](https://matplotlib.org/cheatsheets/_images/cheatsheets-1.png)**

#### **Introduction** 

#### **Installation**

#### **Usage**

# Features and Demo

## Demo: 
