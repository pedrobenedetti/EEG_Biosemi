# EEG_Biosemi

Author: Pedro Benedetti - Bioengineer Department, Buenos Aires' Technological Institute

pbenedetti@itba.edu.ar - @peedrobenedetti

Python files for working with Biosemi EEG device.

## mne_upload_biosemi.py

Script for processing Biosemi's EEG files.

This script works with EEG data from 128 channels. EXG1 and EXG2 are the references, placed in left and right mastoid, respectively.

<img src="https://user-images.githubusercontent.com/105320115/168087179-a85ce94e-ef8f-4d22-9a0b-5a9c3eee6789.png" width="600">

<img src="https://user-images.githubusercontent.com/105320115/168087472-e361ded0-ac94-444d-85cb-6b80152d9b6b.png" width="600">

<img src="https://user-images.githubusercontent.com/105320115/168087551-2abe4a5e-89b3-4802-80a3-1f257d191378.png" width="600">

<img src="https://user-images.githubusercontent.com/105320115/168087605-280e7b92-c6a4-47ae-ba62-e3c5d84e0257.png" width="600">

## oddball_V3.py
Protocol in which a green ball blinks blue. P300 wave is intended to be detected. Duration of stimuli and their repetition are adjustable. Sends triggers to EEG device via 'matalb_parallel_com' script.
Currently, this scripts runs with pygame version 1.9.2 (releases on Dec 2016) because Python 3.5.2 (released on Jun 2016) is installed. This is due to the laboratory computer that runs MATLAB 2016b.

<img src="https://user-images.githubusercontent.com/105320115/177829291-967dfb34-24f9-41fb-aa0b-b5f989785160.png" width="300">  <img src="https://user-images.githubusercontent.com/105320115/177829556-f9616f91-588d-451e-82d1-9a350450f82e.png" width="300">

## oddball_V4.py
Updated version of oddball protocol. There is a blinking ball that in 5 out of 6 times is green ("normal stimulus") and the other is red ("odd stimulus"). The total number stimuli is adjustable via 'N_stim' variable. Period of stimuli it is via 'period' and their duration can be changed via 'duration_stim' variable. Sends triggers to EEG device via 'matalb_parallel_com' script.
Currently, this scripts runs with pygame version 1.9.2 (releases on Dec 2016) because Python 3.5.2 (released on Jun 2016) is installed. This is due to the laboratory computer that runs MATLAB 2016b.

<img src="https://user-images.githubusercontent.com/105320115/191339775-56b0d11f-bb1e-4db6-9f40-137f399d918a.png" width="300"> <img src="https://user-images.githubusercontent.com/105320115/191339844-58ba0beb-b0ef-4cd9-97ff-dd7bf9501116.png" width="300">


## processing_OB_epochs.py
Script for uploading and analyze measures taken with oddball_V4.py. Uploads the file specified in "filepath", applies a notch filter, configures the electrode montage and references and downsamples signals to 256Hz. Detects differents events and stimuli based on "Status" channel, were the triggers are recorded. Afterwards splits the signal in epochs, taking a tmin and tmax referenced with the trigger and sets a baseline. Averages the epochs of each class ("odd" o "frequent") and polts them. If "randomize labels" is true, it will radomize the signals in each class, merging odds and frequents stimuli.

## matlab_parallel_com.py
Contains the function 'send_mark_biosemi'. When imported from another script activates a MATLAB engine. Also contains the fuction 'close_eng', which closes the MATLAB engine.

### send_mark_biosemi(mark, port)
Calls the MATLAB fuction 'send_mark_matlab'. 'mark' and 'port' are the inputs and 'nargout=0' means that there is no output argument
### close_eng()
Fuction to close the engine once the protocol has ended

## send_mark.m
Contains MATLAB fuction that sends marks to the ActiveTwo AD-box of the biosemi device.

## matlab_calling_test.py
Script designed to test the communication between MATLAB and Python.

## testing_pygame_V2.py
Description missing

# Communication between MATLAB and Python
- MATLAB R2014b or later required
- Python 3.7 or older required
  - The Pyhton enviroment must have Python 3.7 and it's path must be the first Python path in the PATH list in Enviroment Variables.
- MATLAB and Python versions must be both of 32bit or 64bit.
- If a MATLAB version that is not the latest one is installed an older version of Python might be needed.
- In MATLAB command window you must run:

```
cd (fullfile(matlabroot,'extern','engines','python'))
system('python setup.py install')
```
In 'matlab_parallel_com.py' there is an example of how MATLAB engine must be called from Python.
