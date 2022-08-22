#LAST UPDATE: 19/8
#Script for processing data from 'oddball_V4.py'
from pickle import TRUE
import mne
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
mne.sys_info()
mne.set_log_level('WARNING')
import random
import os

randomize_labels = False 
#If 'randomize_labels' is TRUE it will randomize the labels of the epochs and decorrelate form them.

misc =  ['EXG1','EXG2'] 
eog = []  
bads = ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8']

filepath = 'C:/Users/pedro/Documents/Doctorado/Biosemi/celina_ob_v4.bdf'
raw = mne.io.read_raw_bdf(filepath, 
                          preload=True, verbose=True, 
                          eog=eog, misc=misc, exclude=bads)

sfreq = raw.info['sfreq']

raw.notch_filter(50,
                 picks=['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D32', 'EXG1', 'EXG2'],filter_length='auto', phase='zero')
# Notch Filter in 50 Hz

raw.set_montage("biosemi128", on_missing='ignore')
raw.set_eeg_reference(ref_channels=['EXG1','EXG2'])
#EXG1 and EXG2 are the references, placed in left and right mastoid, respectively.

raw.filter(1,6, 
           l_trans_bandwidth=1, h_trans_bandwidth=1)
#raw.plot(block=True, title='Check the channels after spectral frequencies')

nfreq = 256
raw.resample(nfreq)
#Resample to nfreq

events = mne.find_events(raw, stim_channel='Status')
event_dict = {'Begin': 20, 'Start': 25, 'Frequent': 75,
              'Odd': 175, 'End': 250}

stimuli_dict = {'Frequent': 75,'Odd': 175}
stimuli = mne.pick_events(events, include=[75, 175])

epochs = mne.Epochs(raw, 
                    stimuli, 
                    tmin=-0.1, tmax=0.7, 
                    baseline=(-0.1, 0),
                    event_id=stimuli_dict, 
                    preload=True)
#epochs.plot(events = stimuli, event_id=event_dict, event_color=dict(Frequent='mediumseagreen', Odd='red'))
#print(epochs)

if randomize_labels:
    epochs_rand = mne.Epochs(raw, 
                    stimuli, 
                    tmin=-0.1, tmax=0.7, 
                    baseline=(-0.1, 0),
                    event_id=stimuli_dict, 
                    preload=True)
    
    labels = np.zeros(epochs_rand.events.shape[0])
    labels_rand = np.zeros(epochs_rand.events.shape[0])

    counter = 0
    for x in epochs_rand.events:
        labels[counter] = x[2]
        counter = counter + 1
        print(counter, x[2])
        
    labels_rand = labels.copy()
    np.random.shuffle(labels_rand)
    
    counter = 0
    for x in epochs_rand.events:
        epochs_rand.events[counter][2] = labels_rand[counter]
        print(counter, epochs_rand.events[counter][2])
        counter = counter + 1
    evoked = epochs_rand.average()
    evoked_odd = epochs_rand['Odd'][:17].average()
    evoked_freq = epochs_rand['Frequent'][:17].average() 
else:

    evoked = epochs.average()
    evoked_odd = epochs['Odd'][:17].average()
    evoked_freq = epochs['Frequent'][:17].average()

del raw
# evoked_freq.plot(picks=['A1'],spatial_colors=True)
# evoked_odd.plot(picks=['A1'],spatial_colors=True)

dirname, basename = os.path.split(filepath)
if randomize_labels:
    basename = basename + ' Randomized'
mne.viz.plot_compare_evokeds([evoked_freq, evoked_odd], 
                             picks = 'A1',
                             colors = ['mediumseagreen', 'red', 'black'],
                             title = basename + ' (Cz)',ci=True,
                             ylim = dict(eeg=[-8, 8]),
                             invert_y = False)

plt.show()
