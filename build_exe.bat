@echo off
echo Creating icon for Tally_LH_Processor...
python create_icon.py

echo Installing required packages...
pip install pyinstaller pillow

echo Building executable with PyInstaller...
pyinstaller --clean tally_lh_processor.spec

echo.
echo Build complete! Check the "dist" folder for Tally_LH_Processor.exe
echo.