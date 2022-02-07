'''! @file      serialplot.py
                This file runs a step response on the motor through serial when a key is pressed. It then reads and parses the data and plots time versus position.
    @author     Michael Cook
    @author     Derick Louie
    @date       January 31, 2022
    @copyright  (c) 2022 by Michael Cook, Derick Louie, and released under GNU Public License v3
'''

import serial
from matplotlib import pyplot

## List for storing times
timeList = []

## List for storing positions
posList = []

## List for storing positions in degrees
posList_deg = []

with serial.Serial ('COM8', 115200) as s_port:
    
    while True:
        if input():
            s_port.write(b'A\r')
        
        while True:
            
            if(s_port.readline() == b'End\r\n'):
                break
            
            ## List of length 2 that stores the time and position values
            data = s_port.readline().split(b',')
            
            try:
                
                ## Time converted to a string
                time_string = str(data[0], 'ascii')
                
                ## Time converted to a float
                time_float = float(time_string)
                
                ## Position converted to a string
                pos_string = str(data[1], 'ascii')
                
                ## Position converted to a float
                pos_float = float(pos_string.rstrip("\r\n"))
                
                
                timeList.append(time_float)
                posList.append(pos_float)
            
            except:
                pass
        
        print(timeList)
        print(posList)
        
        for x in posList:
            var = x/8192*360
            posList_deg.append(var)
            
        
        pyplot.plot(timeList, posList_deg)
        pyplot.ylabel("Position [degrees]")
        pyplot.xlabel("Time [ms]")
        pyplot.show()
        
