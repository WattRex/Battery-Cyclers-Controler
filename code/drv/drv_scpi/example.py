#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
Example of use of the driver for SCPI devices.
"""

#######################        MANDATORY IMPORTS         #######################
import sys, os
sys.path.append(os.getcwd())  #get absolute path

#######################      LOGGING CONFIGURATION       #######################
from sys.sys_log import SYS_LOG_Logger_c, SYS_LOG_LoggerGetModuleLogger

if __name__ == '__main__':
    cycler_logger = SYS_LOG_Logger_c('./sys/sys_log/logginConfig.conf')
log = SYS_LOG_LoggerGetModuleLogger(__name__, config_by_module_filename="./log_config.yaml")

#######################         GENERIC IMPORTS          #######################


#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################
from drv.drv_scpi import DrvScpiHandlerC, DrvScpiErrorC

#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################

#######################              CLASSES             #######################

def main():
    multimeter = DrvScpiHandlerC(port='/dev/ttyUSB0', separator='\n', baudrate = 38400)
    print(f"multimeter")
    # multimeter.send_msg('VOLT:DC:NPLC 1')
    # multimeter.send_msg('FETCH?')
    # multimeter.receive_msg()
    # multimeter.send_and_read('FETCH?')
    print(multimeter.read_device_info())
    print('\n')
    
    
    source = DrvScpiHandlerC(port = '/dev/ttyACM0', separator = '\n', baudrate = 9600)
    print(f"source")
    # source.send_msg('SYSTem:LOCK: ON')
    # source.send_msg('SYSTem:LOCK: OFF')
    # source.send_and_read('MEASure:VOLTage?')
    print(source.read_device_info())


if __name__ == '__main__':
    main()


########## EXAMPLE COMMAND DICTIONARY ##########
'''
MULTIMETER
- Send medium value: 'VOLT:DC:NPLC 1'
- Send slow value: 'VOLT:DC:NPLC 10'
- Send fast value: 'VOLT:DC:NPLC 0.1'

SOURCE
- LOCK ON:  'SYSTem:LOCK: ON'
- LOCK OFF: 'SYSTem:LOCK: OFF'
- Voltaje measure: 'MEASure:VOLTage?'
- Corriente measure: 'MEASure:CURRent?'
'''
