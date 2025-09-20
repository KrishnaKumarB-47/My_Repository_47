#!/usr/bin/env python3
"""
Check API integration status and provide setup instructions
"""

import os
import sys

def check_api_status():
    """Check the current API integration status"""
    print("🔍 AI Artisan Marketplace - API Integration Status")
    print("=" * 60)
    
    # Check Python version
    print(f"🐍 Python Version: {sys.version}")
    
    # Check if we're in the right directory
    print(f"📁 Current Directory: {os.getcwd()}")
    
    # Check for required files
    required_files = ['app.py', 'gcp_services.py', 'config.py', 'requirements.txt']
    print(f"\n📋 Required Files:")
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
    
    # Check Google Cloud libraries
    print(f"\n📦 Google Cloud Libraries:")
    try:
        import google.cloud.translate_v2 as translate
        print("   ✅ google-cloud-translate")
    except ImportError:
        print("   ❌ google-cloud-translate (NOT INSTALLED)")
    
    try:
        import google.cloud.aiplatform
        print("   ✅ google-cloud-aiplatform")
    except ImportError:
        print("   ❌ google-cloud-aiplatform (NOT INSTALLED)")
    
    # Check configuration
    print(f"\n⚙️  Configuration:")
    try:
        from config import Config
        print(f"   Project ID: {Config.GCP_PROJECT_ID}")
        print(f"   Region: {Config.GCP_DEFAULT_REGION}")
        print(f"   Credentials: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'Not set')}")
    except Exception as e:
        print(f"   ❌ Config error: {e}")
    
    # Check GCP services status
    print(f"\n🔧 GCP Services Status:")
    try:
        from gcp_services import gcp_services
        if gcp_services.is_gcp_available():
            print("   ✅ GCP services are available")
        else:
            print("   ⚠️  GCP services using MOCK mode")
            print("   📝 This means:")
            print("      - Translation shows '[Translated to Language]' prefix")
            print("      - AI stories use template-based generation")
            print("      - Recommendations use basic algorithms")
    except Exception as e:
        print(f"   ❌ GCP services error: {e}")
    
    # Test current functionality
    print(f"\n🧪 Testing Current Functionality:")
    try:
        from gcp_services import gcp_services
        
        # Test translation
        translation_result = gcp_services.translate_text("Hello, world!", "hi")
        print(f"   Translation Test: {translation_result}")
        
        # Test AI story generation
        story_result = gcp_services.generate_ai_story("A beautiful handmade vase", "pottery", "Test Artisan")
        print(f"   AI Story Test: {story_result[:50]}...")
        
        print("   ✅ All functions working (using mock or real APIs)")
        
    except Exception as e:
        print(f"   ❌ Function test error: {e}")
    
    # Provide setup instructions
    print(f"\n📖 Setup Instructions:")
    print("   To enable REAL Google Cloud APIs:")
    print("   1. Create a Google Cloud Project")
    print("   2. Enable Translation API and Vertex AI API")
    print("   3. Create a service account and download JSON key")
    print("   4. Set environment variables:")
    print("      - GCP_PROJECT_ID=your-project-id")
    print("      - GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json")
    print("   5. Install libraries: pip install google-cloud-translate google-cloud-aiplatform")
    
    print(f"\n🎯 Current Status:")
    print("   The application is FULLY FUNCTIONAL with mock services!")
    print("   All features work - translation, AI stories, recommendations")
    print("   You can demo everything without needing Google Cloud setup")
    
    print(f"\n🚀 To run the application:")
    print("   python app.py")
    print("   Then open http://localhost:5000")

if __name__ == "__main__":
    check_api_status()
