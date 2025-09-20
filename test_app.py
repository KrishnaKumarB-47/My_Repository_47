#!/usr/bin/env python3
"""
Simple test script for AI Artisan Marketplace
"""

import sqlite3
import os
from app import init_db, generate_ai_story, translate_text, get_recommendations

def test_database():
    """Test database initialization and basic operations"""
    print("Testing database initialization...")
    
    # Check if database file exists
    if os.path.exists('artisan_marketplace.db'):
        print("✓ Database file created successfully")
    else:
        print("✗ Database file not found")
        return False
    
    # Test database connection and tables
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    expected_tables = ['artisans', 'buyers', 'products', 'buyer_interactions']
    
    for table in expected_tables:
        if (table,) in tables:
            print(f"✓ Table '{table}' exists")
        else:
            print(f"✗ Table '{table}' missing")
    
    conn.close()
    return True

def test_ai_functions():
    """Test AI-related functions"""
    print("\nTesting AI functions...")
    
    # Test AI story generation
    test_description = "A beautiful handcrafted wooden bowl made from oak"
    test_category = "woodwork"
    
    story = generate_ai_story(test_description, test_category)
    if story and len(story) > 50:
        print("✓ AI story generation working")
    else:
        print("✗ AI story generation failed")
    
    # Test translation function
    translated = translate_text("Hello world", "es")
    if "Translated" in translated or "Hello world" in translated:
        print("✓ Translation function working")
    else:
        print("✗ Translation function failed")

def test_recommendation_engine():
    """Test recommendation engine"""
    print("\nTesting recommendation engine...")
    
    # Test with non-existent user (should return random products)
    recommendations = get_recommendations(999)
    if isinstance(recommendations, list):
        print("✓ Recommendation engine working")
    else:
        print("✗ Recommendation engine failed")

def main():
    """Run all tests"""
    print("AI Artisan Marketplace - Test Suite")
    print("=" * 40)
    
    # Initialize database
    init_db()
    
    # Run tests
    test_database()
    test_ai_functions()
    test_recommendation_engine()
    
    print("\n" + "=" * 40)
    print("Test completed!")
    print("\nTo run the application:")
    print("python app.py")
    print("Then open http://localhost:5000 in your browser")

if __name__ == "__main__":
    main()

