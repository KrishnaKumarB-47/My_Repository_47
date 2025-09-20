#!/usr/bin/env python3
"""
Database Viewer and Management Tool for AI Artisan Marketplace
"""

import sqlite3
import os
from datetime import datetime

def connect_db():
    """Connect to the database"""
    return sqlite3.connect('artisan_marketplace.db')

def view_all_users():
    """View all users in the database"""
    conn = connect_db()
    cursor = conn.cursor()
    
    print("👥 ALL USERS IN DATABASE")
    print("=" * 80)
    
    # Get artisans
    cursor.execute('SELECT id, username, email, name, location, language, created_at FROM artisans ORDER BY created_at DESC')
    artisans = cursor.fetchall()
    
    print(f"\n🔨 ARTISANS ({len(artisans)} total):")
    print("-" * 80)
    print(f"{'ID':<3} {'Username':<15} {'Email':<25} {'Name':<20} {'Location':<15} {'Language':<8} {'Created':<12}")
    print("-" * 80)
    for artisan in artisans:
        created_date = artisan[6][:10] if artisan[6] else 'N/A'
        print(f"{artisan[0]:<3} {artisan[1]:<15} {artisan[2]:<25} {artisan[3]:<20} {artisan[4]:<15} {artisan[5]:<8} {created_date:<12}")
    
    # Get buyers
    cursor.execute('SELECT id, username, email, name, preferences, created_at FROM buyers ORDER BY created_at DESC')
    buyers = cursor.fetchall()
    
    print(f"\n🛒 BUYERS ({len(buyers)} total):")
    print("-" * 80)
    print(f"{'ID':<3} {'Username':<15} {'Email':<25} {'Name':<20} {'Preferences':<20} {'Created':<12}")
    print("-" * 80)
    for buyer in buyers:
        created_date = buyer[5][:10] if buyer[5] else 'N/A'
        preferences = buyer[4][:17] + '...' if buyer[4] and len(buyer[4]) > 20 else buyer[4] or 'None'
        print(f"{buyer[0]:<3} {buyer[1]:<15} {buyer[2]:<25} {buyer[3]:<20} {preferences:<20} {created_date:<12}")
    
    # Get admins
    cursor.execute('SELECT id, username, email, name, created_at FROM admins ORDER BY created_at DESC')
    admins = cursor.fetchall()
    
    print(f"\n👑 ADMINS ({len(admins)} total):")
    print("-" * 80)
    print(f"{'ID':<3} {'Username':<15} {'Email':<25} {'Name':<20} {'Created':<12}")
    print("-" * 80)
    for admin in admins:
        created_date = admin[4][:10] if admin[4] else 'N/A'
        print(f"{admin[0]:<3} {admin[1]:<15} {admin[2]:<25} {admin[3]:<20} {created_date:<12}")
    
    conn.close()

def view_products():
    """View all products in the database"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.id, p.name, p.price, p.category, p.image_path, a.name as artisan_name, p.created_at
        FROM products p
        JOIN artisans a ON p.artisan_id = a.id
        ORDER BY p.created_at DESC
    ''')
    products = cursor.fetchall()
    
    print(f"\n📦 PRODUCTS ({len(products)} total):")
    print("-" * 100)
    print(f"{'ID':<3} {'Name':<25} {'Price':<10} {'Category':<12} {'Image':<20} {'Artisan':<15} {'Created':<12}")
    print("-" * 100)
    for product in products:
        created_date = product[6][:10] if product[6] else 'N/A'
        image_status = "✅ Yes" if product[4] else "❌ No"
        print(f"{product[0]:<3} {product[1][:24]:<25} ₹{product[2]:<9} {product[3]:<12} {image_status:<20} {product[5]:<15} {created_date:<12}")
    
    conn.close()

def view_cart_items():
    """View all cart items"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.id, b.username, p.name, c.quantity, c.added_at
        FROM cart c
        JOIN buyers b ON c.buyer_id = b.id
        JOIN products p ON c.product_id = p.id
        ORDER BY c.added_at DESC
    ''')
    cart_items = cursor.fetchall()
    
    print(f"\n🛒 CART ITEMS ({len(cart_items)} total):")
    print("-" * 80)
    print(f"{'ID':<3} {'Buyer':<15} {'Product':<25} {'Qty':<5} {'Added':<12}")
    print("-" * 80)
    for item in cart_items:
        added_date = item[4][:10] if item[4] else 'N/A'
        print(f"{item[0]:<3} {item[1]:<15} {item[2][:24]:<25} {item[3]:<5} {added_date:<12}")
    
    conn.close()

def modify_user():
    """Modify user information"""
    print("\n🔧 USER MODIFICATION")
    print("=" * 50)
    
    user_type = input("Enter user type (artisan/buyer/admin): ").lower()
    user_id = input("Enter user ID: ")
    
    try:
        user_id = int(user_id)
    except ValueError:
        print("❌ Invalid user ID")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    
    if user_type == 'artisan':
        cursor.execute('SELECT * FROM artisans WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        if not user:
            print("❌ Artisan not found")
            conn.close()
            return
        
        print(f"\nCurrent artisan info: {user}")
        print("\nWhat would you like to modify?")
        print("1. Name")
        print("2. Email")
        print("3. Location")
        print("4. Language")
        print("5. Delete user")
        
        choice = input("Enter choice (1-5): ")
        
        if choice == '1':
            new_name = input("Enter new name: ")
            cursor.execute('UPDATE artisans SET name = ? WHERE id = ?', (new_name, user_id))
        elif choice == '2':
            new_email = input("Enter new email: ")
            cursor.execute('UPDATE artisans SET email = ? WHERE id = ?', (new_email, user_id))
        elif choice == '3':
            new_location = input("Enter new location: ")
            cursor.execute('UPDATE artisans SET location = ? WHERE id = ?', (new_location, user_id))
        elif choice == '4':
            new_language = input("Enter new language: ")
            cursor.execute('UPDATE artisans SET language = ? WHERE id = ?', (new_language, user_id))
        elif choice == '5':
            confirm = input("Are you sure you want to delete this user? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute('DELETE FROM artisans WHERE id = ?', (user_id,))
                print("✅ User deleted")
            else:
                print("❌ Deletion cancelled")
        else:
            print("❌ Invalid choice")
    
    elif user_type == 'buyer':
        cursor.execute('SELECT * FROM buyers WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        if not user:
            print("❌ Buyer not found")
            conn.close()
            return
        
        print(f"\nCurrent buyer info: {user}")
        print("\nWhat would you like to modify?")
        print("1. Name")
        print("2. Email")
        print("3. Preferences")
        print("4. Delete user")
        
        choice = input("Enter choice (1-4): ")
        
        if choice == '1':
            new_name = input("Enter new name: ")
            cursor.execute('UPDATE buyers SET name = ? WHERE id = ?', (new_name, user_id))
        elif choice == '2':
            new_email = input("Enter new email: ")
            cursor.execute('UPDATE buyers SET email = ? WHERE id = ?', (new_email, user_id))
        elif choice == '3':
            new_preferences = input("Enter new preferences: ")
            cursor.execute('UPDATE buyers SET preferences = ? WHERE id = ?', (new_preferences, user_id))
        elif choice == '4':
            confirm = input("Are you sure you want to delete this user? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute('DELETE FROM buyers WHERE id = ?', (user_id,))
                print("✅ User deleted")
            else:
                print("❌ Deletion cancelled")
        else:
            print("❌ Invalid choice")
    
    else:
        print("❌ Invalid user type")
        conn.close()
        return
    
    conn.commit()
    conn.close()
    print("✅ User updated successfully")

def reset_password():
    """Reset user password"""
    print("\n🔑 PASSWORD RESET")
    print("=" * 30)
    
    user_type = input("Enter user type (artisan/buyer/admin): ").lower()
    username = input("Enter username: ")
    new_password = input("Enter new password: ")
    
    import hashlib
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    
    conn = connect_db()
    cursor = conn.cursor()
    
    if user_type == 'artisan':
        cursor.execute('UPDATE artisans SET password = ? WHERE username = ?', (hashed_password, username))
    elif user_type == 'buyer':
        cursor.execute('UPDATE buyers SET password = ? WHERE username = ?', (hashed_password, username))
    elif user_type == 'admin':
        cursor.execute('UPDATE admins SET password = ? WHERE username = ?', (hashed_password, username))
    else:
        print("❌ Invalid user type")
        conn.close()
        return
    
    if cursor.rowcount > 0:
        print("✅ Password updated successfully")
    else:
        print("❌ User not found")
    
    conn.commit()
    conn.close()

def main():
    """Main menu"""
    while True:
        print("\n🗄️  DATABASE VIEWER & MANAGEMENT")
        print("=" * 40)
        print("1. View all users")
        print("2. View products")
        print("3. View cart items")
        print("4. Modify user")
        print("5. Reset password")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            view_all_users()
        elif choice == '2':
            view_products()
        elif choice == '3':
            view_cart_items()
        elif choice == '4':
            modify_user()
        elif choice == '5':
            reset_password()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
