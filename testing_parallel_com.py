
import time
import logging
logging.basicConfig(filename="log_testing_com.txt", level=logging.DEBUG)
time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
mess=(time_txt + ": Testing marks" + "\n")
logging.debug(mess)
try:
    from parallel_com import *
    send_mark_biosemi('0xC020', 255)

    time.sleep(3)

    send_mark_biosemi('0xC020', 0)

    time.sleep(3)

    send_mark_biosemi('0xC020', 100)

    time.sleep(3)
    send_mark_biosemi('0xC020', 0)

    time.sleep(3)

    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    mess=(time_txt + "Marks sent" + "\n")
    logging.debug(mess)
    
except:
    time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    mess=(time_txt + "Weren't able to send marks" + "\n")
    logging.debug(mess)