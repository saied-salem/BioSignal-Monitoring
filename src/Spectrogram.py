import matplotlib.pyplot as plt
from skimage import exposure
from matplotlib.backends.backend_qt5agg\
     import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from SignalsStore import SignalsStore
from PIL import Image

class Spectrogram(qtw.QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/spectrogram.ui", self)
        canvas_layout = self.findChild(qtw.QVBoxLayout, "spectrogram_canvas")
        self.spectrogram_canvas = SpectrogramCanvas()
        self.spectrogram_canvas.setMinimumSize(2.1,100)
        canvas_layout.addWidget(self.spectrogram_canvas)

        self.signals_store = SignalsStore()
        self.time, self.signal = [],[]

        self.palates.currentIndexChanged.connect(self.updatePalate)
        self.current_channel.currentIndexChanged.connect(self.updateChannel)
        self.update_intensity_btn.clicked.connect(self.updateIntinsity)

    def updatePalate(self):
        curr_palate = self.palates.currentText()
        self.spectrogram_canvas.updatePalate(curr_palate)

    def updateIntinsity(self):
        min_in = self.min_intensity.value()
        max_in = self.max_intensity.value()
        self.spectrogram_canvas.updateIntinsity(min_in, max_in)

    def updateChannelsList(self):
        self.current_channel.clear()
        self.current_channel.addItems(self.signals_store.getChannelsNames())


    def updateChannel(self):
        curr_channel_num = self.current_channel.currentIndex()
        if curr_channel_num >= 0:
            _, (self.time, self.signal) = self.signals_store.getChannel(curr_channel_num)
            self.spectrogram_canvas.updateSignal(self.time, self.signal)

    def updateSpecgramImage(self):
        self.spectrogram_canvas.specgramImage()


class SpectrogramCanvas(FigureCanvas):
    def __init__(self, width=100, height=5):
        self.fig, self.ax = plt.subplots(figsize=(width, height), facecolor="#EFEFEF")
        self.spectrogram, self.spectrogram_image = None, None
        self.time, self.signal = None, None
        self.processed_specgram = None
        super().__init__(self.fig)

    def updateSignal(self, time, signal):
        self.ax.cla()
        self.time, self.signal = time, signal
        self.spectrogram_image = self.updateSpectogram(time, signal, 'plasma')
        self.ax.axis('off')
        self.draw()

    def updateSpectogram(self, time, signal, palate):
        sampling_freq = time.index(1)
        self.spectrogram = self.ax.specgram(
            signal, Fs=sampling_freq, scale='dB', cmap=palate
        )[3]
        return self.spectrogram.make_image(self.ax)[0]

    def updatePalate(self, palate):
        self.ax.cla()
        self.spectrogram_image = self.updateSpectogram(self.time, self.signal, palate)
        self.draw()

    def updateIntinsity(self, min_in, max_in):
        if(max_in > min_in):
            self.processed_specgram = exposure.rescale_intensity(
                self.spectrogram_image, in_range=(min_in, max_in)
            )
            self.ax.imshow( self.processed_specgram, origin='lower', aspect='auto')
            self.draw()

    def specgramImage(self):
        self.fig.savefig('specgram.png', bbox_inches='tight',transparent=True, pad_inches=0)
