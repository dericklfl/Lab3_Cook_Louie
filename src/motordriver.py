'''! @file      motordriver.py
                This program includes a MotorDriver class with functions to initialize the correct pins to control the motor along with setting the duty cycle.
    @author     Michael Cook
    @author     Derick Louie
    @date       January 25, 2022
    @copyright  (c) 2022 by Michael Cook, Derick Louie, and released under GNU Public License v3
'''

import pyb

class MotorDriver:
    '''! 
    This class implements a motor driver for an ME405 kit. 
    '''

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        '''! 
        Creates a motor driver by initializing GPIO
        pins and turning the motor off for safety. 
        @param en_pin EN pin associated with L6206 motor driver
        @param in1pin IN1 pin associated with L6026 motor driver
        @param in2pin IN2 pin associated with l6026 motor driver
        @param timer Timer pin for PWM
        '''
        
        ## Reference for pin object for A10
        self.pinPA10 = pyb.Pin (en_pin, pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
        
        ## Reference for pin object for B4
        self.pinPB4 = pyb.Pin (in1pin, pyb.Pin.OUT_PP)
        
        ## Reference for pin object for B5
        self.pinPB5 = pyb.Pin (in2pin, pyb.Pin.OUT_PP)
        
        ## Reference for timer object tim3
        self.tim3 = pyb.Timer(timer, freq=20000)
        
        ## Reference for timer 3 channel 1
        self.IN1 = self.tim3.channel(1, pyb.Timer.PWM, pin=self.pinPB4)
        
        ## Reference for timer 3 channel 2
        self.IN2 = self.tim3.channel(2, pyb.Timer.PWM, pin=self.pinPB5)
        
        # disables motor
        self.pinPA10.low()
        
        #print ('Creating a motor driver')

    def set_duty_cycle (self, level):
        '''!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        '''
        
        # enables motor
        self.pinPA10.high()
        
        # changes direction of motor depending on if level is positive or negative
        if (level > 0):
            
            self.IN2.pulse_width_percent(0)
            self.IN1.pulse_width_percent(abs(level))
        elif (level < 0):
            self.IN2.pulse_width_percent(abs(level))
            self.IN1.pulse_width_percent(0)
            
        #print ('Setting duty cycle to ' + str (level))



if __name__ == "__main__":
    driver = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    driver.set_duty_cycle(0)



