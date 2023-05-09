from scipy.stats import wilcoxon
import pandas as pd
import numpy as np
import mne
import matplotlib.pyplot as plt

R1 = pd.read_excel(r'C:/Users/pedro/Desktop/Libro1.xlsx', sheet_name='Resting 1')
AUT = pd.read_excel(r'C:/Users/pedro/Desktop/Libro1.xlsx', sheet_name='AUT')
REY = pd.read_excel(r'C:/Users/pedro/Desktop/Libro1.xlsx', sheet_name='REY')
R2 = pd.read_excel(r'C:/Users/pedro/Desktop/Libro1.xlsx', sheet_name='Resting 2')


print("########################### RESTING 1 ###########################")
print(R1)
print("")

print("########################### AUT ###########################")
print(AUT)
print("")

print("########################### REY ###########################")
print(REY)
print("")

print("########################### RESTING 2 ###########################")
print(R2)

channels = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 
            'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 
            'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 
            'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D32']

output=pd.DataFrame()
p_r1_aut = []
p_r1_rey = []
p_aut_rey = []
p_r2_aut = []
p_r2_rey = []

for ch in channels :
    #print(ch)
    r1 = R1[ch]
    aut = AUT[ch]
    rey = REY[ch]
    r2 = R2[ch]

    res1 = wilcoxon(r1,aut,nan_policy='omit')
    res2 = wilcoxon(r1,rey,nan_policy='omit')
    res3 = wilcoxon(aut,rey,nan_policy='omit')
    res4 = wilcoxon(r2,aut,nan_policy='omit')
    res5 = wilcoxon(r2,rey,nan_policy='omit')

    p_r1_aut.append(res1.pvalue)
    p_r1_rey.append(res2.pvalue)
    p_aut_rey.append(res3.pvalue)
    p_r2_aut.append(res4.pvalue)
    p_r2_rey.append(res5.pvalue)
    
    
    
    
##################################################
misc =  ['EXG1','EXG2'] 
eog = []  
bads = ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8']
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
think = mne.pick_events(events, include=[2, 30, 45, 70, 85, 100])
think_dict = {'Resting1': 2, 'AUT think': 30,'AUT': 45, 'REY think': 70, 'REY': 85, 'Resting2': 100}

epochs_think = mne.Epochs(raw, 
                    think, 
                    tmin=0, tmax=60, 
                    baseline=(0, 0),
                    event_id=think_dict, 
                    #reject=reject_criteria,
                    preload=True)
spectrum_resting1 = epochs_think['Resting1'].compute_psd()
spectrum_resting1.plot_topomap(show_names=False, cmap = 'Reds')
####################


mne.viz.plot_topomap(p_aut_rey,(128,2))
# print(p_r1_aut)
# print(p_r1_rey)
# print(p_aut_rey)
# print(p_r2_aut)
# print(p_r2_rey)
# output = output.append({"channels": channels, "R1 and AUT": p_r1_aut, "R1 and REY": p_r1_rey, "REY and AUT": p_aut_rey,"R2 and AUT": p_r2_aut, "R2 and REY": p_r2_rey}, ignore_index=True)
# output.to_excel(r"C:/Users/pedro/Desktop/Output.xlsx", sheet_name="Hoja 1")
                   

