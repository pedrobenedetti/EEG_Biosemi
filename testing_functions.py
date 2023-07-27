#%%
import pandas as pd
import mne
import mne
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#mne.sys_info()
mne.set_log_level('WARNING')
verbose='error'

from my_functions import preprocessing_mne, topomap_values, stats_pvalues, select_bads, topomap_plot
path = 'C:/Users/pedro/Documents/Doctorado/AUT_y_REY/Senales/'
files = ['aut_02.bdf',
        'aut_03.bdf',
        'aut3_05.bdf',
        'aut3_07.bdf',
        'aut3_08.bdf',
        'aut3_09.bdf',
        'aut3_09.bdf']
versions = ['v2',
            'v2',
            'v3',
            'v3',
            'v3',
            'v3',
            'v3']
bads_all =      [['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','B8','B15','B16','B18','B27','B29','C7','C8','C9','C10','C15','C16','C17','C18','C28','C29','C30','C31','D10','D12'],
                 ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','A17','B25','B26','C4','C14','C15','C16','C27','C28','C29','C32','D1','D6','D29'],
                 ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','A11','A12','A13','A14','A15','A24','A25','A26','A27','A28','A29','B8','B9','B10','B11','B12','B13','B19','B27','B28','C3','C6','C7','C8','C9','C10','C11','D22','D23','D25','D31'],
                 ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','A18','B9','B14','B23','B26','B27','B28','C7','C8','C9','C30','D4','D11','D21','D22','D23','D24'],
                 ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','A4','A30','B29','C6','C8','C9','C14','C15','C16','C17','C26','D10','D22','D23','D24'],
                 ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','A4','A8','A9','A19','A20','A29','B3','B5','B16','C3','C4','C13','C14','C15','C16','C17','C18','C21','C28','C29','C30','C31','D6','D11','D19','D20','D26'],
                 ['EXG1','EXG2','EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8']]
# bads = ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','EXG1','EXG2']
# file = 'aut3_09.bdf'
r2 = []
aut = []
rey = []
count = 0
for file in files:
        print(file)
        bads = bads_all[count]
        raw = preprocessing_mne(path, file, bads, lowpass_cut=1,highpass_cut=20,raw_plot=False,filtered_plot=False,psd_plot=False)
        events = mne.find_events(raw, stim_channel='Status')
        epochs = mne.Epochs(raw, 
                        events, 
                        tmin=0, tmax=6,
                        baseline=(0, 0),
                        preload=True)
        if versions[count]=='v2':
                think = mne.pick_events(events, include=[30, 45, 70, 85, 100])
                think_dict = {'AUT think': 30,'AUT': 45, 'REY think': 70, 'REY': 85, 'Resting2': 100}
        else:
                think = mne.pick_events(events, include=[2, 30, 45, 70, 85, 100])
                think_dict = {'Resting1': 2, 'AUT think': 30,'AUT': 45, 'REY think': 70, 'REY': 85, 'Resting2': 100}
        epochs_think = mne.Epochs(raw, 
                        think, 
                        tmin=0, tmax=60, 
                        baseline=(0, 0),
                        event_id=think_dict,
                        preload=True)
        count = count + 1
        values_aut = topomap_values(epochs_think, condition='AUT', bads=bads, my_fmin=8, my_fmax=14)
        aut.append(values_aut)
        values_rey = topomap_values(epochs_think, condition='REY', bads=bads, my_fmin=8, my_fmax=14)
        rey.append(values_rey)
        values_r2 = topomap_values(epochs_think, condition='Resting2', bads=bads, my_fmin=8, my_fmax=14)
        r2.append(values_r2)
        
pvalues_aut_r2 = stats_pvalues(aut,r2)
pvalues_rey_r2 = stats_pvalues(rey,r2)
pvalues_aut_rey = stats_pvalues(aut,rey)

topomap_plot(epochs=epochs_think,title='AUT vs R2',p_values=pvalues_aut_r2,inverse=False)
topomap_plot(epochs=epochs_think,title='REY vs R2',p_values=pvalues_rey_r2,inverse=False)
topomap_plot(epochs=epochs_think,title='AUT vs REY',p_values=pvalues_aut_rey,inverse=True)

print(pvalues_aut_r2)
print(pvalues_rey_r2)
print(pvalues_aut_rey)


pvalues= []
count = 0
for channel in pvalues_aut_r2:
        if ((pvalues_aut_r2[count] == [1]) and (pvalues_rey_r2[count] == [1]) and (pvalues_aut_rey[count] == [0])):
                pvalues.append([1])
                print(count,'1')
        else:
                pvalues.append([0])
                print(count,'0')

        count+=1
        print(count,)
topomap_plot(epochs=epochs_think,title='AUTvsR2 + REYvsR2 - AUTvsREY',p_values=pvalues,binarize= False, inverse=False)
print(aut)
