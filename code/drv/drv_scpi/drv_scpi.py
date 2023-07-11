#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
Driver for SCPI devices.
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
import serial

#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################


#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################
class _Default_Serial_Params_c():
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
class DRV_SCPI_Error_c():
    def __init__(self, message: str, errorCode: int) -> None:
        self.message    = message
        self.error_code  = errorCode

    def __str__(self) -> str:
        return f"Error: {self.message} \t Code: {self.error_code}"


class DRV_SCPI_Handler_c():
    def __init__(self, port: str, separator: str, baudrate: int = _Default_Serial_Params_c.BAUD_RATE, bytesize = _Default_Serial_Params_c.BYTESIZE,
                 parity = _Default_Serial_Params_c.PARITY, stopbits = _Default_Serial_Params_c.STOP_BITS, timeout = _Default_Serial_Params_c.READ_TIMEOUT,
                 write_timeout = _Default_Serial_Params_c.WRITE_TIMEOUT, inter_byte_timeout = _Default_Serial_Params_c.INTER_BYTE_TIMEOUT) -> None:
         
        self.__serial: serial.Serial = serial.Serial(port = port, baudrate = baudrate, bytesize = bytesize, parity = parity, stopbits = stopbits,
                                                     timeout = timeout, write_timeout = write_timeout, inter_byte_timeout = inter_byte_timeout)
        self.__separator: str = separator


    def decodeStr2Numbers(self, data: str) -> int:
        '''Decode str to integers.
        Args:
            data (str): [description]
        Returns:
            int: [description]
        Raises:
            - None
        '''
        pass


    def decodeAndSplit(self, data: bytes) -> list:
        '''Decode str to integers and split the data.
        Args:
            data (bytes): Value to decode and split.
        Returns:
            msg_decode (list): Message decoded and splited.
        Raises:
            - None
        '''
        data = data.decode('utf-8')
        msg_decode = data.split(f"{self.__separator}")
        return msg_decode


    def readDeviceInfo(self) -> list:
        '''Reads the list of device information.
        Args:
            - None
        Returns:
            - msg (list): List of device information.
        Raises:
            - None
        '''

        msg = self.sendAndRead('*IDN?')
        return msg


    def sendMsg(self, msg:str) -> None:
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


    def receiveMsg(self) -> list:
        '''
        Receive a message from the serial port in blocking mode.
        Args:
            - None
        Returns:
            - msg_decoded (str): Received message.
        Raises:
            - None
        '''
        msg = self.__serial.read_until(self.__separator)
        msg_decoded = self.decodeAndSplit(msg)
        return msg_decoded


    def sendAndRead(self, msg: str) -> list:
        '''Send a message to the serial device and read the response.
        Args:
            - msg (str): Message to send.
        Returns:
            - msg (str): Received message.
        Raises:
            - None
        '''
        self.sendMsg(msg)
        response: list = self.receiveMsg()
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