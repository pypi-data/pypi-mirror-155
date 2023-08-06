import os
import numpy as np
import pandas as pd
import h5py

def getSpecificSignalMAT(path_sim, model_name, simNumber, list_Signals):

    simulationSignalsToPlot = pd.DataFrame()

    for i in range(len(simNumber)):
        path_simulationSignals = os.path.join(path_sim + str(simNumber[i]) + '.mat')
        with h5py.File(path_simulationSignals, 'r') as simulationSignals:
            for n in range(len(list_Signals)):
                simulationSignal = np.array(simulationSignals[list_Signals[n]])
                simulationSignal = simulationSignal.flatten().tolist()
                simulationSignal.insert(0, list_Signals[n]+'_'+str(simNumber[i]))
                simulationSignal = [simulationSignal]
                temp_frame = pd.DataFrame(simulationSignal)
                temp_frame.set_index(0, inplace=True)
                simulationSignalsToPlot = simulationSignalsToPlot.append(temp_frame)
    return simulationSignalsToPlot


def get_signals_from_mat(full_name_file: str, list_signals):
    '''
    Reads a mat file and returns a dataframe with the selected signals
    :param full_name_file: full path to the mat file
    :param list_signals: list of signals to read
    :return: dataframe with the selected signals
    '''

    with h5py.File(full_name_file, 'r') as simulationSignals:
        df_signals = pd.DataFrame()
        for signal in list_signals:
            simulationSignal = np.array(simulationSignals[signal])
            simulationSignal = simulationSignal.flatten().tolist()
            df = pd.DataFrame({signal: simulationSignal})
            df_signals = pd.concat([df_signals, df], axis=1)
    return df_signals
