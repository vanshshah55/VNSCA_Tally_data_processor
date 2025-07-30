#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration settings for the Excel Processing Application.
Contains constants and settings used throughout the application.
"""

# Sheet identification
PR_SHEET_IDENTIFIER = "PR"

# Column names that can be added
ADDABLE_COLUMNS = [
    'LEDGER HEAD',
    'TAXABLE VALUE',
    'CGST',
    'SGST',
    'IGST'
]

# Footer detection keywords
FOOTER_KEYWORDS = [
    'total',
    'summary',
    'sum',
    'grand',
    'subtotal',
    'balance',
    'closing',
    'net',
    'amount'
]

# Common column header names for detecting the start of data
COMMON_HEADER_NAMES = [
    'date', 'particular', 'particulars', 'voucher', 'vch', 'vch no', 'voucher no',
    'debit', 'credit', 'amount', 'dr', 'cr', 'balance',
    'narration', 'description', 'details', 'account', 'account name', 
    'reference', 'ref', 'ref no', 'transaction', 'trans',
    'invoice', 'inv', 'inv no', 'bill', 'bill no', 'receipt', 'receipt no',
    'payment', 'cheque', 'chq', 'chq no', 'bank', 'ledger'
]

# GUI settings
WINDOW_TITLE = "Excel Processor"
WINDOW_SIZE = "1000x600"
PREVIEW_ROWS = 10

# File types for file dialogs
EXCEL_FILE_TYPES = [
    ("Excel files", "*.xlsx *.xls"),
    ("All files", "*.*")
]