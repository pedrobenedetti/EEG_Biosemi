import serial
import time
import logging
import datetime

def send_mark_biosemi(port, mark):
    logging.basicConfig(filename="log.txt", level=logging.ERROR)
    try:
        serb = serial.Serial(port=port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None)
        #Connection with the serial port
        #Here Biosemi provides information about the communication https://www.biosemi.com/faq/USB%20Trigger%20interface%20cable.htm
        try:
            #we send the mark the times, each separated by 0.1 seconds
            serb.write(str(mark))
            time.sleep(0.1)
            serb.write(str(mark))
            time.sleep(0.1)
            serb.write(str(mark))
            #we close the communication
            serb.close
        except:
            print("Can't send data to ", port, " port")
            time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            mess=(time_txt + ": Can't send data to " + port + " port")
            logging.error(mess)
            serb.close
    except:
        time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        mess=(time_txt+ ": Can't connect to "+ port+ " port")
        logging.error(mess)
