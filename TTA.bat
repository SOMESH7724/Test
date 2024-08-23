@echo off
REM Get the path to the folder where the batch file is located
set SCRIPT_DIR=%~dp0

REM Find the path to the Python executable
for /f "tokens=*" %%i in ('where python') do set PYTHON_PATH=%%i

REM Check if Python was found
if not defined PYTHON_PATH (
    echo Python is not installed or not found in the system PATH.
    pause
    exit /b 1
)

REM Run the Python script located in the same folder as the batch file
%PYTHON_PATH% "%SCRIPT_DIR%Code - 1.py"

pause
