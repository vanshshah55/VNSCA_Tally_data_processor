# Packaging Instructions for Tally Ledger Head Processor

This document provides detailed instructions for packaging the Tally Ledger Head Processor application into a standalone executable (.exe) file using PyInstaller.

## Prerequisites

1. Python 3.7 or higher installed
2. Required Python packages:
   - pandas
   - numpy
   - openpyxl
   - pillow (for icon creation)
   - pyinstaller

## Step-by-Step Packaging Process

### 1. Install Required Packages

```bash
pip install pandas numpy openpyxl pillow pyinstaller
```

### 2. Create Application Icon

Run the `create_icon.py` script to generate the application icon:

```bash
python create_icon.py
```

This will create a file named `tally_lh_processor.ico` in the current directory.

### 3. Build the Executable

#### Option 1: Using the Batch File (Recommended)

Simply run the provided batch file:

```bash
build_exe.bat
```

This will:
- Create the application icon
- Install required packages
- Build the executable using PyInstaller with optimized settings

#### Option 2: Manual PyInstaller Command

If you prefer to run the command manually:

```bash
pyinstaller --clean tally_lh_processor.spec
```

### 4. Locate the Executable

After the build process completes, the executable file will be located in the `dist` directory:

```
dist/Tally_LH_Processor.exe
```

## Size Optimization

The PyInstaller spec file (`tally_lh_processor.spec`) includes several optimizations to reduce the size of the final executable:

1. Excluding unnecessary packages:
   - matplotlib
   - scipy
   - PyQt5/PyQt6
   - PySide2/PySide6
   - IPython
   - notebook
   - sphinx
   - pytest

2. Removing unnecessary modules from pandas and numpy:
   - pandas/tests
   - pandas/io/formats/templates
   - numpy/core/tests
   - numpy/doc
   - numpy/f2py
   - numpy/testing

3. Using UPX compression (if available)

## Troubleshooting

### Common Issues

1. **Missing Dependencies**:
   - If PyInstaller complains about missing modules, add them to the `hiddenimports` list in the spec file.

2. **Large Executable Size**:
   - Try adding more exclusions in the spec file
   - Use the `--exclude-module` option to exclude unused libraries

3. **Application Crashes on Startup**:
   - Check if all required DLLs are included
   - Try building with `--debug=all` to get more information

### Testing the Executable

Before distributing the executable, test it on a clean system (without Python installed) to ensure it works correctly.

## Distribution

To distribute the application:

1. Copy the `Tally_LH_Processor.exe` file from the `dist` directory
2. Include the README.md file for user instructions
3. Package these files into a ZIP archive or installer if desired

## Future Updates

When updating the application:

1. Increment the version numbers in `file_version_info.txt`
2. Rebuild the executable using the same process
3. Document any changes in a changelog file

---

For any questions or issues with the packaging process, please contact the development team.