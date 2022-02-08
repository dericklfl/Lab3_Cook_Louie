'''! @file      closedloop.py
                This program includes functions for initializing a closed loop P controller, and changing relevant parameters such as the setpoint and kP.
                This class also includes functions to run the controller and output PWM value for the motor, as well as print each position and time.
    @author     Michael Cook
    @author     Derick Louie
    @date       February 7, 2022
    @copyright  (c) 2022 by Michael Cook, Derick Louie, and released under GNU Public License v3
'''

from encoder import Encoder
import pyb
import time

class ClosedLoop:
    '''! 
    This class implements a closed loop P controller for an ME405 kit. 
    '''
    
    def __init__(self, en1, setpoint, kP):
        '''! 
        Sets up encoder by initializing GPIO pins, and creates variables
        @param setpoint Encoder setpoint, in ticks
        @param kP Gain for P controller
        '''
        
        ## Variable for setpoint of encoder
        self.setpoint = setpoint
        
        ## Variable for P controller gain
        self.kP = kP
        
        ## Reference for encoder pins
        self.encoder = en1
        
        ## List to store times
        self.times = []
        
        ## List to store positions
        self.positions = []
        
    def set_setpoint(self, setpoint):
        '''! 
        Modifies setpoint based on parameter
        @param setpoint Encoder setpoint, in ticks
        '''
        self.setpoint = setpoint
        
    def set_kP(self, kP):
        '''! 
        Modifies P controller gain based on parameter
        @param kP Gain for P controller
        '''
        self.kP = kP
        
    def run(self, encoder_val):
        '''! 
        Method which is called repeatedly to run closed loop control.
        @param encoder_val Encoder position
        @return PWM value for motor
        @return Time at which method is run
        @return Position at the time method is run
        '''
        
        self.encoder.update()
        
        ## Difference between the setpoint and encoder value
        self.error = self.setpoint - encoder_val
        
        ## PWM value for motor
        self.pwm = self.kP * self.error
        
        self.times.append(time.ticks_ms())
        self.positions.append(encoder_val)
        
        #print('error', self.error, 'pwm', self.pwm)
        
        return self.pwm, self.times, self.positions

    def results(self, timeList, posList):
        '''! 
        Method that prints each time and it's corresponding position separated by a comma.
        @param timeList List of times
        @param posList List of positions
        '''
        i = 0
        startTime = timeList[0]
        for x in timeList:
            print (str(x - startTime) + "," + str(posList[i]))
            i = i + 1
        self.times = []
        self.positions = []