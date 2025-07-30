#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions for the Excel Processing Application.
Contains helper functions used across the application.
"""

import pandas as pd
import tkinter as tk
from tkinter import ttk

def create_scrollable_frame(parent):
    """
    Create a scrollable frame widget with both horizontal and vertical scrollbars.
    
    Args:
        parent: Parent widget
        
    Returns:
        tuple: (container_frame, scrollable_frame, canvas)
    """
    # Create a container frame with scrollbars
    container = ttk.Frame(parent)
    
    # Create canvas with scrollbars
    canvas = tk.Canvas(container)
    scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
    
    # Create a frame inside the canvas for content
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    # Add mousewheel scrolling
    def _on_mousewheel(event):
        # Respond to Linux or Windows wheel event
        if event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")
    
    # Bind mousewheel events
    canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows
    canvas.bind_all("<Button-4>", _on_mousewheel)    # Linux scroll up
    canvas.bind_all("<Button-5>", _on_mousewheel)    # Linux scroll down
    
    # Place the frame in the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    
    # Grid layout for proper scrollbar placement
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")
    
    # Configure grid weights
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    
    # Method to reset scroll position to top
    def reset_scroll():
        canvas.yview_moveto(0.0)
    
    # Attach the method to the scrollable_frame
    scrollable_frame.reset_scroll = reset_scroll
    
    return container, scrollable_frame

def create_data_table(parent, dataframe):
    """
    Create a table widget to display DataFrame data with proper scrollbars.
    
    Args:
        parent: Parent widget
        dataframe: Pandas DataFrame to display
        
    Returns:
        ttk.Frame: Frame containing the table and scrollbars
    """
    # Create a frame to hold the table and scrollbars
    frame = ttk.Frame(parent)
    
    # Create Treeview widget
    columns = list(dataframe.columns)
    table = ttk.Treeview(frame, columns=columns, show='headings')
    
    # Add vertical and horizontal scrollbars
    vsb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=table.xview)
    table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # Configure columns and headings with better width calculation
    for col in columns:
        table.heading(col, text=col)
        
        # Calculate width based on column name and data
        if len(dataframe) > 0:
            # Get maximum string length in this column (including header)
            col_values = dataframe[col].astype(str)
            max_len = max(len(str(col)), col_values.str.len().max())
            
            # Adjust width based on content type
            if dataframe[col].dtype in [int, float, bool]:
                char_width = 8  # Narrower for numeric columns
            else:
                char_width = 10  # Wider for text columns
                
            width = min(max(max_len * char_width, 80), 300)  # Between 80 and 300 pixels
        else:
            width = max(len(str(col)) * 10, 80)  # Default width if no data
            
        table.column(col, width=width, minwidth=50)
    
    # Insert data rows with row numbers
    for i, row in dataframe.iterrows():
        values = [row[col] if pd.notna(row[col]) else "" for col in columns]
        table.insert('', 'end', text=str(i+1), values=values, tags=('row',))
    
    # Add alternating row colors
    table.tag_configure('row', background='#f0f0f0')
    for i, item in enumerate(table.get_children()):
        if i % 2 == 0:
            table.item(item, tags=('even',))
        else:
            table.item(item, tags=('odd',))
    table.tag_configure('even', background='#f0f0f0')
    table.tag_configure('odd', background='#ffffff')
    
    # Grid layout
    table.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')
    
    # Configure grid weights
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    return frame

def create_search_bar(parent, callback, placeholder="Search..."):
    """
    Create an enhanced search bar widget with live filtering and placeholder text.
    
    Args:
        parent: Parent widget
        callback: Function to call when search text changes
        placeholder: Placeholder text to show when search bar is empty
        
    Returns:
        ttk.Entry: Search entry widget
    """
    frame = ttk.Frame(parent)
    
    # Search label with icon (using text symbol as icon)
    search_label = ttk.Label(frame, text="🔍", font=("Arial", 12))
    search_label.pack(side=tk.LEFT, padx=5)
    
    # Search entry with placeholder functionality
    search_var = tk.StringVar()
    search_entry = ttk.Entry(frame, textvariable=search_var, width=25)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    # Placeholder functionality
    search_entry.insert(0, placeholder)
    search_entry.config(foreground="gray")
    
    def on_focus_in(event):
        if search_entry.get() == placeholder:
            search_entry.delete(0, tk.END)
            search_entry.config(foreground="black")
    
    def on_focus_out(event):
        if not search_entry.get():
            search_entry.insert(0, placeholder)
            search_entry.config(foreground="gray")
            callback("")  # Clear search when returning to placeholder
    
    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)
    
    # Clear button
    def clear_search():
        search_entry.delete(0, tk.END)
        search_entry.focus_set()  # Keep focus in the search box
        callback("")  # Trigger search update with empty string
    
    clear_btn = ttk.Button(frame, text="✕", width=3, command=clear_search)
    clear_btn.pack(side=tk.RIGHT, padx=5)
    
    # Bind callback to search variable - with debounce effect
    def on_search_change(*args):
        # Get the current text
        text = search_var.get()
        # Only trigger callback if not showing placeholder
        if text != placeholder:
            callback(text)
    
    search_var.trace_add("write", on_search_change)
    
    frame.pack(fill=tk.X, padx=10, pady=5)
    return search_entry