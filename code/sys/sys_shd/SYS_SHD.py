#!/usr/bin/python3

#######################        MANDATORY IMPORTS         #######################
import sys, os
sys.path.append(os.getcwd())  #get absolute path


#######################      LOGGING CONFIGURATION       #######################
from SYS.SYS_LOG import SYS_LOG_LoggerGetModuleLogger
log = SYS_LOG_LoggerGetModuleLogger(__name__)

#######################         GENERIC IMPORTS          #######################
from queue import Queue, Empty, Full
from copy import deepcopy
from threading import Condition
from typing import List

#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################

#######################          PROJECT IMPORTS         #######################

#######################              ENUMS               #######################

#######################             CLASSES              #######################

DEFAULT_QUEUE_SIZE : int = 1000

class SYS_SHD_Shared_Obj_c:
    def __init__(self, shared_obj) -> None:
        '''
        Initialize the mutex lock used to protect the shared object.

        Args:
            shared_obj ([type]): Reference to the shared object.
        '''        
        self.__mutex = Condition()
        self.__shared_obj = shared_obj
    
    def read(self) -> object:
        '''
        Gets the mutex control, copy the shared object, release the mutex control
        and returns the copy.

        Returns:
            object: Copy of the private shared_obj attribute.
        '''
        self.__mutex.acquire()
        copied_obj = deepcopy(self.__shared_obj)
        self.__mutex.release()
        return copied_obj

    def write(self, new_obj) -> None:
        '''
        Gets the mutex control, check if the type of the stored shared_obj is equal
        to the new one, write a copy of the passed object to the local shared_obj
        attribute and return the mutex control.

        Args:
            new_obj ([type]): Object desired to be shared among threads.
        '''        
        self.__mutex.acquire()
        if type(self.__shared_obj) is type(new_obj):
            self.__shared_obj = deepcopy(new_obj)
        else:
            log.warning("Type of new object assigned to shared object is different from the previous one assigned.")
        self.__mutex.release()

    def _mergeClass(dst_obj : object, src_obj : object, attribs : List[str]) -> None:
        '''
        Copy the attribute composed of attribs list sequence from src_obj to dst_obj.

        Args:
            dst_obj (object): Destination object where specified attribute is copied.
            src_obj (object): Source object where specified attribute is copied from. 
            attribs (List[str]): Sequence of attributes names used to achieve the nested attributes to be copied.

        Raises:
            SYS_SHD_Chan_Error_c: Throw an exception if the attribute doesn't exists.
        '''        
        if hasattr(dst_obj, attribs[0]) and hasattr(src_obj, attribs[0]):
            old_inst = getattr(dst_obj, attribs[0])
            if isinstance(old_inst, dict):
                new_dict = getattr(src_obj, attribs[0])
                for k, v in old_inst.items():
                    if len(attribs) > 1:
                        SYS_SHD_Shared_Obj_c._mergeClass(v, new_dict[k], attribs[1:])
                    else:
                        old_inst[k] = new_dict[k] 
                setattr(dst_obj, attribs[0], old_inst)
            else:
                if len(attribs) > 1:
                    SYS_SHD_Shared_Obj_c._mergeClass(getattr(dst_obj, attribs[0]), getattr(src_obj, attribs[0]), attribs[1:])
                else:
                    setattr(dst_obj, attribs[0], getattr(src_obj, attribs[0]))
        else:
            log.error(f"New object doesn't have attribute: {attribs[0]}")
            raise SYS_SHD_Chan_Error_c(message=f"New object doesn't have attribute: {attribs[0]}")                


    def mergeIncludedTags(self, new_obj : object, included_tags : List[str]) -> object:
        '''
        Merge shared object with the attributes specified in the new object using the provided attributes .

        Args:
            new_obj (object): [description]
            included_tags (List[str]): [description]

        
        '''        
        '''
        Merge shared object with the new object using the attributes specified in included_tags.
        Copies from new_obj to the shared object the attributes whose names appear in included_tags. 
        If the attribute is a dictionary, or it is a subclass contained in an dict, 
        the merge is done recursively for each item in dict.

        Args:
            new_obj (object): Object that contains the attributes to be copied.
            included_tags (List[str]): Nested names of attributes to be included in merge.
        Returns:
            object: Return a copy of the merged object
        '''        
        temp_obj = self.read()

        for t in included_tags:
            attribs = t.split(".")
            SYS_SHD_Shared_Obj_c._mergeClass(temp_obj, new_obj, attribs)

        self.write(temp_obj)       

        return temp_obj
    
    def mergeExcludedTags(self, new_obj : object, included_tags : List[str]) -> object:
        '''
        Merge shared object with the new object excluding the attributes specified in excluded_tags.
        Copies from new_obj to the shared object all the attributes, except those names that appear in excluded_tags. 
        If the attribute is a dictionary, or it is a subclass contained in an dict, 
        the merge is done recursively for each item in dict.

        Args:
            new_obj (object): Object that contains the attributes to be copied.
            excluded_tags (List[str]): Nested names of attributes to be excluded in merge.
                Attributes preserved from shared object. 
            Merge the included_tags into the class .

        Args:
            new_obj (object): [description]
            included_tags (List[str]): [description]
        
        Returns:
            object: Return a copy of the merged object
        '''        
        # Copy original data to preserver excluded tags
        temp_obj = self.read()

        # Write excluded original tags to new object
        for t in included_tags:
            attribs = t.split(".")
            SYS_SHD_Shared_Obj_c._mergeClass(new_obj, temp_obj, attribs)

        # Write new object with excluded tags to shared object
        self.write(new_obj) 

        return new_obj

class SYS_SHD_Chan_Error_c(Exception):
    def __init__(self, message) -> None:
        '''
        Exception raised for errors when a queue is full and data has tried to be put in it.

        Args:
            message (str): explanation of the error
        '''        
        super().__init__(message)

class SYS_SHD_Chan_c(Queue):

    def __init__(self, maxsize: int = DEFAULT_QUEUE_SIZE) -> None:
        '''
        Initialize the python Queue subclass used to intercommunicate threads.

        Args:
            maxsize (int, optional): Queue max size. Defaults to 100
        '''
        super().__init__(maxsize = maxsize)
        
    def deleteUntilLast(self) -> None:
        '''
        Delete all items from the queue, except the last one.
        '''
        while self.qsize() > 1:
                self.get()
        
    def receiveData(self) -> object:
        '''
        Pop the first element from the queue and return it. If queue is empty, 
        wait until a new element is pushed to the queue.
        
        Returns:
            object: The first element of the queue.
        '''
        return self.get()
        
    def receiveDataUnblocking(self) -> object:
        '''
        Receive data from the queue in unblocking mode.
        
        Returns:
            object: Return the first element from the queue if it is not empty. 
            Return None otherwise.
        '''        
        data = None
        if not self.isEmpty():
            try:
                data = self.get_nowait()
            except Empty:
                log.warning("Error receiving data from channel")
        return data

    def sendData(self, data) -> None:
        '''
        Push data to the queue .

        Args:
            data (object): Data to be pushed to the queue.

        Raises:
            SYS_SHD_Chan_Error_c: Throw an exception if the queue is full.
        '''        
        try:
            self.put_nowait(data)
        except Full as err:
            log.error(err)
            raise SYS_SHD_Chan_Error_c("Data can't be put in queue because it's full")
  
    def isEmpty(self) -> bool:
        '''
        Check if the queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        '''        
        return self.empty()


#######################            FUNCTIONS             #######################
