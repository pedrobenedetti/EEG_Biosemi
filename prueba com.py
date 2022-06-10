from parallel_com import *
import time
import logging

logging.basicConfig(filename="log.txt", level=logging.DEBUG)
time_txt=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
mess=(time_txt + ": Prueba de envio de marcas" + "\n")
logging.debug(mess)

send_mark_biosemi('COM5', 255)

time.sleep(3)

send_mark_biosemi('COM5', 0)

time.sleep(3)

send_mark_biosemi('COM5', 100)

time.sleep(3)
send_mark_biosemi('COM5', 0)

time.sleep(3)