#UPDATED: 7/7/2022
import time
import logging
import datetime
import matlab.engine
#Import MATLAB engine library. 
#Pyhton 3.7 or older is needed.
global eng1 
#Declares MATLAB engine as a global variable

#Starts MATLAB engine. This is supposed to be executed when this file is imported from the protocol script.
eng1 = matlab.engine.start_matlab()
#Defines the path were the MATLAB code is saved
eng1.cd(r'C:\Users\pedro\Documents\Doctorado\Biosemi', nargout=0)

#Defines the function that sends the mark
def send_mark_biosemi(mark):
    logging.basicConfig(filename="logger_parallel.txt", level=logging.ERROR)
    try:
        #Calls the MATLAB fuction 'send_mark'. 'mark' is the input and 'nargout=0' means that there is no output argument
        eng1.send_mark(mark, nargout=0)  
        #eng1.simple_script(nargout=0)          
        
    #throws an exception in case that an error occurs.
    except:
        print("Can't connect or send data to port")
        time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        mess=(time_txt + ": Can't connect or send data to port")
        logging.error(mess)
        
#Defines the fuction to close the engine once the protocol has ended
def close_eng():
    eng1.quit()
