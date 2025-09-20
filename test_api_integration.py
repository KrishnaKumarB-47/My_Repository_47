#!/usr/bin/env python3
"""
Test Google Cloud API integration status
"""

import os
from gcp_services import gcp_services

def test_api_status():
    """Test the current API integration status"""
    print("🔍 Google Cloud API Integration Status")
    print("=" * 50)
    
    # Check if GCP libraries are installed
    try:
        from google.cloud import translate_v2 as translate
        from google.cloud import aiplatform
        print("✅ Google Cloud libraries are installed")
    except ImportError as e:
        print("❌ Google Cloud libraries NOT installed")
        print(f"   Error: {e}")
        print("   Run: pip install google-cloud-translate google-cloud-aiplatform")
        return False
    
    # Check configuration
    print(f"\n📋 Configuration:")
    print(f"   Project ID: {gcp_services.project_id}")
    print(f"   Region: {gcp_services.region}")
    print(f"   Credentials: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'Not set')}")
    
    # Check if GCP services are available
    if gcp_services.is_gcp_available():
        print("✅ GCP services are available and initialized")
        
        # Test Translation API
        print("\n🌐 Testing Translation API...")
        try:
            result = gcp_services.translate_text("Hello, world!", "hi")
            if "[Translated to" in result:
                print("⚠️  Translation API using MOCK service")
            else:
                print("✅ Translation API working with real Google Cloud")
                print(f"   Result: {result}")
        except Exception as e:
            print(f"❌ Translation API error: {e}")
        
        # Test Vertex AI
        print("\n🤖 Testing Vertex AI...")
        try:
            result = gcp_services.generate_ai_story("A beautiful handmade vase", "pottery", "Test Artisan")
            if "Crafted by the skilled hands" in result:
                print("⚠️  Vertex AI using MOCK service")
            else:
                print("✅ Vertex AI working with real Google Cloud")
                print(f"   Result: {result[:100]}...")
        except Exception as e:
            print(f"❌ Vertex AI error: {e}")
            
    else:
        print("❌ GCP services are NOT available")
        print("   Reasons could be:")
        print("   1. Project ID not set (still 'your-project-id')")
        print("   2. Service account credentials not configured")
        print("   3. APIs not enabled in Google Cloud Console")
        print("   4. Billing not enabled")
    
    print("\n" + "=" * 50)
    print("📖 To enable real APIs, follow the GCP_SETUP.md guide")
    return gcp_services.is_gcp_available()

if __name__ == "__main__":
    test_api_status()
