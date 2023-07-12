#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
Example of use of the driver for SCPI devices.
"""

#######################        MANDATORY IMPORTS         #######################
import sys
import os
sys.path.append(os.getcwd())  #get absolute path

#######################      LOGGING CONFIGURATION       #######################
from sys_abs.sys_log import SysLogLoggerC, sys_log_logger_get_module_logger

if __name__ == '__main__':
    cycler_logger = SysLogLoggerC('./sys_abs/sys_log/loggingConfig.conf')
log = sys_log_logger_get_module_logger(__name__, config_by_module_filename="./log_config.yaml")

#######################         GENERIC IMPORTS          #######################


#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################
from drv.drv_scpi import DrvScpiHandlerC

#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################

#######################              CLASSES             #######################

def example():
    '''Example of the remote SCPI.
    '''
    multimeter = DrvScpiHandlerC(port='/dev/ttyUSB0', separator='\n', baudrate = 38400)
    print("multimeter")
    # multimeter.send_msg('VOLT:DC:NPLC 1')
    # multimeter.send_msg('FETCH?')
    # multimeter.receive_msg()
    # multimeter.send_and_read('FETCH?')
    print(multimeter.read_device_info())
    print('\n')
    source = DrvScpiHandlerC(port = '/dev/ttyACM0', separator = '\n', baudrate = 9600)
    print("source")
    # source.send_msg('SYSTem:LOCK: ON')
    # source.send_msg('SYSTem:LOCK: OFF')
    # source.send_and_read('MEASure:VOLTage?')
    print(source.read_device_info())


if __name__ == '__main__':
    example()
