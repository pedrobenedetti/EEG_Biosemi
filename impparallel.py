import sys
sys.path.append('D:/Pedro_Benedetti/lib')
from psychopy import parallel
import datetime



adress = 0xCFE8

def send_mark_biosemi(mark, adress):
    parallel.setPortAddress(adress)

    time_start = datetime.datetime.now()
    time_now = datetime.datetime.now()

    while True:
        parallel.setData(mark)
        time_now = datetime.datetime.now()
        print('B')
        if (time_now - time_start).total_seconds() > 0.0015:
            print((time_now - time_start).total_seconds())
            parallel.setData(0)
            break
