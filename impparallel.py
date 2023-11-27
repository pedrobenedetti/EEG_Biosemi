adress = 0xCFE8
from psychopy import parallel

def send_mark_biosemi(mark, adress,debug=0):
    if debug == 0:
        import sys
        sys.path.append('D:/Pedro_Benedetti/lib')
        
        import datetime
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
    elif debug == 1:
        import datetime
        time_now = datetime.datetime.now()
        print('Sent a ' + str(mark) + ' at ' + time_now.strftime("%m/%d/%Y, %H:%M:%S"))