#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
Example of use of the driver for SCPI devices.
"""

#######################        MANDATORY IMPORTS         #######################
import sys, os
sys.path.append(os.getcwd())  #get absolute path

#######################      LOGGING CONFIGURATION       #######################
from SYS.SYS_LOG import SYS_LOG_Logger_c, SYS_LOG_LoggerGetModuleLogger

if __name__ == '__main__':
    cycler_logger = SYS_LOG_Logger_c('./SYS/SYS_LOG/logginConfig.conf')
log = SYS_LOG_LoggerGetModuleLogger(__name__, config_by_module_filename="./log_config.yaml")

#######################         GENERIC IMPORTS          #######################
from consolemenu import Screen

#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################
from DRV.DRV_SCPI import DRV_SCPI_Handler_c

#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################

#######################              CLASSES             #######################

def main():
    Screen.clear() #TODO: quitarlo de aqui y del import

    multimeter = DRV_SCPI_Handler_c(port='/dev/ttyUSB0', separator='\n', baudrate = 38400)
    print(f"multimeter")
    # multimeter.sendMsg('VOLT:DC:NPLC 1')
    # multimeter.sendMsg('FETCH?')
    # multimeter.receiveMsg()
    # multimeter.sendAndRead('FETCH?')
    print(multimeter.readDeviceInfo())
    print('\n')
    
    
    source = DRV_SCPI_Handler_c(port = '/dev/ttyACM0', separator = '\n', baudrate = 9600)
    print(f"source")
    # source.sendMsg('SYSTem:LOCK: ON')
    # time.sleep(3)
    # source.sendMsg('SYSTem:LOCK: OFF')
    # source.sendAndRead('MEASure:VOLTage?')
    print(source.readDeviceInfo())


if __name__ == '__main__':
    main()


########## DICCIONARIO COMANDOS ##########
'''
MULTIMETRO
- Ponerlo a valor medio: 'VOLT:DC:NPLC 1'
- Ponerlo a valor slow: 'VOLT:DC:NPLC 10'
- Ponerlo a valor fast: 'VOLT:DC:NPLC 0.1'

FUENTE
- LOCK ON:  'SYSTem:LOCK: ON'
- LOCK OFF: 'SYSTem:LOCK: OFF'
- MEDIR voltaje: 'MEASure:VOLTage?'
- MEDIR corriente: 'MEASure:CURRent?'
'''
