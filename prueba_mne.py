import mne 
import matplotlib.pyplot as plt
import numpy

mne.sys_info()

mne.set_log_level('WARNING')

misc =  []
eog = []  #aca podes poner algun canal que quieras que se asuma como EOG
bads = []

# BADS lo podes usar para marcar los canales chotos, entonces
# al cargar el BDF te excluye completamente esos canales

raw = mne.io.read_raw_bdf( 'D:\Doctorado\Biosemi\pedro_benedetti_prueba_1.bdf', preload=True, verbose=True, eog=eog, misc=misc, exclude=bads)

# O la otra opcion que tenes es dejar que MNE te detecte
# los canales chotos con un algoritmo interno que en general
# funciona bien.  Te saca esos canales y te los interpola con 
# un filtro laplaciano espacial con los de alrededor.
raw.interpolate_bads()

# frecuencia de sampleo en el BDF
sfreq = raw.info['sfreq']

# Esto te va a servir para ver si esta todo ok. Lo navegas con las flecas
raw.plot(block=True, title='Carefully identify wrong channels')

# en raw.info.ch_names tenes todos los canales con sus nombres


# Filtro de notch para eliminar el 50 Hz de la linea
raw.notch_filter(50,picks=[1,2],filter_length='auto', phase='zero')

# Montage de los electrodos
raw.set_montage("standard_1020", on_missing='ignore')


# Setear la referencia, en tu caso deja "average"
raw.set_eeg_reference("average")
#raw.set_eeg_reference(ref_channels=['EXG1','EXG2'])
raw.plot_psd(fmax=80.0)
raw.filter(1,15, l_trans_bandwidth=1, h_trans_bandwidth=1)
raw.plot_psd(fmax=80.0)
raw.plot(block=True, title='Check the channels after spectral frequencies')

raw.plot_sensors(show_names=True)
fig = raw.plot_sensors('3d')
plt.show()

# Bajarle el resampleo hasta donde quieras
nfreq = 128

raw.resample( nfreq )

# Chequear el efecto del ajuste de la referencia
if (False):
    for proj in (False, True):
        with mne.viz.use_browser_backend('matplotlib'):
            fig = raw.plot(n_channels=5, proj=proj, scalings=dict(eeg=50e-6))
        fig.subplots_adjust(top=0.9)  # make room for title
        ref = 'Average' if proj else 'No'
        fig.suptitle(f'{ref} reference', size='xx-large', weight='bold')

    plt.show()