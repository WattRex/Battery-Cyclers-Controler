# README

- ```__init.py__``` has to be edited to work properly in your project.
- Change the variable name where the main logger is declared.

# Logging template

## Code to paste on top of the main.py file

```
from DRV.DRV_LOG import DRV_LOG_Logger_c
cycler_logger = DRV_LOG_Logger_c('./DRV/DRV_LOG/logginConfig.conf')
```

## Code to paste on top of every .py file

```
from DRV.DRV_LOG import DRV_LOG_LoggerGetModuleLogger
log = DRV_LOG_LoggerGetModuleLogger(__name__)
```