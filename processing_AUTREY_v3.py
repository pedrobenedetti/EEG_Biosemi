## UPDATED 9/2/2023
## processing_AUTREY_v3.py is the same that processing_AUTREY_v2.py but includes an aditional resting at begining of protocol.

import mne
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
mne.sys_info()
mne.set_log_level('WARNING')
import random
import os

## PAGE ### TITLE ########## TIME MARK ##
## -1       PARTICIPANT CODE    -- ######
## 0        RESTING             02 ######
## 1        PART 1 TITLE        10 ######
## 2        INST. AUT           20 ######
## 3        THINK AUT           30 ######
## 4        AUT                 45 ######    
## 5        PART 2 TITLE        50 ######
## 6        INST REY            60 ######
## 7        THINK REY           70 ######
## 8        REY                 85 ######
## 9        THANKS              90 ######
## 10       RESTING             100 #####       
## 11       SAVING/END          110 #####
#########################################

misc =  ['EXG1','EXG2'] 
eog = []  
bads = ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8',
        'B29', 'B30', 'B31', 'C10', 'D10','D11', 'D12']

filepath = 'C:/Users/pbenedetti/Documents/Doctorado/Biosemi/Senales/aut_02.bdf'
raw = mne.io.read_raw_bdf(filepath, 
                          preload=True, verbose=True, 
                          eog=eog, misc=misc, exclude=bads)

sfreq = raw.info['sfreq']

raw.notch_filter(50,
                 picks=['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'C1', 'C2', 'C3','C4','C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D32', 'EXG1', 'EXG2'],filter_length='auto', phase='zero')
raw.plot(block=True, title='Carefully identify wrong channels')
raw.set_montage("biosemi128", on_missing='ignore')
#raw.set_eeg_reference(ref_channels=['EXG1','EXG2'])
raw.set_eeg_reference("average")

raw.filter(1,20, 
           l_trans_bandwidth=1, h_trans_bandwidth=1)
#raw.plot(block=True, title='Check the channels after spectral frequencies')

nfreq = 256
raw.resample(nfreq)
#raw.plot(block=True, title='Check the channels after spectral frequencies')

#raw.plot_psd(fmax=80.0)

events = mne.find_events(raw, stim_channel='Status')
reject_criteria = dict(eeg=75e-6)      # 75 µV
                      

epochs = mne.Epochs(raw, 
                    events, 
                    tmin=0, tmax=60,
                    baseline=(0, 0),
                    reject=reject_criteria,
                    preload=True)
#epochs.plot()
#evoked_interp = epochs.copy().interpolate_bads(reset_bads=False)

think = mne.pick_events(events, include=[30, 45, 70, 85, 100])
think_dict = {'AUT think': 30,'AUT': 45, 'REY think': 70, 'REY': 85, 'Resting2': 100}
# think = mne.pick_events(events, include=[2, 30, 45, 70, 85, 100])
# think_dict = {'Resting1': 2, 'AUT think': 30,'AUT': 45, 'REY think': 70, 'REY': 85, 'Resting2': 100}


epochs_think = mne.Epochs(raw, 
                    think, 
                    tmin=0, tmax=60, 
                    baseline=(0, 0),
                    event_id=think_dict, 
                    preload=True)

#epochs.plot(events = think, event_id=think_dict)

# epochs_think['AUT think'].plot_psd(fmin=2, fmax=16)
# epochs_think['AUT'].plot_psd(fmin=2, fmax=16)
# epochs_think['REY think'].plot_psd(fmin=2, fmax=16)
# epochs_think['REY'].plot_psd(fmin=2, fmax=16)

#bands = {'Alpha':(8,12), 'Lower alpha':(8,10), 'Upper alpha': (10,12)}

bands = {'Theta':(4,8), 'Alpha':(8,12)}
#bands = {'Theta':(4,8), 'Alpha':(8,12) , 'Low Beta': (14,18)}

# spectrum_resting1 = epochs_think['Resting1'].compute_psd()
# spectrum_resting1.plot_topomap(bands=bands,show_names=False, cmap = 'Reds')

spectrum_AUT_th = epochs_think['AUT think'].compute_psd()
spectrum_AUT_th.plot_topomap(bands=bands,show_names=False, cmap = 'Reds')

spectrum_AUT = epochs_think['AUT'].compute_psd()
spectrum_AUT.plot_topomap(bands=bands,show_names=False, cmap = 'Reds')

spectrum_REY_th = epochs_think['REY think'].compute_psd()
spectrum_REY_th.plot_topomap(bands=bands,show_names=False, cmap = 'Reds')

spectrum_REY = epochs_think['REY'].compute_psd()
spectrum_REY.plot_topomap(bands=bands,show_names=False, cmap = 'Reds')

spectrum_resting2 = epochs_think['Resting2'].compute_psd()
spectrum_resting2.plot_topomap(bands=bands,show_names=False, cmap = 'Reds')

plt.show()