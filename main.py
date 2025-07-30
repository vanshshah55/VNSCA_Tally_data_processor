#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the Excel Processing Application.
This module initializes and launches the application GUI.
"""

import tkinter as tk
from gui import AppGUI

def main():
    """Initialize and launch the application."""
    root = tk.Tk()
    root.title("Excel Processor")
    root.geometry("1000x600")
    app = AppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()