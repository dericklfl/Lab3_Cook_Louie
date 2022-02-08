"""!
@file main.py
    This file contains task definitions to run motors in closed loop.
@author JR Ridgely
@date   February 7, 2022
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
from closedloop import ClosedLoop
from encoder import Encoder
from motordriver import MotorDriver
import time


# def task1_fun ():
#     """!
#     Task which puts things into a share and a queue.
#     """
#     counter = 0
#     while True:
#         share0.put (counter)
#         q0.put (counter)
#         counter += 1
# 
#         yield (0)
# 
# 
# def task2_fun ():
#     """!
#     Task which takes things out of a queue and share to display.
#     """
#     while True:
#         # Show everything currently in the queue and the value in the share
#         print ("Share: {:}, Queue: ".format (share0.get ()), end='');
#         while q0.any ():
#             print ("{:} ".format (q0.get ()), end='')
#         print ('')
# 
#         yield (0)

def task_controller():
    '''! 
    This task implements a closed loop controller for the first motor that is able to run simultaneously with other tasks
    '''
    
    ## Encoder object using pins PB6, PB7 and timer 4
    enc = Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
    
    closedloop = ClosedLoop(enc, 20000, 0.05)
    
    motor = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    
    timeelapsed = 0
    
    ## Boolean to indicate if full set of data has been printed
    printed = False
    
    while True:
        
        if input() or (share0.get() == 1):
            share0.put(1)
            starttime = time.ticks_ms()
            while timeelapsed < 2000:
                timeelapsed = time.ticks_ms() - starttime
                
                #Move the motor to set position at set gain         
                
                enc.update()
                #print("t1", enc.read())
                pwm = list(closedloop.run(enc.read()))
                motor.set_duty_cycle(pwm[0])
                #time.sleep_ms(10)

                yield (0)
                
        if not printed:
            printed = True
            closedloop.results(pwm[1], pwm[2])
            print("End")
        yield(0)
           
def task_controller2():
    '''! 
    This task implements a closed loop controller for the first motor that is able to run simultaneously with other tasks
    '''
    ## Encoder object using pins PC6, PC7 and timer 8
    enc = Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8)
    closedloop = ClosedLoop(enc, 30000, 0.05)
    motor = MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, 5)
    timeelapsed = 0
    
    ## Boolean to indicate if full set of data has been printed
    printed = False
    
    while True:
        if (share0.get() == 1):
            share0.put(1)
            starttime = time.ticks_ms()
            while timeelapsed < 2000:
                timeelapsed = time.ticks_ms() - starttime
                
                #Move the motor to set position at set gain         
            
                enc.update()
                #print("t2", enc.read())
                pwm = list(closedloop.run(enc.read()))
                motor.set_duty_cycle(pwm[0])
                yield (0)
        

        if not printed:
            printed = True
            closedloop.results(pwm[1], pwm[2])
            print("End")
        yield(0)
        
# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share ('h', thread_protect = False, name = "Share 0")
    q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
                           name = "Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (task_controller, name = 'Task_1', priority = 1, 
                          period = 10, profile = True, trace = False)
    task2 = cotask.Task (task_controller2, name = 'Task_2', priority = 1,
                          period = 10, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    #while not vcp.any ():
    #    cotask.task_list.pri_sched ()
    
    while True:
        cotask.task_list.pri_sched ()
    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')
