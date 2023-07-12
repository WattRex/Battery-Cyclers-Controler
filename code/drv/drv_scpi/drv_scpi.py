#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
Driver for SCPI devices.
"""

#######################        MANDATORY IMPORTS         #######################
import sys
import os
sys.path.append(os.getcwd())  #get absolute path

#######################      LOGGING CONFIGURATION       #######################
from sys_abs.sys_log import SYS_LOG_Logger_c, SYS_LOG_LoggerGetModuleLogger

if __name__ == '__main__':
    cycler_logger = SYS_LOG_Logger_c('./sys_abs/SysLogLoggerC/logginConfig.conf')
log = sys_log_logger_get_module_logger(__name__, config_by_module_filename="./log_config.yaml")

#######################         GENERIC IMPORTS          #######################
from typing import List
import serial

#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################


#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################
class _DefaultSerialParamsC:
    "Communication constants"
    _BAUD_RATE           = 115200
    _BYTESIZE            = serial.EIGHTBITS
    _PARITY              = serial.PARITY_NONE
    _STOP_BITS           = serial.STOPBITS_ONE
    _READ_TIMEOUT        = 0.5
    _WRITE_TIMEOUT       = 0.5
    _INTER_BYTE_TIMEOUT  = 0.5
    _MAX_LEN_IN_BYTES    = 21

#######################             CLASSES              #######################
class DrvScpiErrorC:
    '''Error class for SCPI driver.
    '''
    def __init__(self, message: str, error_code: int) -> None:
        self.message    = message
        self.error_code  = error_code

    def __str__(self) -> str:
        return f"Error: {self.message} \t Code: {self.error_code}"


class DrvScpiHandlerC:
    '''Driver for SCPI devices.
    '''
    def __init__(self, port: str, separator: str, baudrate: int = _DefaultSerialParamsC._BAUD_RATE,
                 bytesize = _DefaultSerialParamsC._BYTESIZE,
                 parity = _DefaultSerialParamsC._PARITY,
                 stopbits = _DefaultSerialParamsC._STOP_BITS,
                 timeout = _DefaultSerialParamsC._READ_TIMEOUT,
                 write_timeout = _DefaultSerialParamsC. _WRITE_TIMEOUT,
                 inter_byte_timeout = _DefaultSerialParamsC._INTER_BYTE_TIMEOUT) -> None:
        self.__serial: serial.Serial = serial.Serial(port = port,
                                                     baudrate = baudrate,
                                                     bytesize = bytesize,
                                                     parity = parity, 
                                                     topbits = stopbits,
                                                     timeout = timeout,
                                                     write_timeout = write_timeout,
                                                     inter_byte_timeout = inter_byte_timeout)
        self.__separator: str = separator


    def decode_numbers(self, data: bytes) -> List[float]:
        '''Decode bytes to integers.
        Args:
            - data (bytes): Value to decode
        Returns:
            - msg_decode (List[int]): Message decoded.
        Raises:
            - DrvScpiErrorC: Error decoding data.
        '''
        data = data.decode('utf-8')
        msg_decode = data.split(f"{self.__separator}")
        try:
            msg_decode = [float(i) for i in msg_decode]
        except ValueError as exc:
            result = DrvScpiErrorC(message = "Error decoding data", error_code = 2)
            raise ValueError(result) from exc
        return msg_decode


    def decode_and_split(self, data: bytes) -> List[str]:
        '''Decode str to integers and split the data.
        Args:
            data (bytes): Value to decode and split.
        Returns:
            msg_decode (List[str]): Message decoded and splited.
        Raises:
            - None
        '''
        data = data.decode('utf-8')
        msg_decode = data.split(f"{self.__separator}")
        return msg_decode


    def read_device_info(self) -> List[str]:
        '''Reads the list of device information.
        Args:
            - None
        Returns:
            - msg (List[str]): List of device information.
        Raises:
            - DrvScpiErrorC: Error decoding data.
        '''
        msg = self.send_and_read('*IDN?')
        if len(msg) == 0:
            result = DrvScpiErrorC(message = "Error reading device information", error_code = 1)
            raise ValueError(result)
        else:
            return msg


    def send_msg(self, msg:str) -> None:
        '''Send a message to the serial device.
        Args:
            - msg (str): Message to send.
        Returns:
            - None
        Raises:
            - None
        '''
        msg = msg + self.__separator
        self.__serial.write(bytes(msg.encode('utf-8')))


    def receive_msg(self) -> List[str]:
        '''
        Read until an separator is found, the size is exceeded or until timeout occurs. 
        Args:
            - None
        Returns:
            - msg_decoded (List[str]): Received message of the device.
        Raises:
            - None
        '''
        msg = self.__serial.read_until(self.__separator)
        msg_decoded = self.decode_and_split(msg)
        return msg_decoded


    def send_and_read(self, msg: str) -> List[str]:
        '''Send a message to the serial device and read the response.
        Args:
            - msg (str): Message to send.
        Returns:
            - msg (List[str]): Received message.
        Raises:
            - None
        '''
        self.send_msg(msg)
        response: list = self.receive_msg()
        return response


    def close(self) -> None:
        '''Close the serial connection.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        self.__serial.close()
