## MY_FUNCTIONS.PY
##
import mne
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

mne.set_log_level("WARNING")
import random
import os

verbose = "error"
from mne.preprocessing import ICA


def preprocessing_mne(
    path,
    file,
    bads: list[str],
    lowpass_cut: int,
    highpass_cut: int,
    raw_plot: bool,
    filtered_plot: bool,
    psd_plot: bool,
    edit_marks: bool,
):
    misc = ["EXG1", "EXG2"]
    eog = []
    filepath = path + file
    raw = mne.io.read_raw_bdf(
        filepath, preload=True, verbose=False, eog=eog, misc=misc, exclude=bads
    )
    sfreq = raw.info["sfreq"]
    raw.notch_filter(50)
    raw.set_montage("biosemi128", on_missing="ignore")
    # raw.set_eeg_reference(ref_channels=['EXG1','EXG2'])
    raw.set_eeg_reference("average")
    if raw_plot:
        raw.plot(block=True, title="Carefully identify wrong channels")
        plt.show()
    raw.filter(lowpass_cut, highpass_cut, l_trans_bandwidth=1, h_trans_bandwidth=1)
    # raw.plot(block=True, title='Check the channels after spectral frequencies')
    nfreq = 256
    raw.resample(nfreq)

    if filtered_plot:
        raw.plot(block=True, title="Check the channels after spectral frequencies")
        plt.show()
    if psd_plot:
        raw.plot_psd(fmax=30.0)
        plt.show()
    if edit_marks:
        last_ch = len(raw.ch_names) - 1
        old_separation = 30.0
        new_separation = 5.0
        coef = old_separation / new_separation

        previous_value = None  # previous value in vector raw._data[last_ch]
        last_mark = 0.0  # last mark (value different from zero)
        count_zeros = 0.0  # cant of zeros since last mark
        inserted_POS = None  # position where last inserted mark was placed
        last_mark_POS = 0  # position where last original mark was founded
        current_POS = 0  # position counter
        flag = 0.0
        # plt.plot(raw._data[last_ch])
        # plt.show()
        for x in raw._data[last_ch]:

            if x < 255:
                if x != 0:
                    if x != previous_value:
                        # if x == last_mark:
                        separation = (
                            count_zeros // coef
                        )  # separation between two equals marks will be divided by the coef
                        separation = 1280
                        inserted_POS = last_mark_POS

                        for i in range(last_mark_POS, current_POS):
                            if (i - inserted_POS) >= separation:
                                raw._data[last_ch][i] = last_mark
                                inserted_POS = i
                        last_mark = x
                        last_mark_POS = current_POS
                    count_zeros = 0
                else:
                    count_zeros = count_zeros + 1
            else:
                raw._data[last_ch][current_POS] = 0.0

            previous_value = x
            current_POS = current_POS + 1
        plt.plot(raw._data[last_ch])
        plt.show()
        events = mne.find_events(raw, stim_channel="Status")
        print(events)

    return raw


def select_bads(path: str, file: str, bads: list[str], v: int):
    misc = ["EXG1", "EXG2"]
    eog = []
    filepath = path + file
    raw = mne.io.read_raw_bdf(
        filepath, preload=True, verbose=False, eog=eog, misc=misc, exclude=bads
    )
    sfreq = raw.info["sfreq"]
    raw.notch_filter(50)
    raw.set_montage("biosemi128", on_missing="ignore")
    # raw.set_eeg_reference(ref_channels=['EXG1','EXG2'])
    nfreq = 256
    raw.resample(nfreq)
    events = mne.find_events(raw, stim_channel="Status")
    epochs = mne.Epochs(raw, events, tmin=0, tmax=6, baseline=(0, 0), preload=True)
    print(epochs)
    if v == 2:
        think = mne.pick_events(events, include=[30, 45, 70, 85, 100])
        think_dict = {
            "AUT think": 30,
            "AUT": 45,
            "REY think": 70,
            "REY": 85,
            "Resting2": 100,
        }
    else:
        think = mne.pick_events(events, include=[2, 30, 45, 70, 85, 100])
        think_dict = {
            "Resting1": 2,
            "AUT think": 30,
            "AUT": 45,
            "REY think": 70,
            "REY": 85,
            "Resting2": 100,
        }

    epochs_think = mne.Epochs(
        raw, think, tmin=0, tmax=60, baseline=(0, 0), event_id=think_dict, preload=True
    )

    epochs_think.plot(events=think, event_id=think_dict)
    plt.show()

    print(raw.info["bads"])
    # raw.info["bads"].extend(['C29','C30','C16','C17','D12','C27','C13','D4','D6','C4'])


def topomap_values(
    epochs: mne.Epochs, condition: str, bads: list[str], my_fmin: int, my_fmax: int
):
    """
    Takes one set of epochs and one condition and returns the mean values of power spectral density between two frequencies for each electrode.
    Electrode output is ordered from A1 to D32. If one electrode is missing because is bad, it wil be replaced with a blank space
    """
    # SEE: mne.viz.plot_epochs_psd_topomap
    channels = [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "A10",
        "A11",
        "A12",
        "A13",
        "A14",
        "A15",
        "A16",
        "A17",
        "A18",
        "A19",
        "A20",
        "A21",
        "A22",
        "A23",
        "A24",
        "A25",
        "A26",
        "A27",
        "A28",
        "A29",
        "A30",
        "A31",
        "A32",
        "B1",
        "B2",
        "B3",
        "B4",
        "B5",
        "B6",
        "B7",
        "B8",
        "B9",
        "B10",
        "B11",
        "B12",
        "B13",
        "B14",
        "B15",
        "B16",
        "B17",
        "B18",
        "B19",
        "B20",
        "B21",
        "B22",
        "B23",
        "B24",
        "B25",
        "B26",
        "B27",
        "B28",
        "B29",
        "B30",
        "B31",
        "B32",
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "C6",
        "C7",
        "C8",
        "C9",
        "C10",
        "C11",
        "C12",
        "C13",
        "C14",
        "C15",
        "C16",
        "C17",
        "C18",
        "C19",
        "C20",
        "C21",
        "C22",
        "C23",
        "C24",
        "C25",
        "C26",
        "C27",
        "C28",
        "C29",
        "C30",
        "C31",
        "C32",
        "D1",
        "D2",
        "D3",
        "D4",
        "D5",
        "D6",
        "D7",
        "D8",
        "D9",
        "D10",
        "D11",
        "D12",
        "D13",
        "D14",
        "D15",
        "D16",
        "D17",
        "D18",
        "D19",
        "D20",
        "D21",
        "D22",
        "D23",
        "D24",
        "D25",
        "D26",
        "D27",
        "D28",
        "D29",
        "D30",
        "D31",
        "D32",
    ]

    spectrum = epochs[condition].compute_psd(fmin=my_fmin, fmax=my_fmax)
    values = []
    count = 0

    for channel in spectrum._data[0]:
        while channels[count] in bads:
            values.append(np.nan)
            # If channel is bad, appends a blank space.
            count = count + 1
        channel_value = np.mean(channel)
        values.append(channel_value)
        # If channel is not bad, calculates its mean across time and appends it.
        count = count + 1
    # print('')
    # print('############# ' + condition + ' values #############')
    # print(values)
    return values


def stats_pvalues(condition1, condition2) -> list[list]:
    from scipy.stats import wilcoxon

    channels = [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "A10",
        "A11",
        "A12",
        "A13",
        "A14",
        "A15",
        "A16",
        "A17",
        "A18",
        "A19",
        "A20",
        "A21",
        "A22",
        "A23",
        "A24",
        "A25",
        "A26",
        "A27",
        "A28",
        "A29",
        "A30",
        "A31",
        "A32",
        "B1",
        "B2",
        "B3",
        "B4",
        "B5",
        "B6",
        "B7",
        "B8",
        "B9",
        "B10",
        "B11",
        "B12",
        "B13",
        "B14",
        "B15",
        "B16",
        "B17",
        "B18",
        "B19",
        "B20",
        "B21",
        "B22",
        "B23",
        "B24",
        "B25",
        "B26",
        "B27",
        "B28",
        "B29",
        "B30",
        "B31",
        "B32",
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "C6",
        "C7",
        "C8",
        "C9",
        "C10",
        "C11",
        "C12",
        "C13",
        "C14",
        "C15",
        "C16",
        "C17",
        "C18",
        "C19",
        "C20",
        "C21",
        "C22",
        "C23",
        "C24",
        "C25",
        "C26",
        "C27",
        "C28",
        "C29",
        "C30",
        "C31",
        "C32",
        "D1",
        "D2",
        "D3",
        "D4",
        "D5",
        "D6",
        "D7",
        "D8",
        "D9",
        "D10",
        "D11",
        "D12",
        "D13",
        "D14",
        "D15",
        "D16",
        "D17",
        "D18",
        "D19",
        "D20",
        "D21",
        "D22",
        "D23",
        "D24",
        "D25",
        "D26",
        "D27",
        "D28",
        "D29",
        "D30",
        "D31",
        "D32",
    ]

    p_values = []
    count_channel = 0
    count_condition = 0
    values_channel1 = []
    values_channel2 = []

    for channel in channels:
        for measure in condition1:
            values_channel_condition1 = condition1[count_condition][count_channel]
            values_channel1.append(values_channel_condition1)

            values_channel_condition2 = condition2[count_condition][count_channel]
            values_channel2.append(values_channel_condition2)

            count_condition = count_condition + 1
        count_condition = 0
        wilcoxon_1vs2 = wilcoxon(values_channel1, values_channel2, nan_policy="omit")
        p_values.append(wilcoxon_1vs2.pvalue)
        values_channel1 = []
        values_channel2 = []
        count_channel = count_channel + 1

    return p_values


def topomap_plot(epochs, title, p_values, binarize=True, inverse=False):

    t_min = 0
    p_values0 = p_values
    count = 0
    if binarize:
        for x in p_values0:
            if inverse == False:
                if p_values0[count] < 0.05:
                    p_values0[count] = [1]
                else:
                    p_values0[count] = [0]
            elif inverse == True:
                if p_values0[count] < 0.05:
                    p_values0[count] = [0]
                else:
                    p_values0[count] = [1]
            count = count + 1

    n_channels = len(epochs[0].info.ch_names) - 3
    if epochs.info["nchan"] != 128:
        epochs.drop_channels("Status")
    fake_evoked = mne.EvokedArray(p_values0, epochs[0].info)
    fix, ax = plt.subplots(
        ncols=2, figsize=(12, 5), gridspec_kw=dict(top=0.9), sharex=True, sharey=True
    )

    mne.viz.plot_sensors(fake_evoked.info, axes=ax[0], show=False)
    mne.viz.plot_topomap(
        fake_evoked.data[:, 0],
        fake_evoked.info,
        axes=ax[1],
        cmap="Reds",
        show=False,
        names=epochs[0].info.ch_names,
    )

    ax[0].set_title("Channels")
    ax[1].set_title([title])

    plt.savefig("./topomap.png")
    plt.show()


def make_ICA(
    raw,
    method: str,
    n_components: int,
    decim: int,
    random_state: int,
    reject_limit,
    bad_ica_channels,
    plot_ica_topo: bool,
    plot_ica_time: bool,
    plot_raw: bool,
):
    raw_clean = raw.copy()
    ica = ICA(n_components=n_components, method=method, random_state=random_state).fit(
        raw
    )  # Define the ICA object instance
    # print(ica)
    reject = dict(eeg=reject_limit)
    picks_eeg = mne.pick_types(
        raw.info, meg=False, eeg=True, eog=False, stim=False, exclude="bads"
    )
    # raw.plot()
    ica.fit(raw, picks=picks_eeg, decim=decim, reject=reject)
    if plot_ica_topo == True:
        ica.plot_components(title="ICA components topomaps")
        plt.show()
    if plot_ica_time == True:
        ica.plot_sources(raw, title="ICA components")
        plt.show()
    if bad_ica_channels != None:
        ica.exclude = bad_ica_channels  # indices chosen based on various plots above
    raw_clean = ica.apply(raw_clean)
    if plot_raw == True:
        raw.plot(title="raw")
        raw_clean.plot(title="Minus noisy ICA")
        plt.show()

    return ica, raw_clean


def prom_areas(epochs, condition):
    frontales = [
        "C8",
        "C9",
        "C10",
        "C12",
        "C13",
        "C14",
        "C15",
        "C16",
        "C17",
        "C18",
        "C19",
        "C20",
        "C21",
        "C25",
        "C26",
        "C27",
        "C28",
        "C29",
        "C30",
        "C31",
        "C32",
    ]
    temporales_left = [
        "D4",
        "D5",
        "D6",
        "D7",
        "D8",
        "D9",
        "D10",
        "D11",
        "D21",
        "D22",
        "D23",
        "D24",
        "D25",
        "D26",
        "D29",
        "D30",
        "D31",
        "D32",
    ]
    temporales_right = [
        "C4",
        "C5",
        "C6",
        "C7",
        "B10",
        "B11",
        "B12",
        "B13",
        "B14",
        "B15",
        "B16",
        "B24",
        "B25",
        "B26",
        "B27",
        "B28",
        "B29",
        "B30",
    ]
    occipital = [
        "A8",
        "A9",
        "A10",
        "A11",
        "A12",
        "A13",
        "A14",
        "A15",
        "A16",
        "A17",
        "A18",
        "A20",
        "A21",
        "A22",
        "A23",
        "A24",
        "A25",
        "A26",
        "A27",
        "A28",
        "A29",
        "A30",
        "A31",
        "B5",
        "B6",
        "B7",
        "B8",
        "B9",
    ]
    parietal = [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A19",
        "A32",
        "B1",
        "B2",
        "B3",
        "B4",
        "B17",
        "B18",
        "B19",
        "B20",
        "B21",
        "B22",
        "B23",
        "B31",
        "B32",
        "C1",
        "C2",
        "C3",
        "C11",
        "C22",
        "C23",
        "C24",
        "D1",
        "D2",
        "D3",
        "D12",
        "D13",
        "D14",
        "D15",
        "D16",
        "D17",
        "D18",
        "D19",
        "D20",
        "D27",
        "D28",
    ]

    spectrum = epochs[condition].compute_psd()
    count = 0

    fro_values = []
    temL_values = []
    temR_values = []
    occ_values = []
    par_values = []

    for channel in spectrum._data[0]:
        channel_value = np.mean(channel)
        channel_name = spectrum.ch_names[count]
        if channel_name in frontales:
            fro_values.append(channel_value)
        elif channel_name in temporales_left:
            temL_values.append(channel_value)
        elif channel_name in temporales_right:
            temR_values.append(channel_value)
        elif channel_name in occipital:
            occ_values.append(channel_value)
        elif channel_name in parietal:
            par_values.append(channel_value)
        count = count + 1
    fro_mean = np.mean(fro_values)
    temL_mean = np.mean(temL_values)
    temR_mean = np.mean(temR_values)
    occ_mean = np.mean(occ_values)
    par_mean = np.mean(par_values)

    return fro_mean, temL_mean, temR_mean, occ_mean, par_mean
