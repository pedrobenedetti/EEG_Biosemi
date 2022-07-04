import time
import logging
import datetime
import matlab.engine
global eng1

eng1 = matlab.engine.start_matlab()
eng1.cd(r'C:\Users\pedro\Documents\Doctorado\Biosemi', nargout=0)

    
def send_mark_biosemi(marca):
    logging.basicConfig(filename="logger_parallel.txt", level=logging.ERROR)
    try:
        eng1.send_mark(0)  
        #eng1.simple_script(nargout=0)          
    except:
        print("Can't connect or send data to port")
        time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        mess=(time_txt + ": Can't connect or send data to port")
        logging.error(mess)

def close_eng():
    eng1.quit()
