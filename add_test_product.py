#!/usr/bin/env python3
"""
Add a test product with image to verify image display
"""

import sqlite3
import os
from datetime import datetime

def add_test_product():
    """Add a test product with image"""
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    # Get first artisan ID
    cursor.execute('SELECT id FROM artisans LIMIT 1')
    artisan_id = cursor.fetchone()[0]
    
    # Create a test image file (placeholder)
    test_image_path = 'static/uploads/test_product.jpg'
    
    # Create a simple test image (1x1 pixel JPEG)
    test_image_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
    
    with open(test_image_path, 'wb') as f:
        f.write(test_image_data)
    
    # Add test product
    cursor.execute('''
        INSERT INTO products (artisan_id, name, description, category, price, ai_story, language, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (artisan_id, 'Test Product with Image', 
          'This is a test product to verify image display functionality.', 
          'handicraft', 1000.00, 
          'This is a test AI story for the test product.', 
          'en', 'test_product.jpg'))
    
    conn.commit()
    conn.close()
    
    print("✅ Test product with image added successfully!")
    print(f"   Image saved to: {test_image_path}")
    print("   Product ID: Check database for the new product")

if __name__ == "__main__":
    add_test_product()
