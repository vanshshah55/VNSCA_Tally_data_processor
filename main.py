#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the Tally Ledger Head Processor Application.
This module initializes and launches the application GUI.
"""

import tkinter as tk
import os
import sys
from gui import AppGUI
from expiration_check import should_disable_functionality, get_expiration_status

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    """Initialize and launch the application."""
    root = tk.Tk()
    root.title("Tally Ledger Head Processor")
    root.geometry("1000x600")
    
    # Set application icon if available
    try:
        icon_path = resource_path("tally_lh_processor.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception:
        pass  # Ignore icon errors
    
    app = AppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()