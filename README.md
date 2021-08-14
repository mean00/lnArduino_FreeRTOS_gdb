
This are  modified version of FreeRTOS-GDB (https://github.com/autolycus/FreeRTOS-GDB) for my needs
Bottom line, i use a blackmagic clone debugger and it does not support FreeRTOS
I just want to have backtrack for all the tasks on the system
to see what they are doing and why they are stuck

The aim is to be similar to the "info thread" "thread x" commands of gdb

Disclaimer : I probably broke the other functions + i'm not a python developper

There are 2 subfolders :
* riscv for GD32V103 style chips
* arm_m3 for cortex m3/m0+ chips

Read the readme in each subfolder to have platform specific changes
