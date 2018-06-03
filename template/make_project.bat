set out_dir=output
md %cd%\\%out_dir%
cd /d %cd%\\%out_dir%
cmake -G "Visual Studio 15 2017" .\..\project\
pause
