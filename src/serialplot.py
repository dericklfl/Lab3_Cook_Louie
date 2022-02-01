import serial
from matplotlib import pyplot

timeList = []
posList = []
posList_deg = []

with serial.Serial ('COM7', 115200) as s_port:
        
    while True:
        print(s_port.readline())
        if(s_port.readline() == b'End\r\n'):
            print("break")
            break
        
        
        data = s_port.readline().split(b',')
        
        try:
            time_string = str(data[0], 'ascii')
            time_float = float(time_string)
            
            pos_string = str(data[1], 'ascii')
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
        
    s_port.write(b'Stop\n\r')
        
    pyplot.plot(timeList, posList_deg)
    pyplot.ylabel("Position [degrees]")
    pyplot.xlabel("Time [ms]")
    pyplot.show()
    
    
