#######LIBRARIES#######
import mne
import matplotlib.pyplot as plt
import sys
from my_functions import *
import numpy as np
import pandas as pd
import random
import os

misc = ["EXG1", "EXG2"]
eog = []
bands = {"Theta": (4, 8), "Alpha": (8, 12)}
filepath = (
    "G:/.shortcut-targets-by-id/1e4eps-xW_kig4_czWBgUZmR3FEylEJVo/IMAGINACION/Señales/"
)


# subjects = ["A1", "A2", "A3", "A5", "A6", "A7", "A8", "A9"]

# bads_preICA = [
#     ["EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8", "A8", "A9", "D5"],
#     [
#         "EXG3",
#         "EXG4",
#         "EXG5",
#         "EXG6",
#         "EXG7",
#         "EXG8",
#     ],
#     ["EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8", "D1", "D5"],
#     [
#         "EXG3",
#         "EXG4",
#         "EXG5",
#         "EXG6",
#         "EXG7",
#         "EXG8",
#         "B30",
#         "C10",
#         "C27",
#         "C28",
#         "C29",
#         "C30",
#     ],
#     ["EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8", "B22", "D17", "D26", "D27", "D28"],
#     [
#         "EXG3",
#         "EXG4",
#         "EXG5",
#         "EXG6",
#         "EXG7",
#         "EXG8",
#         "A26",
#         "A27",
#         "A28",
#         "A29",
#         "A30",
#         "A31",
#         "A32",
#         "B1",
#         "B2",
#         "B13",
#         "C16",
#     ],
#     [
#         "EXG3",
#         "EXG4",
#         "EXG5",
#         "EXG6",
#         "EXG7",
#         "EXG8",
#     ],
#     ["EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8", "C16", "C30", "D7"],
# ]

# bads_ICA = [
#     [1, 2, 3, 4, 5, 9, 10, 13, 19, 20, 22],
#     [0, 5, 6, 7, 8, 10, 15, 16, 17, 20, 21, 23, 24],
#     [0, 1, 2, 4, 7, 10, 11, 13, 18, 21],
#     [0, 1, 3, 8, 9, 14, 20, 22],
#     [0, 1, 2, 4, 5, 6, 7, 10, 11, 13, 14, 24],
#     [0, 8, 9, 13, 14, 18, 21],
#     [2, 3, 7, 10, 13, 14, 18, 22, 23, 24],
#     [0, 1, 8, 10, 16, 17, 20, 21, 22, 23],
# ]

# bads_postICA = [
#     ["C16", "C17", "C29", "C30"],
#     ["D8", "D9"],
#     ["C16", "C17", "C29", "C30"],
#     [],
#     ["C17"],
#     ["C8", "C9", "C15", "C17", "C29", "C30", "C31"],
#     [],
#     [],
# ]


subjects = [
    "C1",
    "C3",
    "C4",
    "C5",
    "C6",
    "C7",
    "C8",
    "C9",
]
bads_preICA = [
    ["EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8", "A8", "A12", "B1", "D21"],
    ["EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8", "A18", "B4", "D6", "D7", "D8"],
    [
        "EXG3",
        "EXG4",
        "EXG5",
        "EXG6",
        "EXG7",
        "EXG8",
        "A19",
        "B7",
        "B13",
        "D19",
        "D20",
        "D21",
    ],
    ["EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8", "A19", "C32", "D19", "D20", "D26"],
    ["EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8", "B27", "B28", "D31", "D32"],
    ["EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8"],
    ["EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8", "B1", "B13", "B30", "C30", "D23"],
    ["EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8", "D5"],
]
bads_ICA = [
    [0, 1, 2, 3, 6, 10, 13, 15, 19, 20],
    [0, 2, 3, 6, 7, 9, 16, 18, 20, 23, 24],
    [0, 1, 3, 4, 5, 6, 10, 12, 15, 17, 21, 22, 23, 24],
    [0, 1, 2, 3, 6, 8, 9, 10, 11, 12, 13, 16, 22, 23],
    [0, 1, 3, 4, 5, 7, 10, 11, 17, 18, 19, 21, 24],
    [0, 1, 2, 11, 15, 20, 22, 23, 24],
    [0, 4, 6, 13, 14, 16, 17, 21, 24],
    [0, 2, 3, 4, 6, 7, 15, 16, 18, 19, 20, 22, 23, 24],
]
bads_postICA = [
    [],
    ["C29"],
    ["C16", "C17", "C29", "C30", "D8", "D16"],
    ["A15", "C16", "C17", "D10", "D11", "D22"],
    ["D22"],
    [],
    [],
    [],
]

condition = "ESC6"
lowpass_cut = 1
highpass_cut = 30
raw_plot = False
filtered_plot = False
psd_plot = False
edit_marks = False
count_subs = 0
evokeds = []
bands = {"Theta (4-8 Hz)": (4, 8), "Alpha (8-12 Hz)": (8, 12)}


gAverage = grand_average(
    filepath, subjects, bads_preICA, bads_ICA, bads_postICA, condition
)
print(gAverage)
spectrum = gAverage.compute_psd()
spectrum.plot_topomap(bands=bands, show_names=False, cmap="Blues")
