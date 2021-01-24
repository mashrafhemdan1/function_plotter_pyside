from PySide2 import QtWidgets
import main
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)
        self.plot_button.clicked.connect(self.plotting)

    def plotting(self):
        if(self.check_input()):
            sc = Canvas(self, width=5, hieght=4, dpi=100)
            x_min = int(self.x_min.text())
            x_max = int(self.x_max.text())
            function = self.function.text()
            x = np.linspace(x_min, x_max, 60)
            function = function.replace("^", "**")
            try:
                y = eval(function)
                sc.axes.plot(x, y)
                self.clear_layout()
                self.GLayout.addWidget(sc)
            except SyntaxError:
                QtWidgets.QMessageBox.warning(self, "Invalid Function Input", "Function input is not valid. Make sure your input is correct mathematically")

    def clear_layout(self):
        for i in reversed(range(self.GLayout.count())):
            self.GLayout.itemAt(i).widget().setParent(None)

    def check_input(self):
        function = self.function.text()
        x_min = self.x_min.text()
        x_max = self.x_max.text()
        for c in function:
            if (c not in ['x', '*', '/', '+', '-', '^']) and not c.isnumeric():
                QtWidgets.QMessageBox.warning(self, "Invalid Function Input", "Function input is not valid. You may entered characters other than numbers of operators")
                return False

        if not self.isInt(x_min) or not self.isInt(x_max):
            QtWidgets.QMessageBox.warning(self, "Invalid Range Input",
                                          "Range input is not valid. You may entered characters other than numbers of operators")
            return False
        if(int(x_max) < int(x_min)):
            QtWidgets.QMessageBox.warning(self, "Invalid Range Input",
                                          "X_minimum is larger than or equal to X_maximum")
            return False
        return True

    def isInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

class Canvas(FigureCanvas):

    def __init__(self, parent=None, width=5, hieght=4, dpi=100):
        fig = Figure(figsize=(width, hieght), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(Canvas, self).__init__(fig)

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    qt_app = MyQtApp()
    qt_app.show()
    app.exec_()