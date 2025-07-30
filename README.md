# Excel Processing Application

A Python desktop application for processing Excel files with a focus on PR sheets.

## Features

- Upload and process Excel files (.xlsx or .xls)
- Automatically detect and select sheets with "PR" in their name
- Intelligently exclude header and footer rows
- Add custom columns (LEDGER HEAD, TAXABLE VALUE, CGST, SGST, IGST)
- Process LEDGER HEAD column based on numeric values in selected columns
- Preview data before saving
- Save processed data to a new Excel file

## Requirements

- Python 3.7 or higher
- Required packages:
  - pandas
  - numpy
  - openpyxl (for Excel file handling)
  - tkinter (included with standard Python installation)

## Installation

1. Clone or download this repository
2. Install required packages:

```bash
pip install pandas numpy openpyxl
```

## Usage

1. Run the application:

```bash
python main.py
```

2. Click "Upload File" to select an Excel file
3. Use "Add Columns" to add required columns to the data
4. Use "Process LEDGER HEAD" to analyze selected columns and populate the LEDGER HEAD column
5. Preview the data in the table
6. Click "Save Output" to save the processed data to a new Excel file

## Project Structure

- `main.py`: Entry point for the application
- `gui.py`: GUI implementation using Tkinter
- `data_processor.py`: Excel file processing and data manipulation
- `utils.py`: Utility functions for the application
- `config.py`: Configuration settings and constants

## Workflow Example

1. Upload an Excel file with a PR sheet
2. Add the 'LEDGER HEAD' column
3. Process the LEDGER HEAD column by selecting relevant columns to analyze
4. Save the processed file with the added and populated columns

## Extensibility

The application is designed to be easily extended:
- Add new column types in `config.py`
- Implement new processing rules in `data_processor.py`
- Add new UI features in `gui.py`