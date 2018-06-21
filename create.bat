echo off
set sln_path=E:\code\fde_lib_nex
set sln_name=fde_lib
set sln_namespace=fde

python .\python\create.py -p "%sln_path%" -n "%sln_name%" -s "%sln_namespace%"

pause
