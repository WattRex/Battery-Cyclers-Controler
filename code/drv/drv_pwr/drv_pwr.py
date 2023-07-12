#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
Driver for SCPI devices.
"""

#######################        MANDATORY IMPORTS         #######################
import sys
import os

#######################      LOGGING CONFIGURATION       #######################
# from sys_abs.sys_log import SysLogLoggerC, sys_log_logger_get_module_logger

# if __name__ == '__main__':
#     cycler_logger = SysLogLoggerC('./sys_abs/sys_log/loggingConfig.conf')
# log = sys_log_logger_get_module_logger(__name__, config_by_module_filename="./log_config.yaml")

#######################         GENERIC IMPORTS          #######################
from enum import Enum

#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################


sys.path.append(os.getcwd())  #get absolute path
#######################          PROJECT IMPORTS         #######################
from drv.drv_scpi import DrvScpiHandlerC

#######################              ENUMS               #######################
class DrvPwrStatusE(Enum):
    '''Status of the driver power.
    '''
    COMM_ERROR = -1
    OK = 0
    INTERNAL_ERROR = 1

#######################             CLASSES              #######################
class DrvPwrStatusC:
    '''Handles status of the driver power.
    '''
    def __init__(self, in_error: int, error: DrvPwrStatusE) -> None:
        self.status: DrvPwrStatusE = error
        self.__error_code: int = in_error

    def __str__(self) -> str:
        result = f"Error code: {self.__error_code} \t Status: {self.status}"
        return result
    def __eq__(self, other) -> bool:
        return self.error_code == other.error_code and self.status == other.status

    @property
    def error_code(self) -> int:
        '''The error code associated with this request .
        Args:
            - None
        Returns:
            - (int): The error code associated with this request.
        Raises:
            - None
        '''
        return self.__error_code

    @property
    def value(self) -> int:
        ''' Value of status.
        Args:
            - None
        Returns:
            - (int): Value of status.
        Raises:
            - None
        '''
        return self.status.value

    @property
    def name(self) -> str:
        ''' Name of status.
        Args:
            - None
        Returns:
            - (int): name of status.
        Raises:
            - None
        '''
        return self.status.name


class DrvPwrPropertiesC:
    '''Properties of the driver power.
    '''
    def __init__(self, model: str = None, serial_number: str = None, max_volt_limit: int = 0,
                 max_current_limit: int = 0, max_power_limit: int = 0) -> None:
        self.__model: str = model
        self.__serial_number: str = serial_number
        self.__max_volt_limit: int = max_volt_limit
        self.__max_current_limit: int = max_current_limit
        self.__max_power_limit: int = max_power_limit

class DrvPwrMeasuresC:
    '''Stores driver measurements.
    '''
    def __init__(self, voltage: int, current: int, power: int) -> None:
        self.voltage: int = voltage
        self.current: int = current
        self.power: int = power


class DrvPwrDataC(DrvPwrMeasuresC):
    '''Stores driver data.
    '''
    def __init__(self, mode, status: DrvPwrStatusC, voltage: int, current: int, power: int) -> None:
        super().__init__(voltage = voltage, current = current, power = power)
        self.mode = mode #TODO: No está seguro que hacer con el aún
        self.status: DrvPwrStatusC = status


class DrvPwrDeviceC:
    ''' Principal class.
    '''
    def __init__(self, port: str, separator: str) -> None:
        self.__device_handler: DrvScpiHandlerC  = DrvScpiHandlerC(port=port, separator=separator)
        self.__current_data: DrvPwrDataC        = None  #TODO: que hacer?
        self.__properties: DrvPwrPropertiesC    = None  #TODO: que hacer?

    @property
    def get_measures(self) -> DrvPwrMeasuresC:
        '''Get driver measurements.
        Args:
            - None
        Returns:
            - result (DrvPwrMeasuresC): Driver measurements.
        Raises:
            - None
        '''
        return self.__current_data #TODO: solo la parte de medidas

    @property
    def get_data(self) -> DrvPwrDataC:
        '''Obtain ...
        Args:
            - None
        Returns:
            - DrvPwrDataC: Return data of the driver.
        Raises:
            - None
        '''
        return self.__current_data

    @property
    def get_properties(self) -> DrvPwrPropertiesC:
        '''Obtain ...
        Args:
            - None
        Returns:
            - DrvPwrPropertiesC: Return properties of the driver.
        Raises:
            - None
        '''
        return self.__properties

    def close(self) -> None:
        '''Close the driver.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        self.__device_handler.close()
