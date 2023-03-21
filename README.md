
These are  modified version of FreeRTOS-GDB (https://github.com/autolycus/FreeRTOS-GDB) for my needs
Bottom line, i use a blackmagic clone debugger and it does not support FreeRTOS.
I just want to have backtrack for all the tasks on the system
to see what they are doing and why they are stuck

The aim is to be similar to the "info thread" "thread x" commands of gdb

Disclaimer : I probably broke the other functions + i'm not a python developper

There are 4 subfolders :
* riscv for GD32V103 style chips
* arm_m3 for cortex m3/m0+ chips
* arm_m4 for cortex m4+fpu chips
* ch32_riscv for ch32 riscv chips. 
( on ch32v3x I'm using a modified register layout on the stack to avoid saving fpu registers when not used)

Read the readme in each subfolder to have platform specific changes

Usage :

# be sure to have the folder you use in your python path
export PYTHON_TOOL=some folder/freeRTOS_gdb_support/ch32_riscv
export PYTHONPATH=${PYTHON_TOOL}/

...
start gdb...
source some folder/freeRTOS_gdb_support/ch32_riscv/FreeRTOS.py
...

Now you have 2 new functions from with gdb:
- show Task-List to list all freeRTOS threads
- switchTCB x  : swith to thread x

