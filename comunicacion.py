import serial
import time

def send_mark_biosemi(port,mark):

    serb = serial.Serial(port=port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None)
    #Connection with the serial port
    #Here Biosemi provides information about the communication https://www.biosemi.com/faq/USB%20Trigger%20interface%20cable.htm

    #we send the mark the times, each separated by 0.1 seconds
    serb.write(str(mark))
    time.sleep(0.1)
    serb.write(bstr(mark))
    time.sleep(0.1)
    serb.write(str(mark))
    
    #we close the communication
    serb.close

