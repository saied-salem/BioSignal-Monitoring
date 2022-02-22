import sys
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import  Slider
import numpy as np
import pandas as pd

matplotlib.use('Qt5Agg')
from matplotlib.pyplot import isinteractive
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


'''
    @ Auther by saied salem
    Wakhed Baaaalk Yaa ABO IBRAHEM
'''

class NavigationToolbar(NavigationToolbar2QT):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom')]

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)


        super().__init__(self.fig)

        self.axfreq = self.fig.add_axes([0.25, 0.05, 0.65, 0.03])
        self.slider_position = 0

        self.plot_signal1 ,  = self.axes.plot([],[])
        self.plot_signal2 , = self.axes.plot([], [],'r')
        self.plot_signal3, = self.axes.plot([],[],)
        self.plot_signal4, = self.axes.plot([],[],)


    def Creat_image(self):
        self.image_arr=np.array(self.renderer.buffer_rgba())

        print(self.image_arr)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):


        super(MainWindow, self).__init__()

        self.setCentralWidget(QtWidgets.QWidget())

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        #print(self.centralWidget())
        self.centralWidget().setLayout(QtWidgets.QVBoxLayout())
        self.centralWidget().layout().addWidget(self.canvas)
        self.centralWidget().layout().addWidget(self.toolbar)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setGeometry(QtCore.QRect(100, 100, 150, 60))
        self.b1.setText("start")
        self.b1.clicked.connect(self.play)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setGeometry(QtCore.QRect(200, 20, 150, 60))
        self.b2.setText("toggle visibility")
        self.b2.clicked.connect(self.hide_graph_1)

        self.b3 = QtWidgets.QPushButton(self)
        self.b3.setGeometry(QtCore.QRect(300, 100, 150, 60))
        self.b3.setText("stop")
        self.b3.clicked.connect(self.stop)

        self.b4 = QtWidgets.QPushButton(self)
        self.b4.setGeometry(QtCore.QRect(300, 300, 150, 60))
        self.b4.setText("imge")
        self.b4.clicked.connect(self.print_image)

        self.b4 = QtWidgets.QPushButton(self)
        self.b4.setGeometry(QtCore.QRect(100, 300, 150, 60))
        self.b4.setText("speed up")
        self.b4.clicked.connect(self.increase_speed)

        self.b5 = QtWidgets.QPushButton(self)
        self.b5.setGeometry(QtCore.QRect(100, 400, 150, 60))
        self.b5.setText("speed down")
        self.b5.clicked.connect(self.decrease_speed)




        loaded_ECG_data = pd.read_csv("ECG.csv")
        self.ydata = loaded_ECG_data['filtered_ECG_mV'].to_numpy().tolist()
        self.xdata = loaded_ECG_data['time_sec'].to_numpy().tolist()

        loaded_ECG_data2 = pd.read_csv("emg.csv")
        self.ydata22 = loaded_ECG_data2["EMG_mV"].to_numpy().tolist()
        self.xdata22 = loaded_ECG_data2["time_sec"].to_numpy().tolist()

        loaded_ECG_data3 = pd.read_csv("Sudden Cardiac Death Holter Database.csv")
        self.ydata3 = loaded_ECG_data3['ECG1'].to_numpy().tolist()
        self.xdata3 = np.arange(0.0, len(self.ydata3) * 0.004, 0.004)

        loaded_ECG_data4 = pd.read_csv("Signals/abnormal_emg.xls")
        self.ydata4 = loaded_ECG_data4['EMG'].to_numpy().tolist()
        self.xdata4 = np.arange(0.0, len(self.ydata4) * 0.0025, 0.0025)

        self.canvas.plot_signal1.set_data(self.xdata,self.ydata)
        self.canvas.plot_signal2.set_data(self.xdata22, self.ydata22)
        self.canvas.plot_signal3.set_data(self.xdata3, self.ydata3)
        self.canvas.plot_signal4.set_data(self.xdata4, self.ydata4)




        self.initial_end_xlim = 0.5

        self.dummy_xarr_R=[]
        self.dummy_xarr_L=[]
        self.dummy_yarr_B=[]
        self.dummy_yarr_T=[]
        self.dx=0.001
        self.dx1 = self.xdata[1]- self.xdata[0]
        self.dx2 = self.xdata22[1]- self.xdata22[0]
        self.dx3 = 0

        '''
            Setting initial limits with smallest Signal X_data 
        '''

        self.largest_x_val_arr = [max(self.xdata),max(self.xdata22)]
        self.largest_x_val_arr.sort()


        self.canvas.slider = Slider(
            ax=self.canvas.axfreq,
            label='Frequency [Hz]',
            valmin=0,
            valmax=self.largest_x_val_arr[-1]-0.5,
            valstep=0.0002
        )
        self.canvas.slider.set_val(0)

        '''
            Setting Canvas Limits 
            
        '''

        self.canvas.axes.set_ylim(bottom=-1,top=2.5)
        self.canvas.axes.set_xlim(left=0, right=self.initial_end_xlim)

        '''
            setting initial visibility
        '''
        self.graph_1_visibility = True
        self.graph_2_visibility = True
        self.graph_3_visibility =True
        self.show()

        self.new_xlim = self.canvas.mpl_connect('draw_event', self.on_axes_limits_change_general)

        self.canvas.slider.on_changed(self.slider_movment)

        self.timer = QtCore.QTimer()

        self.canvas.axes.grid()

    def slider_movment(self,value):

        xlim = self.canvas.axes.get_xlim()
        change = value-self.canvas.slider_position
        self.canvas.axes.set_xlim(left=xlim[0]+change , right=xlim[1]+change)
        self.canvas.slider_position = value
        # self.slider.setValue(int(temp_xlim[0]))



    def changing_visiblty(self):
        if self.graph_1_visibility:
            self.canvas.plot_signal1.set_data(self.xdata,self.ydata)
            self.canvas.draw()

        else:
            self.canvas.plot_signal1.set_data([],[])
            self.canvas.draw()



    def on_axes_limits_change_general(self, event):
        temp_xlim = self.canvas.axes.get_xlim()
        temp_ylim = self.canvas.axes.get_ylim()


        if temp_ylim[0]< -1.5:
            self.dummy_yarr_T.append(temp_ylim[1])
            self.canvas.axes.set_ylim(bottom=-0.5,top=self.dummy_yarr_T[0])
            del self.dummy_yarr_T[1:]
            # self.dummy_arr_R.clear()

        if temp_ylim[1] > 2.8:
            self.dummy_yarr_B.append(temp_ylim[0])
            # self.corriction = self.dummy_yarr_L[0]
            self.canvas.axes.set_ylim(bottom=self.dummy_yarr_B[0], top=2.5)
            del self.dummy_yarr_B[1:]
            #print("del self.ydummy_arr_L[1:]" ,  self.dummy_yarr_B)


        if temp_xlim[0]< 0.0:
            self.dummy_xarr_R.append(temp_xlim[1])
            self.canvas.axes.set_xlim(left=0,right=self.dummy_xarr_R[0])
            del self.dummy_xarr_R[1:]
            # self.dummy_arr_R.clear()

        if temp_xlim[1] > self.largest_x_val_arr[-1]:
            print("iam out of raaaange","dummy array:",self.dummy_xarr_L)
            self.dummy_xarr_L.append(temp_xlim[0])
            self.corriction = self.dummy_xarr_L[0]
            self.canvas.axes.set_xlim(left=self.dummy_xarr_L[0], right=self.largest_x_val_arr[-1])
            del self.dummy_xarr_L[1:]
            #print("del self.dummy_arr_L[1:]" ,  self.dummy_xarr_L)

        print("channnngggingggg","\nxlim",temp_xlim)


    def play(self):
        self.idx1 = 0
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot)

        #print("get axesssssssssss",self.canvas.axes.get_xbound())
        self.timer.start()


    def stop(self):
        self.timer.stop()



    def hide_graph_1(self):

        self.graph_1_visibility = not self.graph_1_visibility

        self.changing_visiblty()


    def update_plot(self):


        adjusting_xlim = self.canvas.axes.get_xlim()
        #print(len(self.xdata))

        if(adjusting_xlim[1]+self.dx>self.largest_x_val_arr[-1]):
            #print("stopp scrolling")
            return

        self.canvas.axes.set_xlim(left=adjusting_xlim[0]+self.dx , right=adjusting_xlim[1]+self.dx)
        print(self.dx)


        # Trigger the canvas to update and redraw.


        self.canvas.draw()

    def print_image(self):
        self.canvas.Creat_image()


    def increase_speed(self):
        self.dx  = self.dx*2

    def decrease_speed(self):
        self.canvas.plot_signal3.set_color('#c65969')
        self.dx = self.dx/2

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
