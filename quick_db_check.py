#!/usr/bin/env python3
"""
Quick database check
"""

import sqlite3

def quick_check():
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    print("📊 DATABASE QUICK CHECK")
    print("=" * 50)
    
    # Count users
    cursor.execute('SELECT COUNT(*) FROM artisans')
    artisan_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM buyers')
    buyer_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM admins')
    admin_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM products')
    product_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM cart')
    cart_count = cursor.fetchone()[0]
    
    print(f"👥 Users:")
    print(f"   Artisans: {artisan_count}")
    print(f"   Buyers: {buyer_count}")
    print(f"   Admins: {admin_count}")
    print(f"   Total: {artisan_count + buyer_count + admin_count}")
    
    print(f"\n📦 Products: {product_count}")
    print(f"🛒 Cart items: {cart_count}")
    
    # Show sample users
    print(f"\n🔨 Sample Artisans:")
    cursor.execute('SELECT id, username, name, email FROM artisans LIMIT 5')
    artisans = cursor.fetchall()
    for artisan in artisans:
        print(f"   {artisan[0]}: {artisan[1]} ({artisan[2]}) - {artisan[3]}")
    
    print(f"\n🛒 Sample Buyers:")
    cursor.execute('SELECT id, username, name, email FROM buyers LIMIT 5')
    buyers = cursor.fetchall()
    for buyer in buyers:
        print(f"   {buyer[0]}: {buyer[1]} ({buyer[2]}) - {buyer[3]}")
    
    print(f"\n👑 Admins:")
    cursor.execute('SELECT id, username, name, email FROM admins')
    admins = cursor.fetchall()
    for admin in admins:
        print(f"   {admin[0]}: {admin[1]} ({admin[2]}) - {admin[3]}")
    
    # Check products with images
    cursor.execute('SELECT COUNT(*) FROM products WHERE image_path IS NOT NULL')
    products_with_images = cursor.fetchone()[0]
    
    print(f"\n📸 Products with images: {products_with_images}/{product_count}")
    
    conn.close()

if __name__ == "__main__":
    quick_check()
