# EEG_Biosemi

Author: Pedro Benedetti - Bioengineer Department, Buenos Aires' Technological Institute

pbenedetti@itba.edu.ar - @peedrobenedetti

Python files for working with Biosemi EEG device.

## mne_upload_biosemi

File for processing Biosemi's EEG files.

This file work with EEG data from 128 channels. EXG1 and EXG2 are the references, placed in left and right mastoid, respectively.

<img src="https://user-images.githubusercontent.com/105320115/168087179-a85ce94e-ef8f-4d22-9a0b-5a9c3eee6789.png" width="600">

<img src="https://user-images.githubusercontent.com/105320115/168087472-e361ded0-ac94-444d-85cb-6b80152d9b6b.png" width="600">

<img src="https://user-images.githubusercontent.com/105320115/168087551-2abe4a5e-89b3-4802-80a3-1f257d191378.png" width="600">

<img src="https://user-images.githubusercontent.com/105320115/168087605-280e7b92-c6a4-47ae-ba62-e3c5d84e0257.png" width="600">

## testing_pygame_V2
Description missing

## oddball_V3
Protocol in which a green ball blinks blue. P300 wave is intended to be detected. Duration of stimuli and their repetition are adjustable. Sends triggers to EEG device via 'matalb_parallel_com' script.

<img src="https://user-images.githubusercontent.com/105320115/177829291-967dfb34-24f9-41fb-aa0b-b5f989785160.png" width="300">  <img src="https://user-images.githubusercontent.com/105320115/177829556-f9616f91-588d-451e-82d1-9a350450f82e.png" width="300">



## matlab_parallel_com
Contains the function 'send_mark_biosemi'. When imported from another script activates a MATLAB engine. Also contains the fuction 'close_eng', which closes the MATLAB engine.

## send_mark.m
Contains MATLAB fuction that sends marks to the ActiveTwo AD-box of the biosemi device.
