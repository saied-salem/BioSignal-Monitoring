from DropSignal import DropSignal
from SignalCanvas import SignalCanvas
from Spectrogram import Spectrogram
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from SignalsStore import SignalsStore
from SignalCanvas import SignalCanvas, NavigationToolbar, SignalViewer

class Page(qtw.QWidget):

    signal_loaded = qtc.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.initGlobals()
        self.initBody();

        self.drop_signal.signalDropped.connect(self.extendChannels)

    def extendChannels(self, channel):
        print("NEW CHANNEL LOADED")
        self.signals_store.addChannel(channel)
        self.updatePage()

    def updatePage(self):
        self.spectrogram.updateChannelsList()
        self.signals_viewer.signal_canvas.loadChannels()
        self.signals_viewer.udpateChannelsLabels()
        self.signals_viewer.signal_canvas.drawChannels()
        if not self.viewer_loaded:
            self.splitter.replaceWidget(0, self.signals_viewer)
            self.viewer_loaded = True
        self.signals_viewer.signal_canvas.play()


    def initBody(self):
        self.drop_signal = DropSignal()
        self.spectrogram = Spectrogram()
        self.signals_store = SignalsStore()
        self.signals_viewer = SignalViewer()

        self.toolbar = NavigationToolbar(self.signals_viewer.signal_canvas, self)
        self.splitter = qtw.QSplitter(qtc.Qt.Orientation.Vertical)
        self.layout().addWidget(self.toolbar)

        self.splitter.addWidget(self.drop_signal)
        self.splitter.addWidget(self.spectrogram)
        self.layout().addWidget(self.splitter)

    def initGlobals(self):
        self.viewer_loaded = False

