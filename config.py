import os

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
except ImportError:
    print("Warning: python-dotenv not installed. Using system environment variables only.")

class Config:
    # Google Cloud Configuration
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'your-project-id')
    GCP_REGION_MUMBAI = 'asia-south1'
    GCP_REGION_DELHI = 'asia-south2'
    
    # Default region (Mumbai)
    GCP_DEFAULT_REGION = GCP_REGION_MUMBAI
    
    # Service account key path
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # Upload configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Currency configuration
    CURRENCY_SYMBOL = '₹'
    CURRENCY_CODE = 'INR'
    
    # Translation API configuration
    TRANSLATION_MODEL = 'neural-machine-translation'
    
    # Vertex AI configuration
    VERTEX_AI_MODEL_NAME = 'text-bison@001'  # For text generation
    VERTEX_AI_ENDPOINT = None  # Will be set dynamically
    
    # Gemini AI configuration (for chatbot)
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL_NAME = 'gemini-pro'