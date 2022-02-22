from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic
import utils


class DropSignal(qtw.QDialog):
    signalDropped = qtc.pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/drop_signal.ui", self)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if utils.is_csv(event.mimeData().text()):
            event.accept()
        else: event.ignore()

    def dragMoveEvent(self, event):
        if utils.is_csv(event.mimeData().text()):
            event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        if utils.is_csv(file_path):
            self.loadSignal(file_path)
            event.accept()
        else:
            event.ignore()


    def loadSignal(self, file_path):
        loaded, signal_name, signal_data = utils.load_csv(file_path)
        if loaded:
            self.signalDropped.emit((signal_name, signal_data))
