#UPDATED 16/8
from itertools import count
import mne
import matplotlib.pyplot as plt
import numpy as np
mne.sys_info()
mne.set_log_level('WARNING')
import random

misc =  ['EXG1','EXG2'] 
eog = []  
bads = ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8']
raw = mne.io.read_raw_bdf( 'C:/Users/pedro/Documents/Doctorado/Biosemi/celina_ob_v4.bdf', preload=True, verbose=True, eog=eog, misc=misc, exclude=bads)
#celina_ob_v4.bdf son mediciones hechas el 8/8 con Celina. Script: Oddbal_V4
sfreq = raw.info['sfreq']

raw.notch_filter(50,picks=['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D32', 'EXG1', 'EXG2'],filter_length='auto', phase='zero')
# Notch Filter

raw.set_montage("biosemi128", on_missing='ignore')
raw.set_eeg_reference(ref_channels=['EXG1','EXG2'])
#EXG1 and EXG2 are the references, placed in left and right mastoid, respectively.

raw.filter(1,6, l_trans_bandwidth=1, h_trans_bandwidth=1)
#raw.plot(block=True, title='Check the channels after spectral frequencies')

nfreq = 256
raw.resample(nfreq)
#Resample to nfreq

data = raw._data[0:130,:]
#Channels with data

status = raw._data[130]
#Channels with triggers. 75: Frequent (normal) stimulus; 175: Odd stimulus

size_d = data.shape
#print(size_d)
size_s = status.size
#print(size_s)

vector_norm1 = np.zeros((130,nfreq))
vector_norm2 = np.zeros((130,nfreq))
vector_norm3 = np.zeros((130,nfreq))
vector_norm4 = np.zeros((130,nfreq))

count_norm = 0
vector_odd = np.zeros((130,nfreq))
count_odd = 0
count_trigger=0
coco1=0
coco2=0
coco3=0
coco4=0

for x in range(size_s):
    if status[x] == 75 and count_norm<81:
        #Firsts 20 frequent stimuli
        if count_norm > -1 and count_norm < 21:
            new_vector = data[:,x:x+256]
            vector_norm1 = vector_norm1 + new_vector
            coco1=coco1+1
            count_norm = count_norm + 1
        #Seconds 20 
        if count_norm > 20 and count_norm <41:
            new_vector = data[:,x:x+256]
            vector_norm2 = vector_norm2 + new_vector
            coco2=coco2+1
            count_norm = count_norm + 1
        #Thirds 20 frequent stimuli
        if count_norm > 40 and count_norm < 61:
            new_vector = data[:,x:x+256]
            vector_norm3 = vector_norm3 + new_vector
            coco3=coco3+1
            count_norm = count_norm + 1
        #Fourth 20 frequent stimuli
        if count_norm > 60 and count_norm <81:
            new_vector = data[:,x:x+256]
            vector_norm4 = vector_norm4 + new_vector
            coco4=coco4+1
            count_norm = count_norm + 1
    #Odd stimuli
    if status[x] == 175 and count_odd<21:
        new_vector = data[:,x:x+256]
        vector_odd = vector_odd + new_vector
        count_odd = count_odd + 1
    # if status[x]==75 or status[x]==175:
    #     number = random.randint(0,1)
    #     if number==0 and count_norm<21:
    #         if count_norm > -1:
    #             new_vector = data[:,x:x+256]
    #             vector_norm = vector_norm + new_vector
    #             count_norm = count_norm + 1
    #     elif count_odd<21:
    #         new_vector = data[:,x:x+256]
    #         vector_odd = vector_odd + new_vector
    #         count_odd = count_odd + 1   
        
vector_norm1 = vector_norm1 / 20
vector_norm2 = vector_norm2 / 20
vector_norm3 = vector_norm3 / 20
vector_norm4 = vector_norm4 / 20

#print(vector_norm.shape)

vector_odd = vector_odd / 20
# print(vector_odd.shape)

print(count_norm, count_odd, coco1, coco2, coco3, coco4)

ch=0
x=np.linspace(0, 1000.0, num=256)
plt.title("Oddball") 
plt.xlabel("Miliseconds (ms)") 
plt.ylabel("Volts (V)") 
plt.plot(x,vector_odd[ch,:],color='r',label='Odd') 
plt.plot(x,vector_norm1[ch,:],color='g',label='Frequent1') 
plt.plot(x,vector_norm2[ch,:],color='mediumseagreen',label='Frequent2') 
plt.plot(x,vector_norm3[ch,:],color='limegreen',label='Frequent3') 
plt.plot(x,vector_norm4[ch,:],color='springgreen',label='Frequent4') 

print('Plotting channel: ',raw.ch_names[ch])
plt.legend()
plt.show()
