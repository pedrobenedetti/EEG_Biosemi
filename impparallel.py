import sys
sys.path.append('C:/Users/pedro/src')
from psychopy import parallel

adress = 0xC020

parallel.setPortAddress(adress)
parallel.setData(20)
