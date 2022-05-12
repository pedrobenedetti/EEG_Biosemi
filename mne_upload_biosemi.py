#ACTUALIZADO 12/5
import mne
import matplotlib.pyplot as plt
import numpy

mne.sys_info()

mne.set_log_level('WARNING')

misc =  ['EXG1','EXG2'] 
#Miscelaneos: No son canales pero sirven para algo, no los descarto. Ej: EXG1 y EXG2 que son referencias.

eog = []  
#Canales que son de EOG.

bads = ['EXG3','EXG4', 'EXG5','EXG6','EXG7','EXG8', 'Status']
#Bads: Canales que vi y quiero descartar porque están malos/no tienen nada. Los excluye.


raw = mne.io.read_raw_bdf( 'D:\Doctorado\Biosemi\pedro_benedetti_prueba_1.bdf', preload=True, verbose=True, eog=eog, misc=misc, exclude=bads)
#Cargo el archivo.

raw.interpolate_bads()
# Otra opcion para los Bads que hay es dejar que MNE detecte
# los canales malos con un algoritmo interno que en general
# funciona bien.  Saca esos canales y los interpola con 
# un filtro laplaciano espacial con los de alrededor.

sfreq = raw.info['sfreq']
#Defino frecuencia de sampleo en el BDF

raw.plot(block=True, title='Carefully identify wrong channels')
#Gráfico de señales crudas. Sirve para ver si está todo OK.


#ch_names = raw.info.ch_names
#print(ch_names)
#Canales con sus nombres

raw.notch_filter(50,picks=['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D32', 'EXG1', 'EXG2'],filter_length='auto', phase='zero')
# Filtro de notch para eliminar el 50 Hz de la linea
#Picks: que canales son los que quiero filtrar


raw.set_montage("biosemi128", on_missing='ignore')
#raw.set_montage("standard_1020", on_missing='ignore')
#Montage de los electrodos, buscar en documentación las distintas opciones.


raw.set_eeg_reference(ref_channels=['EXG1','EXG2'])
#Seteo la referencia, Canales EXG1 y EXG2, que en mi caso son mastoideos izquierdo y derecho.
#Otra opción es dejar "average", asi:
#raw.set_eeg_reference("average")

raw.plot_psd(fmax=80.0)
#Ploteo en frecuencia, hasta 80Hz.

raw.filter(1,15, l_trans_bandwidth=1, h_trans_bandwidth=1)
#Filtro pasabanda de 1 a 15Hz, con lo siguiente defino el ripple.

raw.plot_psd(fmax=80.0)
#Ploteo en frecuencia, hasta 80Hz.

raw.plot(block=True, title='Check the channels after spectral frequencies')
#Vuelvo a plotear todos los canales en tiempo ya filtrados

raw.plot_sensors(show_names=True)
fig = raw.plot_sensors('3d')
plt.show()

nfreq = 128
raw.resample(nfreq)
#Resampleo a nfreq

# Chequear el efecto del ajuste de la referencia
if (False):
    for proj in (False, True):
        with mne.viz.use_browser_backend('matplotlib'):
            fig = raw.plot(n_channels=5, proj=proj, scalings=dict(eeg=50e-6))
        fig.subplots_adjust(top=0.9)  # make room for title
        ref = 'Average' if proj else 'No'
        fig.suptitle(f'{ref} reference', size='xx-large', weight='bold')

    plt.show()