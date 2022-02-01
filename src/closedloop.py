import encoder
import pyb
import time

class ClosedLoop:
    
    def __init__(self, setpoint, kP):
        
        self.setpoint = setpoint
        self.kP = kP
        self.encoder = encoder.Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
        self.times = []
        self.positions = []
        
    def set_setpoint(self, setpoint):
        
        self.setpoint = setpoint
        
    def set_kP(self, kP):
        
        self.kP = kP
        
    def run(self, encoder_val):
        
        
        self.encoder.update()
        error = self.setpoint - encoder_val
        
        pwm = self.kP * error
        
        self.times.append(time.ticks_ms())
        self.positions.append(encoder_val)
        
        #print('error', error, 'pwm', pwm)
        
        return pwm, self.times, self.positions

    def results(self, timeList, posList):
        i = 0
        startTime = timeList[0]
        for x in timeList:
            print (str(x - startTime) + "," + str(posList[i]))
            i = i + 1
        self.times = []
        self.positions = []