@echo off
setlocal

REM --- Configuration ---
set VENV_DIR=.\venv_build
set PYTHON_EXE=%VENV_DIR%\Scripts\python.exe
set PI_EXE=%VENV_DIR%\Scripts\pyinstaller.exe
set LOG_FILE=build_log.txt

REM --- Start Fresh ---
echo. > %LOG_FILE%
echo Build started at %date% %time% >> %LOG_FILE%

REM --- Clean Up Old Build Artifacts ---
echo Cleaning up old build artifacts...
if exist "dist\Tally_LH_Processor_Optimized.exe" del /F /Q "dist\Tally_LH_Processor_Optimized.exe"
if exist "build" rmdir /S /Q build

REM --- Create or Re-use Virtual Environment ---
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creating a new virtual environment...
    python -m venv %VENV_DIR% >> %LOG_FILE% 2>&1
    if %errorlevel% neq 0 ( echo ERROR: Failed to create virtual environment. Check %LOG_FILE%. & goto :error )
) else (
    echo Using existing virtual environment.
)

REM --- Install/Upgrade Dependencies ---
echo Installing required packages... This may take a moment.
%PYTHON_EXE% -m pip install --upgrade pip >> %LOG_FILE% 2>&1
%PYTHON_EXE% -m pip install -r requirements.txt --upgrade >> %LOG_FILE% 2>&1
%PYTHON_EXE% -m pip install pyinstaller pillow --upgrade >> %LOG_FILE% 2>&1
if %errorlevel% neq 0 ( echo ERROR: Failed to install packages. Check %LOG_FILE%. & goto :error )

REM --- Build the Executable ---
echo Building the executable... See %LOG_FILE% for detailed progress.
%PI_EXE% --noconfirm tally_lh_processor_optimized.spec >> %LOG_FILE% 2>&1
if %errorlevel% neq 0 ( echo ERROR: PyInstaller build failed. Check %LOG_FILE%. & goto :error )

REM --- Success ---
echo.
echo ===================================================================
echo  BUILD SUCCESSFUL!
echo ===================================================================
echo.
echo  Your optimized, single-file executable is located at:
_**echo  `dist\Tally_LH_Processor_Optimized.exe`**_
echo.
echo  A detailed log has been saved to `build_log.txt`
echo ===================================================================
echo.
goto :eof

:error
echo.
echo *******************************************************************
echo  BUILD FAILED. Please check the `build_log.txt` for details.
echo *******************************************************************
echo.

:eof
endlocal
pause
