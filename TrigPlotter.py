from PyQt5.QtWidgets import QApplication , QMainWindow , QComboBox , QLabel ,QLineEdit
from PyQt5 import uic
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from io import BytesIO
import warnings



class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()

        # define ui file
        uic.loadUi('TrigPlotter.ui',self)


        # define widgets
        self.view_label = self.findChild(QLabel,'view_label')
        self.comboBox = self.findChild(QComboBox,'comboBox')
        self.enter_label = self.findChild(QLabel,'enter_label')
        self.angle_lineEdit = self.findChild(QLineEdit,'angle_lineEdit')


        # connect combo to their function
        self.comboBox.currentTextChanged.connect(self.combo_changed)
        self.angle_lineEdit.returnPressed.connect(
            lambda: self.combo_changed(self.comboBox.currentText())
        )


        self.show()


    #______________________define functions__________________________


    def combo_changed(self, selected_text):

        # get user input from LineEdit
        angle = self.angle_lineEdit.text()

        # stop combo_changed function when lineEdit is empty
        if not angle.strip():
            return

        # map selected text to related function
        func_map = {
            'Sine': self.sin_combo,
            'Cosine': self.cos_combo,
            'Tangent': self.tan_combo,
            'Cotangent': self.cot_combo
        }

        # call selected function
        if selected_text in func_map:
            func_map[selected_text](angle)




    def plot_trig(self, angle, func, func_name, color, y_label, y_limit=None, start_x=0):

        angle = float(angle)                # convert input to float
        rad = np.deg2rad(angle)             # convert degrees to radians
        end_x = max(360, angle + 20)        # ensure at least one full cycle


        x_deg = np.linspace(start_x, end_x, 2000)          # smooth sampling
        x_rad = np.deg2rad(x_deg)                               # convert to radians


        #  suppress divide-by-zero warnings safely
        with np.errstate(divide='ignore', invalid='ignore'):
            y = func(x_rad)
            y_point = func(rad)


        # plot curve
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x_deg, y, label=f"{func_name}(x)", linewidth=2, color=color)
        ax.scatter(angle, y_point, s=100, color="red", zorder=5)
        ax.plot([angle, angle], [0, y_point], "--", color="gray", linewidth=1)
        ax.plot([0, angle], [y_point, y_point], "--", color="gray", linewidth=1)


        # axis spines
        ax.spines['bottom'].set_position(('data', 0))
        ax.spines['left'].set_position(('data', 0))
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')


        # add annotation text near selected point
        ax.text(angle, y_point,
                f"{func_name}({angle:.1f}°) = {y_point:.4f}",
                fontsize=12,
                verticalalignment="bottom",
                horizontalalignment="left",
                color="darkred")


        # configure labels, limits, grid, title, and legend
        ax.set_xlabel("Angle (degrees)", fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        ax.set_xlim(0, end_x)
        if y_limit:
            ax.set_ylim(*y_limit)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.set_title(f"{func_name.capitalize()} Wave (Degrees) with Guide Lines to Axes", fontsize=14)
        ax.legend()


        # render matplotlib figure to QPixmap and show in QLabel
        buf = BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format='png')
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.view_label.setPixmap(pixmap)
        self.view_label.setAlignment(Qt.AlignCenter)
        buf.close()
        plt.close(fig)




    def sin_combo(self, angle):
        self.plot_trig(angle, np.sin, "sin", "blue", "sin(angle)", (-1.1, 1.1))




    def cos_combo(self, angle):
        self.plot_trig(angle, np.cos, "cos", "green", "cos(angle)", (-1.1, 1.1))




    def tan_combo(self, angle):
        angle = float(angle)
        if angle % 180 == 90:
            self.view_label.setText(f"tangent of {angle} degree is undefined cause its cosine equals zero ")
        else:
            self.plot_trig(angle, np.tan, "tan", "purple", "tan(angle)", (-10, 10))




    def cot_combo(self, angle):
        angle = float(angle)
        if angle % 180 == 0  or angle == 0:
            self.view_label.setText(f"cotangent of {angle} degree is undefined cause its sine equals zero")
        else:
            self.plot_trig(angle, lambda x: np.cos(x) / np.sin(x), "cot", "orange", "cot(angle)", (-10, 10))




# initialize
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()