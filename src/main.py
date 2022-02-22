import pandas as pd
import sys
import utils
from Page import Page
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from SignalsStore import SignalsStore
from PIL import Image
from PdfPrinter import printPdf


class MainApp(qtw.QApplication):
    """The main application object"""

    def __init__(self, argv):
        super().__init__(argv)

        self.main_window = MainWindow()
        self.main_window.show()


class MainWindow(qtw.QMainWindow):
    """The main application window"""

    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/main_window.ui", self)
        self.file_menu = self.findChild(qtw.QMenu, "menuFile")
        self.signals_store = SignalsStore()
        self.initMenu()
        self.initBody()


    def loadSignal(self):
        print("LOADING A SIGNAL")
        loaded, name, data = utils.open_csv(self)
        if loaded:
            channel_idx = self.signals_store.addChannel((name, data))
            self.view_page.updatePage()
            if channel_idx != None:
                print(f"CHANNEL STORED in {channel_idx}")
            else: print("NOT A DICT SIGNAL")
        else: print("CSV NOT LOADED")

    def outPdf(self):
        data = []
        for signal in self.signals_store._signals:
            _, (time, signal_values) = signal
            data.append(utils.Signal_Statistics(time, signal_values))
        self.view_page.spectrogram.updateSpecgramImage()
        self.view_page.signals_viewer.updatePrintedImage()
        graph = Image.open("graph.png")
        specgram = Image.open("specgram.png")
        printPdf(data, graph, specgram)
        print("PRINTED A SIGNAL")

    def initMenu(self):
        print("INIT MENU")
        openFile = self.findChild(qtw.QAction, "actionLoad_Signal")
        openFile.setShortcut("Ctrl+O")
        openFile.triggered.connect(self.loadSignal)

        openFile = self.findChild(qtw.QAction, "actionPrintSignal")
        openFile.setShortcut("Ctrl+P")
        openFile.triggered.connect(self.outPdf)

    def initBody(self):
        self.view_page = Page()
        central_layout = self.centralWidget().layout()
        central_layout.addWidget(self.view_page)

if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
