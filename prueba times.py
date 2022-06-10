import time
import datetime

time1=datetime.datetime.now()
time.sleep(2)
time2=datetime.datetime.now()
timeR=(time2-time1).total_seconds()
print(timeR)
