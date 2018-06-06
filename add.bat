echo off
set name=ipc
set folder=lib
set s_path=E:\code\fde_lib_new\fde_lib

python .\python\add.py -p %s_path% -n %name% -f %folder%
pause
