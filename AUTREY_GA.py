#LIBRARIES
import mne
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
mne.sys_info()
mne.set_log_level('WARNING')
import random
import os

misc =  ['EXG1','EXG2'] 
eog = []  
bands = {'Theta':(4,8), 'Alpha':(8,12)}
filepath = 'C:/Users/pbenedetti/Documents/Doctorado/Biosemi/Senales/'
evokeds_R1 = []
evokeds_AUTth = []
evokeds_AUT = []
evokeds_REYth = []
evokeds_REY = []
evokeds_R2 = []

subjects = ['aut_02',
         'aut_03',
         'aut3_05',
         'aut3_06']

bads=[['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','B29', 'B30', 'B31', 'C10', 'D10','D11', 'D12'],
      ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','C4', 'C28', 'C32', 'C27', 'A17'],
      ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','C3', 'D21','C7'],
      ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','C3','C7','C27', 'D20', 'D22', 'B22', 'B21', 'C32', 'D11', 'C4', 'D4']]


count = 0
for subject in subjects:
    file = filepath + subject
    bad = bads[count]
    raw = mne.io.read_raw_bdf(file+''+'.bdf', 
                          preload=True, verbose=True, 
                          eog=eog, misc=misc, exclude=bad)
    #PROCESSING
    sfreq = raw.info['sfreq']

    raw.notch_filter(50,
                    picks=['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'C1', 'C2', 'C3','C4','C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D32', 'EXG1', 'EXG2'],filter_length='auto', phase='zero')
    #raw.plot(block=True, title='Carefully identify wrong channels')
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

    #EPOCHS
    events = mne.find_events(raw, stim_channel='Status')

    my_events = mne.pick_events(events, include=[2, 30, 45, 70, 85, 100])
    if count == 0 or count == 1:
        my_events_dict = {'AUT think': 30,'AUT': 45, 'REY think': 70, 'REY': 85, 'Resting2': 100}
    else:
        my_events_dict = {'Resting1': 2, 'AUT think': 30,'AUT': 45, 'REY think': 70, 'REY': 85, 'Resting2': 100}

    epochs = mne.Epochs(raw, 
                        my_events, 
                        tmin=0, tmax=60, 
                        baseline=(0, 0),
                        event_id=my_events_dict, 
                        preload=True)
    if count > 1:
        evoked_resting1 = epochs['Resting1'].average()
        evokeds_R1.append(evoked_resting1)

    evoked_AUTth = epochs['AUT think'].average()
    evokeds_AUTth.append(evoked_AUTth)

    evoked_AUT = epochs['AUT'].average()
    evokeds_AUT.append(evoked_AUT)

    evoked_REYth = epochs['REY think'].average()
    evokeds_REYth.append(evoked_REYth)

    evoked_REY = epochs['REY'].average()
    evokeds_REY.append(evoked_REY)

    evoked_resting2 = epochs['Resting2'].average()
    evokeds_R2.append(evoked_resting2)
     
    count = count + 1

R1_grand_average=mne.grand_average(evokeds_R1)
AUTth_grand_average=mne.grand_average(evokeds_AUTth)
AUT_grand_average=mne.grand_average(evokeds_AUT)
REYth_grand_average=mne.grand_average(evokeds_REYth)
REY_grand_average=mne.grand_average(evokeds_REY)
R2_grand_average=mne.grand_average(evokeds_R2)

# R1_grand_average.plot_topomap()
# AUTth_grand_average.plot_topomap()
# AUT_grand_average.plot_topomap()
# REYth_grand_average.plot_topomap()
# REY_grand_average.plot_topomap()
# R2_grand_average.plot_topomap()

spectrum_resting1 = R1_grand_average.compute_psd()
spectrum_resting1.plot_topomap(bands=bands,show_names=False, cmap = 'RdBu_r')
spectrum_AUT_th = AUTth_grand_average.compute_psd()
spectrum_AUT_th.plot_topomap(bands=bands,show_names=False, cmap = 'RdBu_r')
spectrum_AUT = AUT_grand_average.compute_psd()
spectrum_AUT.plot_topomap(bands=bands,show_names=False, cmap = 'RdBu_r')
spectrum_REY_th = REYth_grand_average.compute_psd()
spectrum_REY_th.plot_topomap(bands=bands,show_names=False, cmap = 'RdBu_r')
spectrum_REY = REY_grand_average.compute_psd()
spectrum_REY.plot_topomap(bands=bands,show_names=False, cmap = 'RdBu_r')
spectrum_resting2 = R2_grand_average.compute_psd()
spectrum_resting2.plot_topomap(bands=bands,show_names=False, cmap = 'RdBu_r')

plt.show()


