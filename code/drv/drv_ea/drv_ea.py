#!/usr/bin/python3
'''
Driver of ea power supply.
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
class DrvEaModeE(Enum):
    "Modes of the device"
    WAIT = 0
    CV_MODE = 1
    CC_MODE = 2

#######################             CLASSES              #######################
class DrvEaPropertiesC(DrvPwrPropertiesC):
    ''' Properties of ea power supply device.
    '''
    def __init__(self, model: str|None = None, serial_number: str|None = None,
                 max_volt_limit: int = 0, max_current_limit: int = 0,
                 max_power_limit: int = 0) -> None:
        super().__init__(model, serial_number, max_volt_limit, max_current_limit, max_power_limit)


class DrvEaDataC(DrvPwrDataC):
    ''' Data class of ea power supply device.
    '''
    def __init__(self, mode: DrvEaModeE, status: DrvPwrStatusC,\
                 voltage: int, current: int, power: int) -> None:
        super().__init__(status = status, mode = mode, voltage = voltage,\
                         current = current, power = power)
        self.mode: DrvEaModeE = mode


class DrvEaDeviceC(DrvPwrDeviceC):
    '''Principal class of ea power supply device.
    '''
    def __init__(self, handler: DrvScpiHandlerC) -> None:
        self.device_handler: DrvScpiHandlerC
        super().__init__(handler)
        self.__current_data: DrvEaDataC|None = None
        self.__properties: DrvEaPropertiesC|None = None
        self.__initialize_control()
        self.__read_device_properties()
        self.mode: DrvEaModeE = DrvEaModeE.WAIT #TODO: checkear con marius, no existe en la documentación

    def __read_device_properties(self) -> DrvEaPropertiesC:
        '''Read the device properties.
        Args:
            - None.
        Returns:
            - (DrvEaPropertiesC): Returns the device properties.
        Raises:
            - None.
        '''
        model: str|None = None
        serial_number: str|None = None
        max_current_limit: int = 0
        max_voltage_limit: int = 0
        max_power_limit: int = 0
        #Model and serial number
        info = self.device_handler.read_device_info()
        if info is not None:
            model = info[1]
            serial_number = info[2]
        #Max current limit
        read_curr = self.device_handler.send_and_read('SYSTem:NOMinal:CURRent?')
        if read_curr is not None:
            max_current_limit = int(read_curr[0])
        #Max voltage limit
        read_volt = self.device_handler.send_and_read('SYSTem:NOMinal:VOLTage?')
        if read_volt is not None:
            max_voltage_limit = int(read_volt[0])
        #Max power limit
        read_power = self.device_handler.send_and_read('SYSTem:NOMinal:POWer?')
        if read_power is not None:
            max_power_limit = int(read_power[0])

        self.__properties = DrvEaPropertiesC(model = model, serial_number = serial_number, \
                                            max_volt_limit = max_voltage_limit, \
                                            max_current_limit = max_current_limit, \
                                            max_power_limit = max_power_limit)
        return self.__properties


    def __initialize_control(self) -> None:
        ''' Enable remote control and turn it off.
        Args:
            - None.
        Returns:
            - None.
        Raises:
            - None.
        '''
        self.device_handler.send_msg('SYSTem:LOCK: ON')
        self.device_handler.send_msg('OUTPut: OFF')


    def set_wait_mode(self) -> None:
        #TODO: ¿¿¿¿????
        pass


    def set_cc_mode(self, curr_ref: int, voltage_limit: int) -> None:
        '''
        Use source in constant current mode.
        Sink mode will be set with negative current values.
        Security voltage limit can be also set.
        Args:
            - curr_ref (int): current consign (milli Amps)    #TODO: checkear unidades
            - voltage_limit (int): voltage limit (millivolts) #TODO: checkear unidades
        Returns:
            - None
        Raises:
            - None
        '''
        current = round(float(curr_ref)/1000, 2)
        voltage = round(float(voltage_limit/1000), 2)
        if self.__properties is not None:
            max_power_limit = self.__properties.max_power_limit/1000 #TODO: Checkear unidades
            #Check if the power limit is exceeded
            if current * voltage > max_power_limit:
                voltage = max_power_limit / curr_ref

        self.device_handler.send_msg(f"CURRent {current}")
        self.device_handler.send_msg(f"VOLTage {voltage}")
        self.mode = DrvEaModeE.CC_MODE

    def set_cv_mode(self, volt_ref: int, current_limit: int) -> None:
        '''
        Use source in constant voltage mode .
        Security current limit can be also set for both sink and source modes. 
        It is recommended to set both!
        Args:
            - volt_ref (int): voltage consign (millivolts)      #TODO: checkear unidades
            - current_limit (int): current limit (milli Amps)   #TODO: checkear unidades
        Returns:
            - None
        Raises:
            - None
        '''
        voltage = round(float(volt_ref)/1000, 2)
        current = round(float(current_limit/1000), 2)
        if self.__properties is not None:
            max_power_limit = self.__properties.max_power_limit/1000 #TODO: Checkear unidades
            #Check if the power limit is exceeded
            if voltage * current > max_power_limit:
                current = max_power_limit / volt_ref

        self.device_handler.send_msg(f"VOLTage {voltage}")
        self.device_handler.send_msg(f"CURRent {current}")
        self.mode = DrvEaModeE.CV_MODE


    def get_data(self) -> DrvEaDataC:
        '''Read the device data.
        Args:
            - None.
        Returns:
            - (DrvEaDataC): Returns the device data.
        Raises:
            - None.
        '''
        current = 0
        voltage = 0
        power = 0
        status = DrvPwrStatusC(DrvPwrStatusE.OK)

        #TODO: checkear si se puede leer todo de una vez y posiciones
        read_all = self.device_handler.send_and_read('MEASure:ARRay?')
        if read_all is not None:
            current = int(read_all[0])
            voltage = int(read_all[1])
            power = int(read_all[2])
        else:
            status = DrvPwrStatusC(DrvPwrStatusE.COMM_ERROR)
        #Read current
        read_current = self.device_handler.send_and_read('MEASure:CURRent?')
        if read_current is not None:
            current = int(read_current[0])
        else:
            status = DrvPwrStatusC(DrvPwrStatusE.COMM_ERROR)
        #Read voltage
        read_voltage = self.device_handler.send_and_read('MEASure:VOLTage?')
        if read_voltage is not None:
            voltage = int(read_voltage[0])
        else:
            status = DrvPwrStatusC(DrvPwrStatusE.COMM_ERROR)
        #Read power
        read_power = self.device_handler.send_and_read('MEASure:POWer?')
        if read_power is not None:
            power = int(read_power[0])
        else:
            status = DrvPwrStatusC(DrvPwrStatusE.COMM_ERROR)

        self.__current_data = DrvEaDataC(mode = self.mode, status = status, \
                                        voltage = voltage, current = current, power = power)
        return self.__current_data


    def get_properties(self) -> DrvEaPropertiesC:
        '''Read the device properties.
        Args:
            - None.
        Returns:
            - (DrvEaPropertiesC): Returns the device properties.
        Raises:
            - None.
        '''
        return self.__read_device_properties()


    def close(self) -> None:
        '''Close communication with the device.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        self.device_handler.close()


    def set_out_put(self, output:bool) -> None:
        #TODO: Checkear con marius, no existe en la documentación.
        '''
        Activates the source output with True or 'ON'
        Deactivates the source output with 0 or 'OFF'
        Args:
            - output (bool): Activate or deactivate the output of device.
        Returns:
            - None
        Raises:
            - None
        '''
        if output:
            self.device_handler.send_msg('OUTPut ON')
        else:
            self.device_handler.send_msg('OUTPut OFF')




############## DRV SCPI CHECKEAR OTRA VEZ ##############################
def _getOnlyNumbers(inputString:str):
    '''
    Returns only numeric values from an original string.

    :param inputString: string used to match numbers patterns
    :type inputString: str
    :return: list of numbers
    :rtype: list
    '''    
    
    numericString = re.findall('-?\d*\.?\d+',inputString)
    return numericString

def _getResponseSplit(device:serial, separator:str):
    '''
    Receives the serial response from the device and splits it with the given 
    separator.

    :param device: serial device used to receive response
    :type device: serial
    :param separator: string separator used to split the repsonse
    :type separator: str
    :return: strings received from device
    :rtype: list
    '''
    return (str(device.readline().decode("utf-8")).split(separator))

def _getResponseNumbers(device:serial):
    '''
    Receives the serial response from the device and splits it selecting only 
    the numeric values. Returned values are converted to the numerical system 
    used by applying the scaling factor.

    :param device: serial device used to receive response
    :type device: serial
    :return: list of numbers received from device
    :rtype: List[int]
    '''
    listOfNumbers = _getOnlyNumbers(device.readline().decode("utf-8"))
    listOfNumbers = [int(float(i)*_Constants_c.SCALING_FACTOR) for i in listOfNumbers]
    if len(listOfNumbers) == 1: 
        listOfNumbers = listOfNumbers[0]
    return listOfNumbers
