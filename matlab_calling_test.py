#UPDATED 7/7/2022
from matlab_parallel_com import *
#Imports the script that initialize the MATLAB engine and defines the fuctions that send the mark and close the engine.

mark=0
#Defines the mark to be sent

send_mark_biosemi(mark)
#Calls the fuction that sends the mark via MATLAB. Defined in 'matlab_parallel_com'.

close_eng()
#Calls the fuction that closes the MATLAB engine. Defined in 'matlab_parallel_com'.
