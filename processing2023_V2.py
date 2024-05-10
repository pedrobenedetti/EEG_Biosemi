from my_functions import *
import mne
from mne.preprocessing import create_eog_epochs
from mne.preprocessing import create_ecg_epochs

# Inspeccion visual de PSD, de canales en tiempo y de topomapas. Si se ven canales malos los sacamos. Anotamos.
# Autoreject: Aquellos canales que saquen mas del 20% de las epocas los eliminamos. Anotamos.
# ICA: Si alguno es raro lo eliminamos. Vemos sus detalles a ver que caracteristcas tiene para saber el origen de la falla. Anotamos.
file_name = "06_test_2023.bdf"
bad_channels = ["EXG1", "EXG2", "EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8", "B3"]
bad_ica_channels = [0, 1, 2, 4, 7, 8, 11, 12, 13, 23]
# bad_ica_channels = None

lims_graph = (80, 700)
# lims_graph = (None, None)

colors = "Reds"
# colors = 'Blues'
raw = preprocessing_mne(
    "G:/Mi unidad/Doctorado/Protocolo2023/senales/",
    file_name,
    bads=bad_channels,
    lowpass_cut=1,
    highpass_cut=20,
    raw_plot=False,
    filtered_plot=False,
    psd_plot=True,
    edit_marks=True,
)


# Hay que aplicar ICA sobre el raw y no el epoched https://pubmed.ncbi.nlm.nih.gov/19162199/
ica, raw_clean = make_ICA(
    raw,
    method="fastica",
    n_components=25,
    decim=3,
    random_state=23,
    reject_limit=500e-6,
    bad_ica_channels=bad_ica_channels,
    plot_ica_topo=True,
    plot_ica_time=True,
    plot_raw=True,
)
# 40: RESTING
# 60: REY THINKING
# 70: REY
# 100: AUT THINKING
# 110: AUT
events = mne.find_events(raw_clean, stim_channel="Status")
my_events = mne.pick_events(events, include=[40, 60, 70, 100, 110])
my_events_dict = {
    "Resting": 40,
    "REY Thinking": 60,
    "REY": 70,
    "AUT Thinking": 100,
    "AUT": 110,
}
reject_criteria = dict(eeg=500e-6)
epochs_think = mne.Epochs(
    raw_clean,
    my_events,
    tmin=0,
    tmax=30,
    baseline=(0, 0),
    event_id=my_events_dict,
    preload=True,
    reject=reject_criteria,
)
epochs_think.plot_drop_log()
epochs_think.plot()
# plt.show()
# print(epochs_think)

# ica, epochs_think_copy = make_ICA(epochs_think,method='fastica',n_components = 25,decim = 3,random_state = 23,reject_limit=500e-6,bad_ica_channels=bad_ica_channels,plot_ica_topo=True,plot_ica_time=True,plot_raw=True)
# ica.exclude =  bad_ica_channels # indices chosen based on various plots above
# VER ESTO
# ica.plot_properties(raw_copy, picks=0)
# plt.show()
bands = {"Alpha": (8, 12)}

spectrum_resting = epochs_think["Resting"].compute_psd()
spectrum_resting.plot_topomap(
    bands=bands, show_names=False, cmap=colors, vlim=lims_graph
)
plt.show()
spectrum_REY_th = epochs_think["REY Thinking"].compute_psd()
spectrum_REY_th.plot_topomap(
    bands=bands, show_names=False, cmap=colors, vlim=lims_graph
)
plt.show()
spectrum_REY = epochs_think["REY"].compute_psd()
spectrum_REY.plot_topomap(bands=bands, show_names=False, cmap=colors, vlim=lims_graph)
plt.show()
spectrum_AUT_th = epochs_think["AUT Thinking"].compute_psd()
spectrum_AUT_th.plot_topomap(
    bands=bands, show_names=False, cmap=colors, vlim=lims_graph
)
plt.show()
spectrum_AUT = epochs_think["AUT"].compute_psd()
spectrum_AUT.plot_topomap(bands=bands, show_names=False, cmap=colors, vlim=lims_graph)
plt.show()
# 100,2000
