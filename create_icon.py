#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create a simple icon for the Tally_LH_Processor application.
This script generates a basic icon file that can be used with PyInstaller.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple icon for the application."""
    # Create a new image with a white background
    icon_size = 256
    img = Image.new('RGBA', (icon_size, icon_size), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a rounded rectangle as background with green color
    draw.rectangle([(20, 20), (icon_size-20, icon_size-20)], 
                   fill=(46, 204, 113, 255), outline=(39, 174, 96, 255), width=4)
    
    # Add text
    try:
        # Try to use a nice font if available
        font = ImageFont.truetype("arial.ttf", 48)
    except IOError:
        # Fall back to default font
        font = ImageFont.load_default()
    
    draw.text((icon_size//2, icon_size//2-10), "TLP", fill=(255, 255, 255, 255), 
              font=font, anchor="mm")
    
    # Add a smaller text below
    try:
        small_font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        small_font = ImageFont.load_default()
    
    draw.text((icon_size//2, icon_size//2+40), "Tally Ledger Processor", 
              fill=(255, 255, 255, 255), font=small_font, anchor="mm")
    
    # Save as .ico file
    img.save("tally_lh_processor.ico", format="ICO")
    
    print(f"Icon created: {os.path.abspath('tally_lh_processor.ico')}")

if __name__ == "__main__":
    create_icon()