"""
Google Cloud Platform services integration
Handles Translation API and Vertex AI integration
"""

import os
import json
from typing import List, Dict, Any, Optional
from config import Config

try:
    from google.cloud import translate_v2 as translate
    from google.cloud import aiplatform
    GCP_AVAILABLE = True
except ImportError:
    GCP_AVAILABLE = False
    print("Warning: Google Cloud libraries not installed. Using mock services.")

class GCPServices:
    def __init__(self):
        self.project_id = Config.GCP_PROJECT_ID
        self.region = Config.GCP_DEFAULT_REGION
        self.translate_client = None
        self.vertex_ai_initialized = False
        
        if GCP_AVAILABLE and self.project_id != 'your-project-id':
            self._initialize_services()
    
    def _initialize_services(self):
        """Initialize GCP services"""
        try:
            # Initialize Translation API
            self.translate_client = translate.Client()
            
            # Initialize Vertex AI
            aiplatform.init(
                project=self.project_id,
                location=self.region
            )
            self.vertex_ai_initialized = True
            print(f"GCP services initialized for project: {self.project_id}, region: {self.region}")
        except Exception as e:
            print(f"Error initializing GCP services: {e}")
            self.translate_client = None
            self.vertex_ai_initialized = False
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'en') -> str:
        """
        Translate text using Google Cloud Translation API
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'hi', 'es', 'fr')
            source_language: Source language code (default: 'en')
        
        Returns:
            Translated text
        """
        if not self.translate_client:
            print(f"Translation client not initialized. Falling back to mock translation for {target_language}.")
            return self._mock_translate(text, target_language)
        
        try:
            # Ensure target_language is a valid ISO code (e.g., 'hi' for Hindi)
            valid_lang = target_language.split('-')[0].lower()
            result = self.translate_client.translate(
                text,
                target_language=valid_lang,
                source_language=source_language,
                model=Config.TRANSLATION_MODEL
            )
            return result['translatedText']
        except Exception as e:
            print(f"Translation error for '{text}' to '{target_language}': {e}")
            return self._mock_translate(text, target_language)
    
    def _mock_translate(self, text: str, target_language: str) -> str:
        """Mock translation for testing purposes"""
        language_names = {
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ar': 'Arabic',
            'pt': 'Portuguese'
        }
        lang_name = language_names.get(target_language, target_language)
        return f"[Translated to {lang_name}] {text}"
    
    def generate_ai_story(self, description: str, category: str, artisan_name: str = "") -> str:
        """
        Generate AI story using Vertex AI
        
        Args:
            description: Product description
            category: Product category
            artisan_name: Name of the artisan
        
        Returns:
            Generated AI story
        """
        if not self.vertex_ai_initialized:
            return self._mock_generate_story(description, category, artisan_name)
        
        try:
            # Create a prompt for story generation
            prompt = f"""
            Create a compelling, creative story for a handmade {category} product with the following description:
            "{description}"
            
            The story should:
            - Be engaging and emotional
            - Highlight the craftsmanship and tradition
            - Be 2-3 paragraphs long
            - Include cultural elements if appropriate
            - Make the product feel special and unique
            
            {"Crafted by: " + artisan_name if artisan_name else ""}
            
            Story:
            """
            
            # Use Vertex AI text generation
            model = aiplatform.Model(Config.VERTEX_AI_MODEL_NAME)
            response = model.predict(
                instances=[{"prompt": prompt}],
                parameters={
                    "temperature": 0.8,
                    "max_output_tokens": 500,
                    "top_p": 0.9
                }
            )
            
            if response.predictions:
                return response.predictions[0].get('content', '')
            else:
                return self._mock_generate_story(description, category, artisan_name)
                
        except Exception as e:
            print(f"Vertex AI error: {e}")
            return self._mock_generate_story(description, category, artisan_name)
    
    def _mock_generate_story(self, description: str, category: str, artisan_name: str = "") -> str:
        """Mock story generation for testing purposes"""
        story_templates = {
            'handicraft': f"Once upon a time, a skilled artisan carefully crafted this beautiful piece. {description} This creation tells a story of tradition, patience, and the artisan's dedication to preserving cultural heritage. Each detail reflects hours of meticulous work and a deep connection to ancient techniques passed down through generations.",
            'jewelry': f"In the heart of a bustling marketplace, this exquisite piece was born. {description} The artisan's hands moved with precision, creating something that would become a treasured heirloom. This piece carries the essence of elegance and the promise of countless special moments to come.",
            'textile': f"From thread to treasure, this textile piece weaves its own story. {description} The artisan's loom sang a song of creativity as each thread was carefully placed, creating patterns that speak of culture, tradition, and artistic vision. This piece is more than fabric - it's a canvas of human expression.",
            'pottery': f"From clay to creation, this pottery piece holds ancient wisdom. {description} The artisan's hands shaped not just clay, but dreams and aspirations. Each curve and line tells of the earth's gifts transformed by human skill into something both functional and beautiful.",
            'woodwork': f"From forest to furniture, this wooden piece carries nature's spirit. {description} The artisan's tools carved away the unnecessary, revealing the wood's hidden beauty. This creation bridges the gap between nature and human craftsmanship, creating something that will age gracefully with time."
        }
        
        base_story = story_templates.get(category, f"This remarkable piece tells a unique story. {description} Crafted with care and passion, it represents the artisan's dedication to their craft and the beauty that emerges when skill meets creativity.")
        
        if artisan_name:
            base_story = f"Crafted by the skilled hands of {artisan_name}, " + base_story.lower()
        
        return base_story
    
    def get_enhanced_recommendations(self, user_id: int, user_preferences: str = "", 
                                   interaction_history: List[Dict] = None) -> List[Dict]:
        """
        Get enhanced recommendations using Vertex AI
        
        Args:
            user_id: User ID
            user_preferences: User's stated preferences
            interaction_history: List of user interactions
        
        Returns:
            List of recommended products with scores
        """
        if not self.vertex_ai_initialized:
            return self._mock_enhanced_recommendations(user_id, user_preferences)
        
        try:
            # Prepare data for recommendation
            user_data = {
                "user_id": user_id,
                "preferences": user_preferences,
                "interaction_history": interaction_history or []
            }
            
            # Use Vertex AI for recommendation scoring
            prompt = f"""
            Based on the following user data, provide product recommendations:
            User ID: {user_id}
            Preferences: {user_preferences}
            Interaction History: {json.dumps(interaction_history or [])}
            
            Recommend products that match the user's interests and preferences.
            Focus on categories and styles that align with their behavior.
            """
            
            model = aiplatform.Model(Config.VERTEX_AI_MODEL_NAME)
            response = model.predict(
                instances=[{"prompt": prompt}],
                parameters={
                    "temperature": 0.7,
                    "max_output_tokens": 300
                }
            )
            
            # Parse the response and return recommendations
            if response.predictions:
                # This would be processed based on your specific model output
                return self._mock_enhanced_recommendations(user_id, user_preferences)
            else:
                return self._mock_enhanced_recommendations(user_id, user_preferences)
                
        except Exception as e:
            print(f"Vertex AI recommendation error: {e}")
            return self._mock_enhanced_recommendations(user_id, user_preferences)
    
    def _mock_enhanced_recommendations(self, user_id: int, user_preferences: str) -> List[Dict]:
        """Mock enhanced recommendations for testing purposes"""
        return [
            {"product_id": 1, "score": 0.95, "reason": "Matches your jewelry preferences"},
            {"product_id": 2, "score": 0.88, "reason": "Similar to products you've viewed"},
            {"product_id": 3, "score": 0.82, "reason": "Popular in your region"},
            {"product_id": 4, "score": 0.78, "reason": "New artisan with great reviews"},
            {"product_id": 5, "score": 0.75, "reason": "Trending in your category"},
            {"product_id": 6, "score": 0.72, "reason": "Matches your style preferences"}
        ]
    
    def is_gcp_available(self) -> bool:
        """Check if GCP services are available"""
        return GCP_AVAILABLE and self.project_id != 'your-project-id' and self.translate_client is not None

# Global instance
gcp_services = GCPServices()
