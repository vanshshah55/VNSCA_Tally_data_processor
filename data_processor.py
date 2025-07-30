#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data processing module for the Excel Processing Application.
Handles Excel file operations, data manipulation, and analysis.
"""

import pandas as pd
import numpy as np
from config import PR_SHEET_IDENTIFIER, FOOTER_KEYWORDS, COMMON_HEADER_NAMES

class ExcelProcessor:
    """
    Handles all Excel file processing operations.
    
    This class is responsible for loading Excel files, detecting headers and footers,
    adding columns, and processing data according to business rules.
    """
    
    def __init__(self):
        """Initialize the Excel processor."""
        self.file_path = None
        self.workbook = None
        self.sheet_name = None
        self.raw_data = None
        self.processed_data = None
        self.header_rows = []
        self.footer_rows = []
        self.data_rows = []
        self._header_row_index = -1  # Index of the identified header row
    
    def load_file(self, file_path):
        """
        Load an Excel file and identify the appropriate sheet.
        
        Args:
            file_path (str): Path to the Excel file
            
        Returns:
            tuple: (success, message, sheet_names)
        """
        try:
            self.file_path = file_path
            self.workbook = pd.ExcelFile(file_path)
            sheet_names = self.workbook.sheet_names
            
            # Try to find a sheet with "PR" in its name
            pr_sheets = [sheet for sheet in sheet_names if PR_SHEET_IDENTIFIER.lower() in sheet.lower()]
            
            if pr_sheets:
                self.sheet_name = pr_sheets[0]
                message = f"Found sheet with 'PR' in name: {self.sheet_name}"
            else:
                self.sheet_name = sheet_names[0]
                message = f"No sheet with 'PR' in name found. Using first sheet: {self.sheet_name}"
            
            # Load the raw data
            self.raw_data = pd.read_excel(file_path, sheet_name=self.sheet_name)
            
            # Process the data
            self._detect_structure()
            self._extract_data_rows()
            
            return True, message, sheet_names
        
        except Exception as e:
            return False, f"Error loading file: {str(e)}", []
    
    def _detect_structure(self):
        """
        Detect header and footer rows in the Excel sheet.
        
        This method analyzes the data to identify header rows (typically at the top with text)
        and footer rows (typically at the bottom with summary information).
        """
        self.header_rows = []
        self.footer_rows = []
        
        # Find the row with the most column header names
        best_header_row = -1
        max_header_matches = 0
        max_non_empty = 0
        
        # Examine first 20 rows to find the best header row
        for i, row in self.raw_data.iloc[:min(20, len(self.raw_data))].iterrows():
            # Skip empty or nearly empty rows
            non_empty_count = sum(1 for val in row if pd.notna(val))
            if non_empty_count <= 2:
                continue
                
            # Convert row values to lowercase strings for comparison
            row_values = [str(val).lower().strip() for val in row if pd.notna(val)]
            
            # Count how many common header names are in this row
            header_name_matches = 0
            for val in row_values:
                for header_name in COMMON_HEADER_NAMES:
                    if header_name in val or val in header_name:
                        header_name_matches += 1
                        break
            
            # Check for exact matches with key column names
            key_columns = ['date', 'particular', 'voucher']
            key_matches = sum(1 for val in row_values if val in key_columns)
            
            # Prioritize rows with key column matches
            if key_matches > 0:
                header_name_matches += key_matches * 2
            
            # If this row has more header matches than previous best, or same matches but more non-empty cells
            if (header_name_matches > max_header_matches) or \
               (header_name_matches == max_header_matches and non_empty_count > max_non_empty):
                max_header_matches = header_name_matches
                max_non_empty = non_empty_count
                best_header_row = i
        
        # If we found a good header row
        if best_header_row >= 0 and max_header_matches >= 2:
            # All rows before the header row are also headers
            self.header_rows = list(range(best_header_row + 1))
            
            # Use the header row to set column names
            header_values = self.raw_data.iloc[best_header_row].tolist()
            valid_headers = [str(h).strip() if pd.notna(h) else f"Column_{i+1}" for i, h in enumerate(header_values)]
            
            # Store the identified header row index for later use
            self._header_row_index = best_header_row
        else:
            # Fallback to heuristic approach if no clear header row found
            for i, row in self.raw_data.iterrows():
                # Count non-numeric values and non-empty cells
                non_numeric_count = sum(1 for val in row if not self._is_numeric(val) and pd.notna(val))
                non_empty_count = sum(1 for val in row if pd.notna(val))
                
                # Consider it a header if it has many non-numeric values or looks like column headers
                if (non_numeric_count > len(row) / 3 and non_empty_count > len(row) / 4) or \
                   (i < 5 and non_empty_count > 3 and non_numeric_count / max(non_empty_count, 1) > 0.7):
                    self.header_rows.append(i)
                elif i > 0 and non_empty_count > 0:  # If we've found a data row after headers
                    break
            
            # No specific header row identified
            self._header_row_index = -1
        
        # Check for footer rows (summary rows or empty rows at the bottom)
        consecutive_empty_rows = 0
        for i in range(len(self.raw_data) - 1, -1, -1):
            row = self.raw_data.iloc[i]
            
            # Skip if this row is already identified as a header
            if i in self.header_rows:
                break
                
            # Check if row is empty or nearly empty
            non_empty_count = sum(1 for val in row if pd.notna(val))
            if non_empty_count <= 2:  # Row is empty or nearly empty
                self.footer_rows.append(i)
                consecutive_empty_rows += 1
                if consecutive_empty_rows >= 3:  # If we've found several consecutive empty rows, stop
                    break
                continue
            else:
                consecutive_empty_rows = 0  # Reset counter when we find a non-empty row
            
            # Check if row contains summary keywords
            row_values = [str(val).lower() for val in row if pd.notna(val)]
            row_text = " ".join(row_values).lower()
            if any(keyword in row_text for keyword in FOOTER_KEYWORDS):
                self.footer_rows.append(i)
                # Also include a few rows after a total/summary row as they're likely part of the footer
                for j in range(i+1, min(i+3, len(self.raw_data))):
                    if j not in self.footer_rows and j not in self.header_rows:
                        self.footer_rows.append(j)
                continue
            
            # If we've processed several non-empty, non-summary rows, stop looking for footers
            if i < len(self.raw_data) - 5:
                break
    
    def _extract_data_rows(self):
        """
        Extract data rows excluding headers and footers.
        Use column names from identified header row if available.
        """
        all_rows = set(range(len(self.raw_data)))
        exclude_rows = set(self.header_rows + self.footer_rows)
        self.data_rows = sorted(list(all_rows - exclude_rows))
        
        # Create processed data with only data rows
        if self._header_row_index >= 0:
            # Get column names from the identified header row
            header_values = self.raw_data.iloc[self._header_row_index].tolist()
            column_names = []
            
            # Clean up column names
            for i, h in enumerate(header_values):
                if pd.isna(h):
                    column_names.append(f"Column_{i+1}")
                else:
                    # Clean and normalize column name
                    clean_name = str(h).strip()
                    if not clean_name or clean_name.lower() == 'nan':
                        clean_name = f"Column_{i+1}"
                    column_names.append(clean_name)
            
            # Create DataFrame with proper column names
            self.processed_data = pd.DataFrame(self.raw_data.iloc[self.data_rows].values, columns=column_names)
        else:
            # Fallback to original column names
            self.processed_data = self.raw_data.iloc[self.data_rows].reset_index(drop=True)
    
    def add_columns(self, columns_to_add):
        """
        Add new columns to the processed data.
        
        Args:
            columns_to_add (list): List of column names to add
            
        Returns:
            bool: Success status
        """
        try:
            for column in columns_to_add:
                if column not in self.processed_data.columns:
                    self.processed_data[column] = ""
            return True
        except Exception:
            return False
    
    def process_ledger_head(self, selected_columns):
        """
        Process the LEDGER HEAD column based on numeric values in selected columns.
        
        Args:
            selected_columns (list): List of column names to analyze
            
        Returns:
            bool: Success status
        """
        try:
            if 'LEDGER HEAD' not in self.processed_data.columns:
                self.processed_data['LEDGER HEAD'] = ""
            
            for idx, row in self.processed_data.iterrows():
                numeric_columns = []
                
                for col in selected_columns:
                    if col in self.processed_data.columns and self._is_numeric(row[col]) and row[col] != 0:
                        numeric_columns.append(col)
                
                if numeric_columns:
                    self.processed_data.at[idx, 'LEDGER HEAD'] = " + ".join(numeric_columns)
            
            return True
        except Exception:
            return False
    
    def _is_numeric(self, val):
        """
        Check if a value is numeric (int or float) and not NaN.
        
        Args:
            val: Value to check
            
        Returns:
            bool: True if numeric, False otherwise
        """
        if pd.isna(val):
            return False
        
        try:
            float_val = float(val)
            return not pd.isna(float_val)
        except (ValueError, TypeError):
            return False
    
    def get_preview_data(self, rows=10):
        """
        Get a preview of the processed data.
        
        Args:
            rows (int): Number of rows to include in preview
            
        Returns:
            DataFrame: Preview data with proper column names
        """
        if self.processed_data is None or len(self.processed_data) == 0:
            return pd.DataFrame()
        
        # Create a copy of the preview data to avoid modifying the original
        preview = self.processed_data.head(rows).copy()
        
        # Ensure all columns have proper names (no 'Unnamed: X' columns)
        renamed_columns = {}
        for col in preview.columns:
            if 'Unnamed:' in str(col):
                renamed_columns[col] = f"Column_{preview.columns.get_loc(col)+1}"
        
        if renamed_columns:
            preview = preview.rename(columns=renamed_columns)
            
        return preview
    
    def save_to_file(self, output_path):
        """
        Save the processed data to a new Excel file.
        
        This method saves only from the detected header row onwards,
        preserving the column structure and processed data.
        
        Args:
            output_path (str): Path to save the Excel file
            
        Returns:
            tuple: (success, message)
        """
        try:
            # Determine which data to save based on header detection
            if self._header_row_index >= 0:
                # Create a new DataFrame with the header row and processed data
                # First, get the header row values
                header_values = self.raw_data.iloc[self._header_row_index].tolist()
                column_names = []
                
                # Clean up column names
                for i, h in enumerate(header_values):
                    if pd.isna(h):
                        column_names.append(f"Column_{i+1}")
                    else:
                        clean_name = str(h).strip()
                        if not clean_name or clean_name.lower() == 'nan':
                            clean_name = f"Column_{i+1}"
                        column_names.append(clean_name)
                
                # Create output DataFrame with the processed data
                output_data = self.processed_data.copy()
                
                # Add any missing columns from original data
                for i, col_name in enumerate(column_names):
                    if col_name not in output_data.columns and i < len(self.raw_data.columns):
                        # Get the column data from raw_data for the data rows
                        col_data = [self.raw_data.iloc[idx, i] if i < len(self.raw_data.columns) else "" 
                                   for idx in self.data_rows]
                        output_data[col_name] = col_data
            else:
                # If no specific header row was detected, use the processed data as is
                output_data = self.processed_data.copy()
            
            # Save to Excel - only the processed data with proper column names
            output_data.to_excel(output_path, sheet_name=self.sheet_name, index=False)
            
            return True, f"File saved successfully to {output_path}"
        
        except Exception as e:
            return False, f"Error saving file: {str(e)}"