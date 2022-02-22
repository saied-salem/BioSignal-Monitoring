import matplotlib
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from SignalsStore import SignalsStore
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic

matplotlib.use('Qt5Agg')

class NavigationToolbar(NavigationToolbar2QT):
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom')]

class SignalViewer(qtw.QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/signal_canvas.ui", self)
        canvas_layout = self.findChild(qtw.QVBoxLayout, "viewer")
        self.horizontal_slider = self.findChild(qtw.QScrollBar, "x_scroll")
        self.vertical_slider = self.findChild(qtw.QScrollBar, "y_scroll")
        self.horizontal_slider.setSingleStep(2)
        self.horizontal_slider.setMinimum(0)
        self.horizontal_slider.setMaximum(2000)
        self.vertical_slider.setMinimum(0)
        self.vertical_slider.setMaximum(2000)
        self.mapping_horizontal_scroll = 0
        self.mapping_vertical_scroll = 0

        self.signal_canvas = SignalCanvas()
        self.signal_canvas.setMinimumSize(2.1,100)
        canvas_layout.addWidget(self.signal_canvas)

        self.signals_store = SignalsStore()

        self.speed_up.clicked.connect(self.signal_canvas.increase_speed)
        self.speed_down.clicked.connect(self.signal_canvas.decrease_speed)
        self.start.clicked.connect(self.signal_canvas.play)
        self.stop.clicked.connect(self.signal_canvas.stop)
        self.channel_1.stateChanged.connect(self.toggleVisibility1)
        self.channel_2.stateChanged.connect(self.toggleVisibility2)
        self.channel_3.stateChanged.connect(self.toggleVisibility3)

        self.signal_canvas.channelLoaded.connect(self.updateScrollingLimits)

        self.horizontal_slider.valueChanged.connect(self.updateGraphHorizontal)
        self.signal_canvas.xPosChanged.connect(self.updateHorizontalPos)

        self.vertical_slider.valueChanged.connect(self.updateGraphVertical)

    def udpateChannelsLabels(self):
        for i in range(0, len(self.signal_canvas.channels)):
            channel = self.signal_canvas.channels[i]
            print(channel.keys())
            channel_name = channel["name"]
            if i == 0: self.channel_1.setText(f"CH1: {channel_name}")
            if i == 1: self.channel_2.setText(f"CH2: {channel_name}")
            if i == 2: self.channel_3.setText(f"CH3: {channel_name}")

    def updateHorizontalPos(self, left):
        slider_pos = left * 2000/self.mapping_horizontal_scroll
        self.horizontal_slider.setValue(slider_pos)

    def updateVerticalPos(self, bottom):
        slider_pos = bottom * 2000/self.mapping_vertical_scroll
        self.horizontal_slider.setValue(slider_pos)

    def updateGraphHorizontal(self, curr_value):
        curr_graph_poistion = curr_value * self.mapping_horizontal_scroll/2000
        self.signal_canvas.updateGraphPosition(curr_graph_poistion)

    def updateGraphVertical(self, curr_value):
        curr_graph_poistion = curr_value * self.mapping_vertical_scroll/2000
        self.signal_canvas.updateGraphHeight(curr_graph_poistion)

    def toggleVisibility1(self):
        if self.channel_1.isChecked():
            self.signal_canvas.setVisibility(0, True)
        else: self.signal_canvas.setVisibility(0, False)

    def toggleVisibility2(self):
        if self.channel_2.isChecked():
            self.signal_canvas.setVisibility(1, True)
        else: self.signal_canvas.setVisibility(1, False)

    def toggleVisibility3(self):
        if self.channel_3.isChecked():
            self.signal_canvas.setVisibility(2, True)
        else: self.signal_canvas.setVisibility(2, False)

    def updatePrintedImage(self):
        self.signal_canvas.PrintedImage()

    def updateScrollingLimits(self, statistics, screen_width, screen_height):
        _,maxTime, minValue, maxValue = statistics
        self.mapping_horizontal_scroll = (maxTime-screen_width)
        self.mapping_vertical_scroll = (maxValue-minValue-screen_height)
        #self.mapping_vertical_scroll = 6


class SignalCanvas(FigureCanvas):

    channelLoaded = qtc.pyqtSignal(tuple, float, float)
    xPosChanged = qtc.pyqtSignal(float)

    def __init__(self, width=5, height=4, dpi=100):

        self.fig = plt.Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

        self.signals_store = SignalsStore()
        self.initGlobals()
        self.initSetters()
        self.mpl_connect( 'draw_event', self.limitsHandler)
        self.mpl_connect( 'draw_event', self.updateHorizontalPos)
        self.timer = qtc.QTimer()

    def initSetters(self):
        self.setMinimumSize(0,250)
        self.axes.set_ylim(bottom=-1,top=2.5)
        self.axes.set_xlim(left=0, right=0.5)
        self.axes.grid()

    def initGlobals(self):
        self.slider_position = 0
        self.step = 0.001
        self.channels = []
        self.dummy_xarr_R=[]
        self.dummy_xarr_L=[]
        self.dummy_yarr_B=[]
        self.dummy_yarr_T=[]
        self.min_time, self.max_time, self.min_signal, self.max_signal = 0,0,0,0

    def getStatistics(self):
        if(self.signals_store.getNumChannels() >= 1):
            times , signals_values = [], []
            for channel in self.signals_store._signals:
                _, (time, signal_values) = channel
                times.append(max(time))
                times.append(min(time))
                signals_values.append(max(signal_values))
                signals_values.append(min(signal_values))
            return (min(times), max(times), min(signals_values), max(signals_values))
        else: return (0,0,0,0)


    def loadChannels(self):
        print(len(self.signals_store._signals))
        self.channels.clear()
        self.axes.cla()
        self.initSetters()
        for channel in self.signals_store._signals:
            channel_name, (time, signal_values) = channel
            channel_plot, = self.axes.plot([], [])
            self.channels.append(
                {
                    "name": channel_name,
                    "plot": channel_plot,
                    "visiblility": True,
                    "time": time,
                    "signal_values": signal_values
                }
            )
        statistics = self.getStatistics()
        self.min_time, self.max_time, self.min_signal, self.max_signal = statistics
        self.channelLoaded.emit(statistics, 0.5, 3.5)

    def drawChannels(self):
        for channel in self.channels:
            time = channel["time"]
            signal_values = channel["signal_values"]
            channel_plot = channel["plot"]
            channel_plot.set_data(time, signal_values)

    def updateHorizontalPos(self, event):
        left, right = self.axes.get_xlim()
        self.xPosChanged.emit(left)

    def updateGraphHeight(self, pos):
        self.axes.set_ylim(bottom=pos , top=pos+3.5)
        self.draw()

    def updateGraphPosition(self, pos):
        self.axes.set_xlim(left=pos , right=pos+0.5)
        self.draw()

    def horizontalSlider(self,value):

        left_limit, right_limit = self.axes.get_xlim()
        change = value-self.slider_position
        self.axes.set_xlim(left=left_limit+change , right=right_limit+change)
        self.slider_position = value



    def setVisibility(self, channelIdx, visible):
        if(channelIdx <= self.signals_store.getNumChannels()-1):
            time = self.channels[channelIdx]["time"]
            signal_values = self.channels[channelIdx]["signal_values"]
            channel_plot = self.channels[channelIdx]["plot"]
            if visible:
                channel_plot.set_data(time, signal_values)
                self.draw()
            else:
                channel_plot.set_data([],[])
                self.draw()
        else: print("CHANNELS ARE NOT ENOUGH")

    def limitsHandler(self, event):
        left, right = self.axes.get_xlim()
        bottom, top = self.axes.get_ylim()

        if bottom < -1.5:
            self.dummy_yarr_T.append(top)
            self.axes.set_ylim(bottom=-0.5,top=self.dummy_yarr_T[0])
            del self.dummy_yarr_T[1:]

        if top > 2.8:
            self.dummy_yarr_B.append(bottom)
            self.axes.set_ylim(bottom=self.dummy_yarr_B[0], top=2.5)
            del self.dummy_yarr_B[1:]

        if left < 0.0:
            self.dummy_xarr_R.append(right)
            self.axes.set_xlim(left=0,right=self.dummy_xarr_R[0])
            del self.dummy_xarr_R[1:]

        if right > self.max_time:
            self.dummy_xarr_L.append(left)
            self.corriction = self.dummy_xarr_L[0]
            self.axes.set_xlim(left=self.dummy_xarr_L[0], right=self.max_time)
            del self.dummy_xarr_L[1:]


    def play(self):
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()


    def stop(self):
        self.timer.stop()

    def hide_graph_1(self):
        self.graph_1_visibility = not self.graph_1_visibility
        self.changing_visiblty()


    def update_plot(self):
        left, right = self.axes.get_xlim()
        if (right > self.max_time):
            return
        self.axes.set_xlim(left = left+self.step , right = right+self.step)
        self.draw()

    def PrintedImage(self):
        self.fig.savefig('graph.png', bbox_inches='tight',transparent=True, pad_inches=0)

    def increase_speed(self):
        self.step  = self.step*2

    def decrease_speed(self):
        self.step = self.step/2
