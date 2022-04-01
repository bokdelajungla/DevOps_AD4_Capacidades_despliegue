@echo off
set fichero=cadenas.txt
set /A puerto=12345

:loop
if "%1" == "" goto done
if "%1" == "-f" set "fichero=%2"
if "%1" == "-p" set "puerto=%2"
shift
goto :loop

:done
python server.py -f %fichero% -p %puerto%
