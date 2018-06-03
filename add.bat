echo off
set name=fde_test
set folder=lib
::set path=

python .\python\add.py -n %name% -f %folder%
pause
