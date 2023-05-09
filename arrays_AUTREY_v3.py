## UPDATED 9/2/2023
## processing_AUTREY_v3.py is the same that processing_AUTREY_v2.py but includes an aditional resting at begining of protocol.

import mne
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#mne.sys_info()
mne.set_log_level('WARNING')
import random
import os
verbose='error'

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
bads = ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8']
#       ,'C21', 'B3', 'C3']

filepath = 'C:/Users/pedro/Documents/Doctorado/AUT_y_REY/Senales/aut3_09.bdf'
raw = mne.io.read_raw_bdf(filepath, 
                          preload=True, verbose=False, 
                          eog=eog, misc=misc, exclude=bads)

sfreq = raw.info['sfreq']

raw.notch_filter(50,
                 picks=['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'C1', 'C2', 'C3','C4','C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D32', 'EXG1', 'EXG2'],filter_length='auto', phase='zero')
raw.set_montage("biosemi128", on_missing='ignore')
raw.set_eeg_reference("average")

raw.filter(1,20, 
           l_trans_bandwidth=1, h_trans_bandwidth=1)

nfreq = 256
raw.resample(nfreq)

events = mne.find_events(raw, stim_channel='Status')

# think = mne.pick_events(events, include=[30, 45, 70, 85, 100])
# think_dict = {'AUT think': 30,'AUT': 45, 'REY think': 70, 'REY': 85, 'Resting2': 100}
think = mne.pick_events(events, include=[2, 30, 45, 70, 85, 100])
think_dict = {'Resting1': 2, 'AUT think': 30,'AUT': 45, 'REY think': 70, 'REY': 85, 'Resting2': 100}

epochs_think = mne.Epochs(raw, 
                    think, 
                    tmin=0, tmax=60, 
                    baseline=(0, 0),
                    event_id=think_dict, 
                    preload=True)


bands = {'Theta':(4,8), 'Alpha':(8,12)}
#bands = {'Theta':(4,8), 'Alpha':(8,12) , 'Low Beta': (14,18)}
#bands = {'Alpha':(8,12), 'Lower alpha':(8,10), 'Upper alpha': (10,12)}

#######
spectrum_resting1 = epochs_think['Resting1'].compute_psd(fmin=8, fmax=14)
resting1_array = []
for channel in spectrum_resting1._data[0]:
    channel_value = np.mean(channel)
    resting1_array.append(channel_value)
print('')
print('############# RESTING 1 #############')
print(resting1_array)
# print(spectrum_resting1._data)
# print(spectrum_resting1._data.shape)
#######

#######
spectrum_AUT_th = epochs_think['AUT think'].compute_psd(fmin=8, fmax=14)
AUT_th_array = []
for channel in spectrum_AUT_th._data[0]:
    channel_value = np.mean(channel)
    AUT_th_array.append(channel_value)
print('')
print('############# AUT Th #############')
print(AUT_th_array)
#######

#######
spectrum_AUT = epochs_think['AUT'].compute_psd(fmin=8, fmax=14)
AUT_array = []
for channel in spectrum_AUT._data[0]:
    channel_value = np.mean(channel)
    AUT_array.append(channel_value)
print('')
print('############# AUT #############')
print(AUT_array)
#######

#######
spectrum_REY_th = epochs_think['REY think'].compute_psd(fmin=8, fmax=14)
REY_th_array = []
for channel in spectrum_REY_th._data[0]:
    channel_value = np.mean(channel)
    REY_th_array.append(channel_value)
print('')
print('############# REY TH #############')
print(REY_th_array)
#######

#######
spectrum_REY = epochs_think['REY'].compute_psd(fmin=8, fmax=14)
REY_array = []
for channel in spectrum_REY._data[0]:
    channel_value = np.mean(channel)
    REY_array.append(channel_value)
print('')
print('############# REY #############')
print(REY_array)
#######

#######
spectrum_resting2 = epochs_think['Resting2'].compute_psd(fmin=8, fmax=14)
resting2_array = []
for channel in spectrum_resting2._data[0]:
    channel_value = np.mean(channel)
    resting2_array.append(channel_value)
print('')
print('############# RESTING 2 #############')
print(resting2_array)
#######
