#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI module for the Excel Processing Application.
Implements the user interface using Tkinter.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

from data_processor import ExcelProcessor
from utils import create_scrollable_frame, create_data_table, create_search_bar
from config import ADDABLE_COLUMNS, EXCEL_FILE_TYPES, PREVIEW_ROWS

class AppGUI:
    """
    Main application GUI class.
    
    This class implements the graphical user interface for the Excel Processing Application,
    including file upload, column addition, data preview, and processing functionality.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.excel_processor = ExcelProcessor()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create sections
        self._create_file_section()
        self._create_action_section()
        self._create_preview_section()
        self._create_status_bar()
    
    def _create_file_section(self):
        """Create the file upload section."""
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        # File path display
        self.file_path_var = tk.StringVar()
        file_path_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=50)
        file_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Upload button
        upload_btn = ttk.Button(file_frame, text="Upload File", command=self._upload_file)
        upload_btn.pack(side=tk.RIGHT, padx=5)
    
    def _create_action_section(self):
        """Create the action buttons section."""
        action_frame = ttk.Frame(self.main_frame, padding="10")
        action_frame.pack(fill=tk.X, pady=5)
        
        # Add Columns button
        add_columns_btn = ttk.Button(action_frame, text="Add Columns", command=self._show_add_columns_dialog)
        add_columns_btn.pack(side=tk.LEFT, padx=5)
        
        # Process LEDGER HEAD button
        process_btn = ttk.Button(action_frame, text="Process LEDGER HEAD", command=self._show_process_dialog)
        process_btn.pack(side=tk.LEFT, padx=5)
        
        # Help button
        help_btn = ttk.Button(action_frame, text="Help", command=self._show_help_dialog)
        help_btn.pack(side=tk.LEFT, padx=5)
        
        # Save button
        save_btn = ttk.Button(action_frame, text="Save Output", command=self._save_output)
        save_btn.pack(side=tk.RIGHT, padx=5)
    
    def _create_preview_section(self):
        """Create the data preview section with improved scrolling."""
        preview_frame = ttk.LabelFrame(self.main_frame, text="Data Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create a frame for preview info
        info_frame = ttk.Frame(preview_frame)
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Add info labels
        self.preview_info_var = tk.StringVar(value="No data loaded")
        ttk.Label(info_frame, textvariable=self.preview_info_var).pack(side=tk.LEFT)
        
        # Container for the table
        self.preview_container = ttk.Frame(preview_frame)
        self.preview_container.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder for the table
        self.preview_table = None
    
    def _create_status_bar(self):
        """Create the status bar."""
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        self.status_var.set("Ready")
    
    def _upload_file(self):
        """Handle file upload button click."""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=EXCEL_FILE_TYPES
        )
        
        if not file_path:
            return
        
        self.file_path_var.set(file_path)
        self.status_var.set("Loading file...")
        self.root.update_idletasks()
        
        success, message, sheet_names = self.excel_processor.load_file(file_path)
        
        if success:
            self.status_var.set(message)
            self._update_preview()
        else:
            messagebox.showerror("Error", message)
            self.status_var.set("Error loading file")
    
    def _show_add_columns_dialog(self):
        """Show dialog for adding columns."""
        if self.excel_processor.processed_data is None:
            messagebox.showinfo("Info", "Please upload a file first")
            return
        
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Columns")
        dialog.geometry("300x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create checkboxes for columns
        ttk.Label(dialog, text="Select columns to add:").pack(anchor=tk.W, padx=10, pady=5)
        
        # Variables to track checkbox states
        column_vars = {}
        
        # Select All checkbox
        select_all_var = tk.BooleanVar()
        
        def toggle_all():
            """Toggle all checkboxes based on Select All state."""
            state = select_all_var.get()
            for var in column_vars.values():
                var.set(state)
        
        select_all_cb = ttk.Checkbutton(dialog, text="Select All", variable=select_all_var, command=toggle_all)
        select_all_cb.pack(anchor=tk.W, padx=10, pady=5)
        
        # Individual column checkboxes
        for column in ADDABLE_COLUMNS:
            var = tk.BooleanVar()
            column_vars[column] = var
            cb = ttk.Checkbutton(dialog, text=column, variable=var)
            cb.pack(anchor=tk.W, padx=20, pady=2)
        
        # Add button
        def add_selected_columns():
            """Add selected columns to the data."""
            selected_columns = [col for col, var in column_vars.items() if var.get()]
            
            if not selected_columns:
                messagebox.showinfo("Info", "No columns selected")
                return
            
            success = self.excel_processor.add_columns(selected_columns)
            
            if success:
                self._update_preview()
                self.status_var.set(f"Added columns: {', '.join(selected_columns)}")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to add columns")
        
        ttk.Button(dialog, text="Add", command=add_selected_columns).pack(pady=10)
    
    def _show_process_dialog(self):
        """Show dialog for processing LEDGER HEAD with improved search and selection."""
        if self.excel_processor.processed_data is None:
            messagebox.showinfo("Info", "Please upload a file first")
            return
        
        if 'LEDGER HEAD' not in self.excel_processor.processed_data.columns:
            messagebox.showinfo("Info", "Please add the 'LEDGER HEAD' column first")
            return
        
        # Create dialog window with better size
        dialog = tk.Toplevel(self.root)
        dialog.title("Process LEDGER HEAD")
        dialog.geometry("500x600")
        dialog.minsize(400, 500)  # Set minimum size
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Get all available columns
        available_columns = list(self.excel_processor.processed_data.columns)
        
        # Create header with instructions
        header_frame = ttk.Frame(dialog, padding="10")
        header_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            header_frame, 
            text="Select columns to analyze for numeric values:",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            header_frame,
            text="The LEDGER HEAD column will be populated based on columns containing numeric values.",
            wraplength=480
        ).pack(anchor=tk.W, pady=5)
        
        # Create frame for search and checkboxes
        content_frame = ttk.Frame(dialog, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add search bar at the top with placeholder
        search_frame = ttk.Frame(content_frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        # Variables to track checkbox states
        column_vars = {}
        column_checkboxes = {}
        visible_columns = set(available_columns)  # Track currently visible columns
        
        # Function to update the Select All checkbox state
        def update_select_all_state():
            if visible_columns:
                all_selected = all(column_vars[col].get() for col in visible_columns)
                select_all_var.set(all_selected)
        
        # Select All checkbox with better styling
        select_all_frame = ttk.Frame(content_frame)
        select_all_frame.pack(fill=tk.X, pady=5)
        
        select_all_var = tk.BooleanVar(value=True)
        
        def toggle_all():
            """Toggle all visible checkboxes based on Select All state."""
            state = select_all_var.get()
            for col in visible_columns:
                column_vars[col].set(state)
        
        select_all_cb = ttk.Checkbutton(
            select_all_frame, 
            text="Select All", 
            variable=select_all_var, 
            command=toggle_all,
            style="Bold.TCheckbutton"
        )
        select_all_cb.pack(side=tk.LEFT)
        
        # Add column count indicator
        column_count_var = tk.StringVar(value=f"({len(available_columns)} columns)")
        ttk.Label(select_all_frame, textvariable=column_count_var).pack(side=tk.LEFT, padx=10)
        
        # Create a container for the checkboxes with improved styling
        checkbox_frame = ttk.LabelFrame(content_frame, text="Available Columns")
        checkbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        checkbox_container, scrollable_frame = create_scrollable_frame(checkbox_frame)
        checkbox_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Store reference to scrollable_frame for later use
        self.column_scrollable_frame = scrollable_frame
        
        # Create a style for the checkbuttons
        style = ttk.Style()
        style.configure("Bold.TCheckbutton", font=("Arial", 10, "bold"))
        
        # Group columns by type for better organization
        numeric_columns = []
        text_columns = []
        other_columns = []
        
        # Sort columns by type
        for column in available_columns:
            if column == 'LEDGER HEAD':
                continue  # Skip LEDGER HEAD column
                
            # Check if column contains mostly numeric values
            data = self.excel_processor.processed_data[column]
            numeric_count = sum(1 for val in data if pd.notna(val) and isinstance(val, (int, float)))
            
            if numeric_count > len(data) * 0.5:  # If more than 50% values are numeric
                numeric_columns.append(column)
            elif column.lower() in ['date', 'particular', 'particulars', 'narration', 'description']:
                text_columns.append(column)
            else:
                other_columns.append(column)
        
        # Add section headers and checkboxes
        if numeric_columns:
            ttk.Label(scrollable_frame, text="Numeric Columns", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(5, 2))
            for column in numeric_columns:
                var = tk.BooleanVar(value=True)  # Default to selected
                column_vars[column] = var
                cb = ttk.Checkbutton(scrollable_frame, text=column, variable=var)
                cb.pack(anchor=tk.W, padx=15, pady=2)
                column_checkboxes[column] = cb
        
        if text_columns:
            ttk.Label(scrollable_frame, text="Text Columns", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(10, 2))
            for column in text_columns:
                var = tk.BooleanVar(value=False)  # Default to not selected for text columns
                column_vars[column] = var
                cb = ttk.Checkbutton(scrollable_frame, text=column, variable=var)
                cb.pack(anchor=tk.W, padx=15, pady=2)
                column_checkboxes[column] = cb
        
        if other_columns:
            ttk.Label(scrollable_frame, text="Other Columns", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(10, 2))
            for column in other_columns:
                var = tk.BooleanVar(value=True)  # Default to selected
                column_vars[column] = var
                cb = ttk.Checkbutton(scrollable_frame, text=column, variable=var)
                cb.pack(anchor=tk.W, padx=15, pady=2)
                column_checkboxes[column] = cb
        
        # Create enhanced search functionality
        def filter_columns(search_text):
            """Filter visible columns based on search text with improved matching."""
            search_text = search_text.lower().strip()
            visible_count = 0
            visible_columns.clear()
            
            # If search is empty, show all columns
            if not search_text:
                for column, cb in column_checkboxes.items():
                    cb.pack(anchor=tk.W, padx=15, pady=2)
                    visible_count += 1
                    visible_columns.add(column)
            else:
                # First hide all section headers
                for widget in scrollable_frame.winfo_children():
                    if isinstance(widget, ttk.Label):
                        widget.pack_forget()
                
                # Then show only matching columns
                for column, cb in column_checkboxes.items():
                    # More flexible matching - check if search text is contained in column name
                    # or if column name starts with search text
                    col_lower = column.lower()
                    if search_text in col_lower or col_lower.startswith(search_text):
                        cb.pack(anchor=tk.W, padx=15, pady=2)
                        visible_count += 1
                        visible_columns.add(column)
                    else:
                        cb.pack_forget()
            
            # Update column count indicator
            column_count_var.set(f"({visible_count} columns visible)")
            
            # Update select all checkbox based on visible checkboxes
            update_select_all_state()
            
            # Reset scroll position to top to show the search results
            self.root.after(50, lambda: scrollable_frame.reset_scroll())
            
            # Force update to ensure UI reflects changes immediately
            scrollable_frame.update_idletasks()
        
        # Add enhanced search bar at the top
        create_search_bar(search_frame, filter_columns, "Search columns...")
        
        # Buttons frame at the bottom
        button_frame = ttk.Frame(dialog, padding="10")
        button_frame.pack(fill=tk.X, pady=10)
        
        # Cancel button
        ttk.Button(
            button_frame, 
            text="Cancel", 
            command=dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        # Process button
        def process_selected_columns():
            """Process LEDGER HEAD for selected columns with progress indication."""
            selected_columns = [col for col, var in column_vars.items() if var.get()]
            
            if not selected_columns:
                messagebox.showinfo("Info", "No columns selected")
                return
            
            # Show processing indicator
            self.status_var.set("Processing LEDGER HEAD...")
            self.root.update_idletasks()
            
            # Process the data
            success = self.excel_processor.process_ledger_head(selected_columns)
            
            if success:
                self._update_preview()
                self.status_var.set(f"Processed LEDGER HEAD based on {len(selected_columns)} columns")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to process LEDGER HEAD")
                self.status_var.set("Error processing LEDGER HEAD")
        
        ttk.Button(
            button_frame, 
            text="Process", 
            command=process_selected_columns
        ).pack(side=tk.RIGHT, padx=5)
    
    def _update_preview(self):
        """Update the data preview table with improved display."""
        # Clear existing preview
        for widget in self.preview_container.winfo_children():
            widget.destroy()
        
        # Get preview data
        preview_data = self.excel_processor.get_preview_data(rows=PREVIEW_ROWS)
        
        if preview_data.empty:
            self.preview_info_var.set("No data to preview")
            self.status_var.set("No data to preview")
            return
        
        # Update preview info
        total_rows = len(self.excel_processor.processed_data)
        header_count = len(self.excel_processor.header_rows)
        footer_count = len(self.excel_processor.footer_rows)
        
        # Add information about detected header row
        header_info = ""
        if self.excel_processor._header_row_index >= 0:
            header_info = f" (Main header row: {self.excel_processor._header_row_index+1})"
        
        self.preview_info_var.set(
            f"Showing {min(PREVIEW_ROWS, total_rows)} of {total_rows} data rows. " 
            f"Detected {header_count} header rows{header_info} and {footer_count} footer rows."
        )
        
        # Create new table with improved display
        self.preview_table = create_data_table(self.preview_container, preview_data)
        self.preview_table.pack(fill=tk.BOTH, expand=True)
    
    def _show_help_dialog(self):
        """Show help dialog with user instructions and troubleshooting information."""
        # Create dialog window
        help_dialog = tk.Toplevel(self.root)
        help_dialog.title("Excel Processor Help")
        help_dialog.geometry("700x600")
        help_dialog.minsize(600, 500)
        help_dialog.transient(self.root)
        help_dialog.grab_set()
        
        # Create notebook for tabbed help sections
        notebook = ttk.Notebook(help_dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        overview_tab = ttk.Frame(notebook, padding=15)
        workflow_tab = ttk.Frame(notebook, padding=15)
        columns_tab = ttk.Frame(notebook, padding=15)
        errors_tab = ttk.Frame(notebook, padding=15)
        
        notebook.add(overview_tab, text="Overview")
        notebook.add(workflow_tab, text="Workflow Steps")
        notebook.add(columns_tab, text="Column Information")
        notebook.add(errors_tab, text="Troubleshooting")
        
        # Overview Tab Content
        ttk.Label(overview_tab, text="Tally Data Processor", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        overview_text = (
            "This application helps you process Excel files containing financial data. "
            "It automatically detects header rows, allows you to add specific columns, "
            "and can populate the LEDGER HEAD column based on numeric values in other columns.\n\n"
            "Key Features:\n"
            "• Automatic detection of PR sheets and header rows\n"
            "• Adding custom columns (LEDGER HEAD, TAXABLE VALUE, etc.)\n"
            "• Processing LEDGER HEAD based on numeric values\n"
            "• Preview of data before saving\n"
            "• Saving processed data to a new Excel file"
        )
        
        overview_label = ttk.Label(
            overview_tab, 
            text=overview_text, 
            wraplength=650, 
            justify=tk.LEFT
        )
        overview_label.pack(fill=tk.BOTH, expand=True)
        
        # Workflow Tab Content
        ttk.Label(workflow_tab, text="Step-by-Step Workflow", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        workflow_text = (
            "1. Upload File\n"
            "   • Click 'Upload File' and select an Excel file (.xlsx or .xls)\n"
            "   • The application will automatically detect sheets with 'PR' in the name\n"
            "   • Header and footer rows will be identified automatically\n\n"
            
            "2. Add Columns\n"
            "   • Click 'Add Columns' to open the column selection dialog\n"
            "   • Select which columns to add (LEDGER HEAD, TAXABLE VALUE, etc.)\n"
            "   • Click 'Add' to add the selected columns to your data\n\n"
            
            "3. Process LEDGER HEAD\n"
            "   • Click 'Process LEDGER HEAD' to open the processing dialog\n"
            "   • Select which columns to analyze for numeric values\n"
            "   • Use the search bar to filter columns if needed\n"
            "   • Click 'Process' to populate the LEDGER HEAD column\n\n"
            
            "4. Save Output\n"
            "   • Click 'Save Output' to save the processed data\n"
            "   • Choose a location and filename for the output file\n"
            "   • The processed data will be saved with the proper column structure"
        )
        
        # Create scrollable frame for workflow text
        workflow_container, workflow_frame = create_scrollable_frame(workflow_tab)
        workflow_container.pack(fill=tk.BOTH, expand=True)
        
        workflow_label = ttk.Label(
            workflow_frame, 
            text=workflow_text, 
            wraplength=650, 
            justify=tk.LEFT
        )
        workflow_label.pack(fill=tk.BOTH, expand=True, anchor=tk.W)
        
        # Columns Tab Content
        ttk.Label(columns_tab, text="Column Information", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        columns_text = (
            "Required Columns:\n"
            "The application works with any Excel sheet structure, but it's designed to work best "
            "with financial data that includes these common columns:\n\n"
            
            "• Date - Transaction dates\n"
            "• Particular/Particulars - Transaction descriptions\n"
            "• Voucher/Voucher No - Reference numbers\n"
            "• Debit/Credit - Transaction amounts\n"
            "• Amount - Transaction values\n\n"
            
            "Added Columns:\n"
            "The following columns can be added through the 'Add Columns' feature:\n\n"
            
            "• LEDGER HEAD - Will be populated based on which columns contain numeric values\n"
            "• TAXABLE VALUE - For tax-related calculations\n"
            "• CGST - Central Goods and Services Tax\n"
            "• SGST - State Goods and Services Tax\n"
            "• IGST - Integrated Goods and Services Tax\n\n"
            
            "LEDGER HEAD Processing:\n"
            "When processing the LEDGER HEAD column, the application will:\n"
            "1. Analyze each row in the selected columns\n"
            "2. Identify cells with numeric values (excluding 0 and empty cells)\n"
            "3. Populate the LEDGER HEAD column with the names of columns containing numeric values\n"
            "4. If multiple columns have numeric values, they will be concatenated with '+'"
        )
        
        # Create scrollable frame for columns text
        columns_container, columns_frame = create_scrollable_frame(columns_tab)
        columns_container.pack(fill=tk.BOTH, expand=True)
        
        columns_label = ttk.Label(
            columns_frame, 
            text=columns_text, 
            wraplength=650, 
            justify=tk.LEFT
        )
        columns_label.pack(fill=tk.BOTH, expand=True, anchor=tk.W)
        
        # Errors Tab Content
        ttk.Label(errors_tab, text="Troubleshooting", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        errors_text = (
            "Common Issues and Solutions:\n\n"
            
            "1. File Loading Issues\n"
            "   • Ensure the file is a valid Excel file (.xlsx or .xls)\n"
            "   • Check if the file is open in another application\n"
            "   • Verify the file is not corrupted\n\n"
            
            "2. Header Detection Problems\n"
            "   • If headers are not correctly detected, check if your Excel sheet has clear column headers\n"
            "   • Headers are detected based on common column names like 'Date', 'Particular', 'Voucher'\n"
            "   • The application looks for rows with multiple text cells that match common header patterns\n\n"
            
            "3. LEDGER HEAD Processing Issues\n"
            "   • Ensure the 'LEDGER HEAD' column has been added before processing\n"
            "   • Verify that the columns you selected for processing contain numeric values\n"
            "   • Check that the numeric values are properly formatted in Excel\n\n"
            
            "4. Search Functionality\n"
            "   • If search results don't appear, try scrolling up to see the results\n"
            "   • Clear the search and try again with different terms\n"
            "   • Make sure you're using simple search terms that match part of the column names\n\n"
            
            "5. Saving Output\n"
            "   • Ensure you have write permissions for the selected output location\n"
            "   • If the file is in use by another application, close it before saving\n"
            "   • Check that there's enough disk space available\n\n"
            
            "If you encounter persistent issues, try restarting the application or checking your Excel file format."
        )
        
        # Create scrollable frame for errors text
        errors_container, errors_frame = create_scrollable_frame(errors_tab)
        errors_container.pack(fill=tk.BOTH, expand=True)
        
        errors_label = ttk.Label(
            errors_frame, 
            text=errors_text, 
            wraplength=650, 
            justify=tk.LEFT
        )
        errors_label.pack(fill=tk.BOTH, expand=True, anchor=tk.W)
        
        # Close button
        close_btn = ttk.Button(help_dialog, text="Close", command=help_dialog.destroy)
        close_btn.pack(pady=10)
        
    def _save_output(self):
        """Handle save output button click."""
        if self.excel_processor.processed_data is None:
            messagebox.showinfo("Info", "Please upload and process a file first")
            return
        
        # Get original file name and directory
        original_path = self.file_path_var.get()
        original_dir = os.path.dirname(original_path)
        original_filename = os.path.basename(original_path)
        name, ext = os.path.splitext(original_filename)
        
        # Suggest output file name
        suggested_filename = f"{name}_processed{ext}"
        suggested_path = os.path.join(original_dir, suggested_filename)
        
        # Show save dialog
        output_path = filedialog.asksaveasfilename(
            title="Save Processed File",
            initialdir=original_dir,
            initialfile=suggested_filename,
            filetypes=EXCEL_FILE_TYPES,
            defaultextension=".xlsx"
        )
        
        if not output_path:
            return
        
        self.status_var.set("Saving file...")
        self.root.update_idletasks()
        
        success, message = self.excel_processor.save_to_file(output_path)
        
        if success:
            messagebox.showinfo("Success", message)
            self.status_var.set(message)
        else:
            messagebox.showerror("Error", message)
            self.status_var.set("Error saving file")