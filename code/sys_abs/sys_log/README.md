# README

- ```__init.py__``` has to be edited to work properly in your project.
- Change the variable name where the main logger is declared.

# Logging template

## Code to paste on top after imports of the main.py file

```
from sys_abs.sys_log import SysLogLoggerC, sys_log_logger_get_module_logger
cycler_logger = SysLogLoggerC('./sys_abs/sys_log/logginConfig.conf')
log = sys_log_logger_get_module_logger(__name__, './log_config.yaml')
```

## Code to paste on top after imports of every .py file

```
from sys_abs.sys_log import sys_log_logger_get_module_logger
log = sys_log_logger_get_module_logger(__name__)
```

# Complete the ```log_config.yaml``` file (or whatever name you gave it)

- You can place this file where you want but you have to specify its path and name when sys_log_logger_get_module_logger function is used.
- If the file ```log_config.yaml``` is empty, all loggers created on your modules will be defined at error level by default.
- To assign an specific logging level to a module, you have to write its name in this file and set the desired logging level like the following example.
- There is a template of the file in ```template_log_config.yaml```
```
MID.MID_DABS: "DEBUG"
```

- Example of this file properly filled:

```
--- #YAML FILE START
APP.APP_MODULE: "CRITICAL" #APP/APP_MODULE/APP_EXAMPLE.py

__main__: "CRITICAL"
Test_MID_FLOW : "CRITICAL"

##### APP #####
APP.APP_SALG: "DEBUG"
APP.APP_DIAG: "WARN"
APP.APP_STRG: "WARN"

##### MID #####
MID.MID_FLOW: "WARN"
MID.MID_SOC: "WARN"
MID.MID_PWR: "WARN"
MID.MID_DABS: "WARN"
MID.MID_STR: "INFO"
MID.MID_SYNC: "WARN"
MID.MID_COMM: "INFO"

##### DRV ######
DRV.DRV_CAN: "WARN"
DRV.DRV_MODBUS: "CRITICAL"

DRV.DRV_EPC: "ERROR"
DRV.DRV_PLAK: "ERROR"

DRV.DRV_VFD: "WARN"
DRV.DRV_GFRAN: "CRITICAL"
DRV.DRV_VAT: "WARN"
DRV.DRV_TMP: "WARN"
DRV.DRV_HVAC: "WARN"
# DRV.DRV_EA: "CRITICAL"
# DRV.DRV_RS: "CRITICAL"

DRV.DRV_DB: "WARN"
DRV.DRV_MQTT: "WARN"

DRV.DRV_IO: "WARN"
DRV.DRV_LVL: "WARN"

##### SYS #####
SYS.SYS_SHD: "WARN"
SYS.SYS_CONF: "WARN"
SYS.SYS_LOG: "WARN"
SYS.SYS_PARS: "WARN"
```