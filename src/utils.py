import pandas as pd
import os
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
import numpy as np


def load_ecg():
    loaded_ECG_data = pd.read_csv("src/data/ECG.csv")
    ecg = loaded_ECG_data['filtered_ECG_mV'].to_numpy().tolist()
    time = loaded_ECG_data['time_sec'].to_numpy().tolist()

    return (time, ecg)

def is_csv(path):
    file_name = path.split(os.path.sep)[-1]
    return file_name.find(".csv") != -1

def open_csv(window):
    path,_ = qtw.QFileDialog.getOpenFileName(window, 'Open File')
    return load_csv(path)

def load_csv(path):
    name = path.split(os.path.sep)[-1]
    if name and name.__contains__('.csv'):
        loaded_data = pd.read_csv(path)
        time  = loaded_data['time'].to_numpy().tolist()
        values = loaded_data['values'].to_numpy().tolist()
        return (True, name, (time, values))
    else:
        return (False, None, None)

def Signal_Statistics(signal_x,signal_y):
    mean = np.mean(signal_y)
    std = np.std(signal_y)
    v_max = np.max(signal_y)
    v_min = np.min(signal_y)
    return [mean,std,v_min,v_max]
