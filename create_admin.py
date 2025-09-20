#!/usr/bin/env python3
"""
Create admin user for AI Artisan Marketplace
"""

import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin():
    """Create admin user"""
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    # Check if admin already exists
    cursor.execute('SELECT id FROM admins WHERE username = ?', ('admin',))
    if cursor.fetchone():
        print("Admin user already exists!")
        conn.close()
        return
    
    # Create admin user
    cursor.execute('''
        INSERT INTO admins (username, email, password, name)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin@artisanmarketplace.com', hash_password('admin123'), 'Administrator'))
    
    conn.commit()
    conn.close()
    
    print("Admin user created successfully!")
    print("Username: admin")
    print("Password: admin123")
    print("Email: admin@artisanmarketplace.com")

if __name__ == "__main__":
    create_admin()
