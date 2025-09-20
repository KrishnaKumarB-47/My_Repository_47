#!/usr/bin/env python3
"""
Demo data script for AI Artisan Marketplace
Adds sample artisans, buyers, and products for testing
"""

import sqlite3
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_demo_data():
    """Add demo data to the database"""
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    # Add sample artisans
    artisans = [
        ('john_artisan', 'john@example.com', hash_password('password123'), 'John Smith', 'New York, USA', 'en'),
        ('maria_craft', 'maria@example.com', hash_password('password123'), 'Maria Garcia', 'Barcelona, Spain', 'es'),
        ('akira_wood', 'akira@example.com', hash_password('password123'), 'Akira Tanaka', 'Tokyo, Japan', 'ja'),
        ('sophie_pottery', 'sophie@example.com', hash_password('password123'), 'Sophie Dubois', 'Paris, France', 'fr')
    ]
    
    for artisan in artisans:
        try:
            cursor.execute('''
                INSERT INTO artisans (username, email, password, name, location, language)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', artisan)
        except sqlite3.IntegrityError:
            pass  # Skip if already exists
    
    # Add sample buyers
    buyers = [
        ('alice_buyer', 'alice@example.com', hash_password('password123'), 'Alice Johnson', 'jewelry, pottery, textiles'),
        ('bob_shopper', 'bob@example.com', hash_password('password123'), 'Bob Wilson', 'woodwork, handicraft'),
        ('charlie_collector', 'charlie@example.com', hash_password('password123'), 'Charlie Brown', 'all categories')
    ]
    
    for buyer in buyers:
        try:
            cursor.execute('''
                INSERT INTO buyers (username, email, password, name, preferences)
                VALUES (?, ?, ?, ?, ?)
            ''', buyer)
        except sqlite3.IntegrityError:
            pass  # Skip if already exists
    
    # Get artisan IDs
    cursor.execute('SELECT id, name FROM artisans')
    artisan_data = cursor.fetchall()
    artisan_map = {name: id for id, name in artisan_data}
    
    # Add sample products (prices in INR)
    products = [
        (artisan_map.get('John Smith', 1), 'Handcrafted Oak Bowl', 
         'A beautiful handcrafted wooden bowl made from premium oak wood. Each piece is unique and finished with natural beeswax.', 
         'woodwork', 3817.17, 'en'),  # $45.99 * 83
        (artisan_map.get('Maria Garcia', 2), 'Ceramic Vase Collection', 
         'A stunning collection of ceramic vases inspired by traditional Spanish pottery. Each vase is hand-painted with intricate patterns.', 
         'pottery', 7469.17, 'es'),  # $89.99 * 83
        (artisan_map.get('Akira Tanaka', 3), 'Silk Kimono Scarf', 
         'Elegant silk scarf featuring traditional Japanese motifs. Made from 100% pure silk with hand-dyed patterns.', 
         'textile', 10375.00, 'ja'),  # $125.00 * 83
        (artisan_map.get('Sophie Dubois', 4), 'Silver Pendant Necklace', 
         'Delicate silver pendant necklace with hand-engraved floral design. Comes with a matching chain and gift box.', 
         'jewelry', 6266.50, 'fr'),  # $75.50 * 83
        (artisan_map.get('John Smith', 1), 'Rustic Wooden Clock', 
         'Unique wooden wall clock made from reclaimed barn wood. Features a minimalist design with Roman numerals.', 
         'woodwork', 5395.00, 'en'),  # $65.00 * 83
        (artisan_map.get('Maria Garcia', 2), 'Handwoven Tapestry', 
         'Colorful handwoven tapestry depicting Spanish countryside scenes. Made using traditional weaving techniques.', 
         'textile', 12450.00, 'es'),  # $150.00 * 83
        (artisan_map.get('Akira Tanaka', 3), 'Bamboo Tea Set', 
         'Complete bamboo tea set including teapot, cups, and serving tray. Perfect for traditional Japanese tea ceremonies.', 
         'handicraft', 7885.00, 'ja'),  # $95.00 * 83
        (artisan_map.get('Sophie Dubois', 4), 'Ceramic Dinnerware Set', 
         'Elegant ceramic dinnerware set for four people. Features a modern design with subtle French-inspired patterns.', 
         'pottery', 9960.00, 'fr')  # $120.00 * 83
    ]
    
    for product in products:
        try:
            cursor.execute('''
                INSERT INTO products (artisan_id, name, description, category, price, language)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', product)
        except sqlite3.IntegrityError:
            pass  # Skip if already exists
    
    # Add some buyer interactions for recommendations
    cursor.execute('SELECT id FROM buyers LIMIT 1')
    buyer_id = cursor.fetchone()[0]
    
    cursor.execute('SELECT id FROM products LIMIT 3')
    product_ids = [row[0] for row in cursor.fetchall()]
    
    for product_id in product_ids:
        try:
            cursor.execute('''
                INSERT INTO buyer_interactions (buyer_id, product_id, interaction_type)
                VALUES (?, ?, ?)
            ''', (buyer_id, product_id, 'view'))
        except sqlite3.IntegrityError:
            pass  # Skip if already exists
    
    conn.commit()
    conn.close()
    
    print("Demo data added successfully!")
    print("\nSample accounts created:")
    print("Artisans:")
    print("- john_artisan / password123")
    print("- maria_craft / password123")
    print("- akira_wood / password123")
    print("- sophie_pottery / password123")
    print("\nBuyers:")
    print("- alice_buyer / password123")
    print("- bob_shopper / password123")
    print("- charlie_collector / password123")

if __name__ == "__main__":
    add_demo_data()

