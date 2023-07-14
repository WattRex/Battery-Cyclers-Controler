#!/usr/bin/python3
'''
Driver of multimeter.
'''
#######################        MANDATORY IMPORTS         #######################
from __future__ import annotations
import sys
import os

#######################         GENERIC IMPORTS          #######################


#######################       THIRD PARTY IMPORTS        #######################
from enum import Enum

#######################      LOGGING CONFIGURATION       #######################
# from sys_abs.sys_log import sys_log_logger_get_module_logger
# if __name__ == '__main__':
#     from sys_abs.sys_log import SysLogLoggerC
#     cycler_logger = SysLogLoggerC('./sys_abs/sys_log/logginConfig.conf')
# log = sys_log_logger_get_module_logger(__name__)

sys.path.append(os.getcwd()+'\\code')  #get absolute path

#######################          PROJECT IMPORTS         #######################
from drv.drv_scpi import DrvScpiHandlerC
from drv.drv_pwr import *

#######################          MODULE IMPORTS          #######################


#######################              ENUMS               #######################
class DrvBkModeE(Enum):
    "Modes of the device"
    VOLT_AUTO           = 'VOLT:DC:RANGE:AUTO ON'
    VOLT_R200_MILI_V    = 'VOLT:DC:RANGE 0.2'
    VOLT_R2_V           = 'VOLT:DC:RANGE 2'
    VOLT_R20_V          = 'VOLT:DC:RANGE 20'
    VOLT_R200_V         = 'VOLT:DC:RANGE 200'
    VOLT_R1000_V        = 'VOLT:DC:RANGE 1000'
    CURR_AUTO           = 'CURR:DC:RANGE:AUTO ON'
    CURR_R2_MILI_A      = 'CURR:DC:RANGE 0.002'
    CURR_R20_MILI_A     = 'CURR:DC:RANGE 0.02'
    CURR_R200_MILI_A    = 'CURR:DC:RANGE 0.2'
    CURR_R2_A           = 'CURR:DC:RANGE 2'
    CURR_R20_A          = 'CURR:DC:RANGE 20'

class _DrvBkIntegrationRateE(Enum):
    "Integration rate of the device"
    SLOW = '10'
    MEDIUM = '1'
    FAST = '0.1'


#######################             CLASSES              #######################
class DrvBkPropertiesC(DrvPwrPropertiesC):
    ''' Properties of bk device.
    '''
    def __init__(self, model: str|None = None, serial_number: str|None = None,
                 max_volt_limit: int = 0, max_current_limit: int = 0,
                 max_power_limit: int = 0) -> None:
        super().__init__(model, serial_number, max_volt_limit, max_current_limit, max_power_limit)


class DrvBkDataC(DrvPwrDataC):
    ''' Data class of bk device.
    '''
    def __init__(self, mode: DrvBkModeE, status: DrvPwrStatusC,\
                 voltage: int, current: int, power: int) -> None:
        super().__init__(status = status, mode = mode, voltage = voltage,\
                         current = current, power = power)
        self.mode: DrvBkModeE = mode


class DrvBkDeviceC(DrvPwrDeviceC):
    ''' Principal class of bk device.
    '''
    def __init__(self, handler: DrvScpiHandlerC) -> None:
        self.device_handler: DrvScpiHandlerC
        super().__init__(handler = handler)
        self.__current_data: DrvBkDataC|None = None
        self.__properties: DrvBkPropertiesC|None = None
        self.__initialize_control()
        self.__read_device_properties()
        self.mode: DrvBkModeE = DrvBkModeE.VOLT_AUTO #TODO: Checkear con Marius. No existía el mode.


    def __initialize_control(self) -> None:
        '''Initialize the device control.
        Args:
            - None.
        Returns:    
            - None.
        Raises:
            - None.
        '''
        #Initialize device speed
        self.device_handler.send_msg('VOLT:DC:NPLC '+ _DrvBkIntegrationRateE.MEDIUM.value)
        #Initialize device mode in auto voltage
        self.device_handler.send_msg(DrvBkModeE.VOLT_AUTO.value)


    def __read_device_properties(self) -> DrvBkPropertiesC:
        '''Read the device properties .
        Args:
            - None.
        Returns:
            (DrvBkPropertiesC): Returns the device properties.
        Raises:
            - None.
        '''
        info = self.device_handler.read_device_info()
        if info is not None:
            x = 0 #TODO: hay que ver la posición en la que se encuentra el modelo y el serial en la respuesta
            model = info[x]
            serial_number = info[x+1]
        else:
            model = None
            serial_number = None
        self.__properties = DrvBkPropertiesC(model = model, serial_number = serial_number)
        return self.__properties #TODO ¿retornar propiedades si se guardan en un self?

    def set_mode(self, meas_mode: DrvBkModeE) -> None:
        '''Set the device mode.
        Args:
            - meas_mode (DrvBkModeE): Mode to set.
        Returns:
            - None.
        Raises:
            - None.
        '''
        mode_cod = meas_mode.value.split(':')[0]+':' + meas_mode.value.split(':')[1]
        #Change mode to voltage or current
        self.device_handler.send_msg('FUNC '+ mode_cod)
        #Change range of the mode
        self.device_handler.send_msg(meas_mode.value)
        self.mode = meas_mode

    def get_data(self) -> DrvBkDataC:
        #TODO: Se podría medir el voltaje y la corriente pero uno de los dos dará 0.
        #TODO: La potencia en un multímetro no se puede medir.
        '''Read the device measures.
        Args:
            - None.
        Returns:
            - (DrvBkDataC): Returns the device measures.
        Raises:
            - None
        '''
        current = 0
        voltage = 0
        #Read measure
        response = self.device_handler.send_and_read('FETC?')
        if response is not None:
            response = int(response[1])
            if self.mode.value.split(':')[0] == 'VOLT':
                voltage = response
            elif self.mode.value.split(':')[0] == 'CURR':
                current = response
            status = DrvPwrStatusC(DrvPwrStatusE.OK)
        else:
            status = DrvPwrStatusC(DrvPwrStatusE.COMM_ERROR)
        self.__current_data = DrvBkDataC(mode = self.mode, status = status,\
                                        voltage = voltage, current = current, power = 0)
        return self.__current_data

    def get_properties(self) -> DrvBkPropertiesC:
        '''Read the device properties.
        Args:
            - None.
        Returns:
            - (DrvBkPropertiesC): Returns the device properties.
        Raises:
            - None.
        '''
        return self.__read_device_properties()


    def close(self) -> None:
        '''Close communication with the device.
        Args:
            - None.
        Returns:
            - None.
        Raises:
            - None.
        '''
        self.device_handler.close()
