#!/usr/bin/python3
'''
Example of use of the driver for SCPI devices.
'''
#######################        MANDATORY IMPORTS         #######################
import sys
import os

#######################         GENERIC IMPORTS          #######################

#######################       THIRD PARTY IMPORTS        #######################

#######################      SYSTEM ABSTRACTION IMPORTS  #######################
sys.path.append(os.getcwd()+'\\code')  #get absolute path
# from sys_abs.sys_log import sys_log_logger_get_module_logger
# if __name__ == '__main__':
#     from sys_abs.sys_log import SysLogLoggerC
#     cycler_logger = SysLogLoggerC('./sys_abs/sys_log/logginConfig.conf')
# log = sys_log_logger_get_module_logger(__name__)

#######################          PROJECT IMPORTS         #######################

#######################          MODULE IMPORTS          #######################
from drv.drv_scpi import DrvScpiHandlerC

#######################              ENUMS               #######################

#######################              CLASSES             #######################

def example():
    '''Example of the remote SCPI.
    '''
    # multimeter = DrvScpiHandlerC(port='COM4', separator='\n', baudrate = 38400)
    # print("multimeter")
    # multimeter.send_msg('VOLT:DC:NPLC 1')
    # multimeter.send_msg('FETCH?')
    # multimeter.receive_msg()
    # print(multimeter.send_and_read('FETCH?'))
    # print(multimeter.read_device_info())
    print('\n')
    source = DrvScpiHandlerC(port = 'COM5', separator = '\n', baudrate = 9600)
    print("source")
    # # source.send_msg('SYSTem:LOCK: ON')
    # # source.send_msg('SYSTem:LOCK: OFF')
    print(source.send_and_read('MEASure:VOLTage?'))
    print(source.read_device_info())


if __name__ == '__main__':
    example()
