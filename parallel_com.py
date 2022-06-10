import time
import logging
import datetime
import parallel

def send_mark_biosemi(port, mark):
    logging.basicConfig(filename="log.txt", level=logging.ERROR)
    try:
        pport = parallel.ParallelPort(address=port)
        #Connection with the serial port
        #Here Biosemi provides information about the communication https://www.biosemi.com/faq/USB%20Trigger%20interface%20cable.htm
        try:
            #we send the mark the times, each separated by 0.1 seconds
            pport.setData(mark)
            time.sleep(0.1)
            pport.setData(mark)
            time.sleep(0.1)
            pport.setData(mark)
            #we close the communication
            
        except:
            print("Can't send data to ", port, " port")
            time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            mess=(time_txt + ": Can't send data to " + port + " port")
            logging.error(mess)
            
    except:
        time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        mess=(time_txt+ ": Can't connect to "+ port+ " port")
        logging.error(mess)
