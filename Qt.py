from PySide2 import QtWidgets
import main
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self) #start the UI
        self.plot_button.clicked.connect(self.plotting) #add a listener to the plot button

    def plotting(self):
        if(self.check_input()):
            sc = Canvas(self, width=5, hieght=4, dpi=100) #create a figure that will contain the plot later
            x_min = int(self.x_min.text()) #take inputs
            x_max = int(self.x_max.text())
            function = self.function.text()
            x = np.linspace(x_min, x_max, 60) #create the x axis values
            function = function.replace("^", "**") #replace all ^ with ** because it's understood by eval function
            try:   #just in case the experission is wrong mathematically
                y = eval(function)  #function to evaluate the function
                sc.axes.plot(x, y) #plot x vs y
                self.clear_layout() #remove any existing widgets inside the layout
                self.GLayout.addWidget(sc) #add this figure to the layout
            except SyntaxError: #incase SyntaxError is found in the expression
                QtWidgets.QMessageBox.warning(self, "Invalid Function Input", "Function input is not valid. Make sure your input is correct mathematically")

    def clear_layout(self): #just to clear the layout from widgets
        for i in reversed(range(self.GLayout.count())):
            self.GLayout.itemAt(i).widget().setParent(None)

    def check_input(self): #function to check input
        function = self.function.text()
        x_min = self.x_min.text()
        x_max = self.x_max.text()
        for c in function: #check function input validity
            if (c not in ['x', '*', '/', '+', '-', '^']) and not c.isnumeric():
                QtWidgets.QMessageBox.warning(self, "Invalid Function Input", "Function input is not valid. You may entered characters other than numbers of operators")
                return False

        if not self.isInt(x_min) or not self.isInt(x_max):  #check the validity of the range
            QtWidgets.QMessageBox.warning(self, "Invalid Range Input",
                                          "Range input is not valid. You may entered characters other than numbers of operators")
            return False
        if(int(x_max) < int(x_min)): #check if range logic is invalid or not
            QtWidgets.QMessageBox.warning(self, "Invalid Range Input",
                                          "X_minimum is larger than or equal to X_maximum")
            return False
        return True #if no error detected then it's true

    def isInt(self, s): #function to check if this string is integer
        try:
            int(s)
            return True
        except ValueError:
            return False

class Canvas(FigureCanvas): #class for the figure from matplotlib

    def __init__(self, parent=None, width=5, hieght=4, dpi=100):
        fig = Figure(figsize=(width, hieght), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(Canvas, self).__init__(fig)

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    qt_app = MyQtApp()
    qt_app.show()
    app.exec_()