@echo off
REM Windows Build Script - Friesen Enrollment Converter
REM This batch file makes it easy to run the Python build script

echo Friesen Enrollment Converter - Windows Build
echo =====================================
echo.
echo IMPORTANT: Make sure you have installed runtime dependencies first:
echo    pip install -r requirements.txt
echo.

REM Check if we're in the right directory
if not exist "src\main.py" (
    echo Error: Please run this script from the project root directory
    echo Expected to find: src\main.py
    pause
    exit /b 1
)

REM Run the Python build script
echo Running build script...
python build\windows\build.py %*

echo.
echo Build process finished.
pause 