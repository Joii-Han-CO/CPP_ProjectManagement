echo off
set sln_path=D:\tmp
set sln_name=fde_lib
set sln_namespace=fde_lib

python .\python\create.py -p "%sln_path%" -n "%sln_name%" -s "%sln_namespace%"

pause
