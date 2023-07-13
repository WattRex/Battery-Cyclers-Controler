#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
Driver for power devices.
"""

#######################        MANDATORY IMPORTS         #######################
from __future__ import annotations
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


#######################          PROJECT IMPORTS         #######################
from drv.drv_scpi import DrvScpiHandlerC

sys.path.append(os.getcwd())  #get absolute path
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
    def __init__(self, error: int|DrvPwrStatusE) -> None:
        if isinstance(error, DrvPwrStatusE):
            self.status = error
            self.__error_code = error.value
        else:
            self.__error_code = error
            if error > 0:
                self.status = DrvPwrStatusE.INTERNAL_ERROR
            else:
                self.status = DrvPwrStatusE(error)

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
    def __init__(self, model: str|None = None, serial_number: str|None = None,\
                 max_volt_limit: int = 0, max_current_limit: int = 0,\
                 max_power_limit: int = 0) -> None:
        self.model: str|None = model
        self.serial_number: str|None = serial_number
        self.max_volt_limit: int = max_volt_limit
        self.max_current_limit: int = max_current_limit
        self.max_power_limit: int = max_power_limit


class DrvPwrDataC:
    '''Device data storage.
    '''
    def __init__(self,  status: DrvPwrStatusC, mode: Enum, voltage: int,
                 current: int, power: int) -> None:
        self.status: DrvPwrStatusC = status
        self.mode: Enum = mode
        self.voltage: int = voltage
        self.current: int = current
        self.power: int = power


class DrvPwrDeviceC:
    '''Representation of power devices.
    '''
    def __init__(self, handler: DrvScpiHandlerC) -> None:
        self.__device_handler: DrvScpiHandlerC  = handler
        self.__current_data: DrvPwrDataC|None        = None
        self.__properties: DrvPwrPropertiesC|None   = None


    def get_data(self) -> DrvPwrDataC|None:
        '''Obtain ...
        Args:
            - None
        Returns:
            - DrvPwrDataC: Return data of the driver.
        Raises:
            - None
        '''
        return self.__current_data


    def get_properties(self) -> DrvPwrPropertiesC|None:
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
