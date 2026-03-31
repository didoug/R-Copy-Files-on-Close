set myvar=%cd%

cd C:\Program Files\RStudio\
start rstudio.exe

:check_status
TASKLIST /FI "IMAGENAME EQ RStudio.exe" |FIND ":" > nul
IF ERRORLEVEL 1 TIMEOUT /T 1 /NOBREAK && GOTO check_status 

cd %myvar%
python copyFilesToGDrive.py
