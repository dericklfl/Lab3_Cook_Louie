'''! @file      encoder.py
                This program includes an encoder class with functions to initialize the encoder, update the encoder reading, return the encoder reading, and zero the encoder. 
    @author     Michael Cook
    @author     Derick Louie
    @date       January 25, 2022
    @copyright  (c) 2022 by Michael Cook, Derick Louie, and released under GNU Public License v3
'''

import pyb

class Encoder:
    '''! 
    This class implements an encoder driver for an ME405 kit. 
    '''

    def __init__(self, pin1, pin2, tim):
        '''! 
        Sets up encoder by initializing GPIO pins
        @param pin1 Encoder pin 1
        @param pin2 Encoder pin 2
        @param tim Timer pin for recording encoder value
        '''
        
        ## Variable for encoder pin 1
        self.pin1 = pin1
        
        ## Variable for encoder pin 2
        self.pin2 = pin2
    
        ## Reference for pin one object
        pin_one = pyb.Pin (pin1, pyb.Pin.IN)
        
        ## Reference for pin two object
        pin_two = pyb.Pin (pin2, pyb.Pin.IN)
        
        ## Reference for timer object tim4
        self.tim4 = pyb.Timer(tim, period = 65535, prescaler = 0)
        
        ## Reference for channel 1 on timer 4
        self.t4ch1 = self.tim4.channel(1, pyb.Timer.ENC_A, pin=pin_one)
        
        ## Reference for channel 2 on timer 4
        self.t4ch2 = self.tim4.channel(2, pyb.Timer.ENC_B, pin=pin_two)
        
        ## Variable to record the previous tick value
        self.old_tick=0
        
        ## Variable for timer period
        self.per=65535
        
        ## Variable for position value
        self.position=0

        
    def update(self):
        '''!
        This method updates the timer value by adding the difference
        in encoder value to it's previous value. If the difference exceeds
        half of the period, this means the timer has overflowed. To prevent the
        value from resetting, the period is added or subtracted from the delta
        value.
        '''
        
        new_tick=self.tim4.counter()
        
        # set delta to difference in encoder value
        ## Delta variable defined by current position minus previous position
        self.delta=new_tick-self.old_tick
        self.old_tick=new_tick
        
        # if delta exceeds half period, add or subtract period to account for overflow
        if(abs(self.delta) >= self.per/2):
            if(self.delta > 0):
                self.delta -= self.per
            else:
                self.delta += self.per

        self.position += self.delta
        
    def read(self):
        '''!
        This method reads the encoder value by returning the position variable.
        @return Position variable
        '''
        
        return self.position
    
    def zero(self):
        '''!
        This method resets the encoder value by setting the position variable to 0.
        '''
        
        self.position = 0
        
    
    
if __name__ == "__main__":
    enc = Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
    enc2 = Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
    
    while True:
        enc.update()
        enc2.update()
        print('enc1:',enc.read(), 'enc2:',enc2.read())