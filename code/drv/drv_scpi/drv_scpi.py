#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
Driver for SCPI devices.
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
from typing import List
import serial

#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################


#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################
class _DefaultSerialParamsC():
    "Communication constants"
    BAUD_RATE           = 115200
    BYTESIZE            = serial.EIGHTBITS
    PARITY              = serial.PARITY_NONE
    STOP_BITS           = serial.STOPBITS_ONE
    READ_TIMEOUT        = 0.5
    WRITE_TIMEOUT       = 0.5
    INTER_BYTE_TIMEOUT  = 0.5
    MAX_LEN_IN_BYTES    = 21

#######################             CLASSES              #######################
class DrvScpiErrorC():
    '''Error class for SCPI driver.
    '''
    def __init__(self, message: str, error_code: int) -> None:
        self.message    = message
        self.error_code  = error_code

    def __str__(self) -> str:
        return f"Error: {self.message} \t Code: {self.error_code}"


class DrvScpiHandlerC():
    '''Driver for SCPI devices.
    '''
    def __init__(self, port: str, separator: str, baudrate: int = _DefaultSerialParamsC.BAUD_RATE, bytesize = _DefaultSerialParamsC.BYTESIZE,
                 parity = _DefaultSerialParamsC.PARITY, stopbits = _DefaultSerialParamsC.STOP_BITS, timeout = _DefaultSerialParamsC.READ_TIMEOUT,
                 write_timeout = _DefaultSerialParamsC.WRITE_TIMEOUT, inter_byte_timeout = _DefaultSerialParamsC.INTER_BYTE_TIMEOUT) -> None:
         
        self.__serial: serial.Serial = serial.Serial(port = port, baudrate = baudrate, bytesize = bytesize, parity = parity, stopbits = stopbits,
                                                     timeout = timeout, write_timeout = write_timeout, inter_byte_timeout = inter_byte_timeout)
        self.__separator: str = separator


    def decode_numbers(self, data: bytes) -> List[int]:
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
            msg_decode = [int(i) for i in msg_decode]
        except ValueError:
            raise DrvScpiErrorC(message = "Error decoding data", error_code = 2)
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
            raise DrvScpiErrorC(message = "Error reading device information", error_code = 1)
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
        Receive a message from the serial port in blocking mode.
        Args:
            - None
        Returns:
            - msg_decoded (List[str]): Received message.
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