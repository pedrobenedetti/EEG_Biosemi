from my_functions import *
import mne

raw = preprocessing_mne('C:/Users/pedro/Documents/Doctorado/protocol2023/Senales/','06_TEST_2023.bdf',
                  bads=['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8','B6','B16','B17','B30','D29'], lowpass_cut = 1, highpass_cut = 20, 
                  raw_plot = False, filtered_plot=False, psd_plot=False)

events = mne.find_events(raw, stim_channel='Status')
epochs = mne.Epochs(raw, 
                    events, 
                    tmin=0, tmax=30, 
                    baseline=(0, 0),
                    preload=True)


#40: RESTING
#60: REY THINKING
#70: REY
#100: AUT THINKING
#110: AUT
my_events = mne.pick_events(events, include=[40, 60, 70, 100, 110])
my_events_dict = {'Resting': 40,'REY Thinking': 60, 'REY': 70, 'AUT Thinking': 100, 'AUT': 110}

epochs_think = mne.Epochs(raw, 
                    my_events, 
                    tmin=0, tmax=30, 
                    baseline=(0, 0),
                    event_id=my_events_dict, 
                    preload=True)
epochs_think.plot()
plt.show()
print(epochs_think)
#epochs_think.plot(events = my_events, event_id=my_events_dict)

bands = {'Alpha':(8,12)}

spectrum_AUT_th = epochs_think['Resting'].compute_psd()
spectrum_AUT_th.plot_topomap(bands=bands,show_names=False, cmap = 'Reds')

spectrum_AUT = epochs_think['REY Thinking'].compute_psd()
spectrum_AUT.plot_topomap(bands=bands,show_names=False, cmap = 'Reds')

spectrum_REY_th = epochs_think['REY'].compute_psd()
spectrum_REY_th.plot_topomap(bands=bands,show_names=False, cmap = 'Reds')

spectrum_REY = epochs_think['AUT Thinking'].compute_psd()
spectrum_REY.plot_topomap(bands=bands,show_names=False, cmap = 'Reds')

spectrum_resting = epochs_think['AUT'].compute_psd() 
spectrum_resting.plot_topomap(bands=bands,show_names=False, cmap = 'Reds')


plt.show()