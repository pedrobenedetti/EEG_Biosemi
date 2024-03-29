# EEG_Biosemi

Author: Pedro Benedetti - PhD Candidate - Bioengineer Department, Buenos Aires' Technological Institute

pbenedetti@itba.edu.ar - @peedrobenedetti

Python files for working with Biosemi EEG device.

## AUT_and_REY.py 
Script designed to make the AUT and REY figure task test. In v3 version includes a Resting at the beginning and another at the end. It also has a minute to think before AUT and REY task. The marks send to the EEG are the following: 

- RESTING-------------02 
- PART 1 TITLE--------10 
- INST. AUT-----------20 
- THINK AUT-----------30 
- AUT-----------------45     
- PART 2 TITLE--------50 
- INST REY------------60 
- THINK REY-----------70 
- REY-----------------85 
- THANKS--------------90 
- RESTING-------------100        
- SAVING/END----------110 

## processing_AUTREY_v3
Process data from AUT_and_REY.py. Computes PSD and plot it for Theta and Alpha bands.

## processing_AUTREY_GA.py
Same that previous but for a Gran Average across participants.

## arrays_AUTREY_v3.py
Generates arrays with the PSD of Theta and Alpha bands' PSD. They are separated for the diverse stages of the study and saved on an excel file.

## mne_upload_biosemi.py

Script for processing Biosemi's EEG files.

This script works with EEG data from 128 channels. EXG1 and EXG2 are the references, placed in left and right mastoid, respectively.

<img src="https://user-images.githubusercontent.com/105320115/168087179-a85ce94e-ef8f-4d22-9a0b-5a9c3eee6789.png" width="500"> <img src="https://user-images.githubusercontent.com/105320115/168087472-e361ded0-ac94-444d-85cb-6b80152d9b6b.png" width="500">

<img src="https://user-images.githubusercontent.com/105320115/168087551-2abe4a5e-89b3-4802-80a3-1f257d191378.png" width="500">

<img src="https://user-images.githubusercontent.com/105320115/191343740-e9c4cce4-21a8-4820-b380-f978770d2c61.png" width="500"><img src="https://user-images.githubusercontent.com/105320115/168087605-280e7b92-c6a4-47ae-ba62-e3c5d84e0257.png" width="500">

## oddball_V3.py
Protocol in which a green ball blinks blue. P300 wave is intended to be detected. Duration of stimuli and their repetition are adjustable. Sends triggers to EEG device via 'matalb_parallel_com' script.
Currently, this scripts runs with pygame version 1.9.2 (releases on Dec 2016) because Python 3.5.2 (released on Jun 2016) is installed. This is due to the laboratory computer wich runs MATLAB 2016b.

<img src="https://user-images.githubusercontent.com/105320115/177829291-967dfb34-24f9-41fb-aa0b-b5f989785160.png" width="300">  <img src="https://user-images.githubusercontent.com/105320115/177829556-f9616f91-588d-451e-82d1-9a350450f82e.png" width="300">

## oddball_V4.py
Updated version of oddball protocol. There is a blinking ball that in 5 out of 6 times is green ("standard stimulus") and the other is red ("rare target stimulus"). The total number stimuli is adjustable via 'N_stim' variable. Period of stimuli it is via 'period' and their duration can be changed via 'duration_stim' variable. Sends triggers to EEG device via 'matalb_parallel_com' script.
Currently, this scripts runs with pygame version 1.9.2 (releases on Dec 2016) because Python 3.5.2 (released on Jun 2016) is installed. This is due to the laboratory computer wich runs MATLAB 2016b.

<img src="https://user-images.githubusercontent.com/105320115/191339775-56b0d11f-bb1e-4db6-9f40-137f399d918a.png" width="300"> <img src="https://user-images.githubusercontent.com/105320115/191339844-58ba0beb-b0ef-4cd9-97ff-dd7bf9501116.png" width="300">

## oddball_V5.py
Same as oddball_V4.py but user hast to press the right button each time he sees a red ball (target). It also has a fixed number (20) of rare target stimuli instead a fixed total stimuli.

## processing_OB_epochs.py
Script for uploading and analyze measures taken with oddball_V4.py. Uploads the file specified in "filepath", applies a notch filter, configures the electrode montage and references and downsamples signals to 256Hz. Detects differents events and stimuli based on "Status" channel, were the triggers are recorded. Afterwards splits the signal in epochs, taking a tmin and tmax referenced with the trigger and sets a baseline. Averages the epochs of each class ("rare target" or "stardard") and polts them. If "randomize labels" is true, it will radomize the signals in each class, merging rares and stardards stimuli.

<img src="https://user-images.githubusercontent.com/105320115/191342438-9a0229e9-e7d3-4e7a-9a3e-42346510412e.png" width="500" > <img src="https://user-images.githubusercontent.com/105320115/191342493-9a3623c6-0724-49ac-ac55-a5b90160b15e.png" width="500" >

<img src="https://user-images.githubusercontent.com/105320115/191341361-3c94354c-a00b-4a63-b084-c69e68de6a94.png" width="1000">


## matlab_parallel_com.py
Contains the function 'send_mark_biosemi'. When imported from another script activates a MATLAB engine. Also contains the fuction 'close_eng', which closes the MATLAB engine.

### send_mark_biosemi(mark, port)
Calls the MATLAB fuction 'send_mark_matlab'. 'mark' and 'port' are the inputs and 'nargout=0' means that there is no output argument
### close_eng()
Fuction to close the engine once the protocol has ended

## send_mark.m
Contains MATLAB fuction that sends marks to the ActiveTwo AD-box of the biosemi device.



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
