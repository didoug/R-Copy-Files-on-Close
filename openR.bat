@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "RSTUDIO_EXE=%ProgramFiles%\RStudio\rstudio.exe"

if not exist "%RSTUDIO_EXE%" set "RSTUDIO_EXE=%ProgramFiles%\RStudio\bin\rstudio.exe"

if not exist "%RSTUDIO_EXE%" (
    echo RStudio was not found. Update the path in openR.bat.
    pause
    exit /b 1
)

start "" /wait "%RSTUDIO_EXE%"

pushd "%SCRIPT_DIR%"
where py >nul 2>&1
if %errorlevel%==0 (
    py -3 copyFilesToGDrive.py
) else (
    python copyFilesToGDrive.py
)
popd

endlocal
