"""
Chatbot service using Google Gemini AI for Artisan Marketplace
"""
import os
import json
import google.generativeai as genai
from config import Config
import sqlite3
from datetime import datetime

class ChatbotService:
    def __init__(self):
        self.model = None
        self.setup_gemini()
    
    def setup_gemini(self):
        """Initialize Gemini AI model"""
        try:
            # Configure Gemini API
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                print("Warning: GEMINI_API_KEY not found. Chatbot will use fallback responses.")
                return
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            print("Gemini AI initialized successfully")
        except Exception as e:
            print(f"Error initializing Gemini AI: {e}")
            self.model = None
    
    def get_chat_response(self, user_message, user_context=None):
        """
        Get response from Gemini AI based on user message and context
        """
        try:
            if not self.model:
                return self._get_fallback_response(user_message)
            
            # Build context for the AI
            context = self._build_context(user_context)
            
            # Create prompt with context
            prompt = f"""
            You are a helpful assistant for the Artisan Marketplace, a platform connecting local artisans with buyers. 
            Your role is to help users navigate the marketplace, find products, understand artisan stories, and provide general assistance.
            
            Context about the marketplace:
            {context}
            
            User message: {user_message}
            
            Please provide a helpful, friendly response. If the user is asking about products, artisans, or marketplace features, 
            provide relevant information. Keep responses concise but informative.
            """
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response.text:
                return {
                    'success': True,
                    'message': response.text,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return self._get_fallback_response(user_message)
                
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return self._get_fallback_response(user_message)
    
    def _build_context(self, user_context):
        """Build context about the marketplace for the AI"""
        context_parts = [
            "This is an Artisan Marketplace where:",
            "- Local artisans can showcase their handmade products",
            "- Buyers can discover unique, handcrafted items",
            "- Each product has an AI-generated story about its creation",
            "- Products are categorized (pottery, jewelry, textiles, etc.)",
            "- Users can browse, search, and add items to cart",
            "- The platform supports multiple languages and currencies (INR)",
            "- Artisans can manage their product listings",
            "- Buyers get personalized recommendations"
        ]
        
        if user_context:
            context_parts.append(f"\nCurrent user context: {user_context}")
        
        # Add some recent product info if available
        try:
            conn = sqlite3.connect('artisan_marketplace.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT p.name, p.category, p.price, a.name as artisan_name
                FROM products p
                JOIN artisans a ON p.artisan_id = a.id
                ORDER BY p.created_at DESC
                LIMIT 5
            ''')
            
            recent_products = cursor.fetchall()
            if recent_products:
                context_parts.append("\nRecent products available:")
                for product in recent_products:
                    context_parts.append(f"- {product[0]} ({product[1]}) by {product[3]} - ₹{product[2]}")
            
            conn.close()
        except Exception as e:
            print(f"Error fetching context: {e}")
        
        return "\n".join(context_parts)
    
    def _get_fallback_response(self, user_message):
        """Provide fallback responses when AI is not available"""
        fallback_responses = {
            'hello': "Hello! Welcome to the Artisan Marketplace. How can I help you today?",
            'products': "You can browse our artisan products by visiting the Browse page. We have handmade items in various categories like pottery, jewelry, textiles, and more.",
            'artisan': "Artisans can register and showcase their handmade products on our platform. They can add product details, images, and stories.",
            'buy': "To purchase items, browse our products, add them to your cart, and proceed to checkout. You'll need to register as a buyer first.",
            'register': "You can register as either an artisan (to sell products) or a buyer (to purchase items). Visit our registration pages to get started.",
            'help': "I'm here to help! You can ask me about products, artisans, registration, or any general questions about our marketplace.",
            'price': "All prices on our marketplace are in Indian Rupees (₹). You can filter products by price range when browsing.",
            'categories': "We have various product categories including pottery, jewelry, textiles, woodwork, paintings, and more handcrafted items."
        }
        
        message_lower = user_message.lower()
        
        for key, response in fallback_responses.items():
            if key in message_lower:
                return {
                    'success': True,
                    'message': response,
                    'timestamp': datetime.now().isoformat()
                }
        
        # Default response
        return {
            'success': True,
            'message': "I'm here to help you with the Artisan Marketplace. You can ask me about products, artisans, registration, or any other questions about our platform. How can I assist you?",
            'timestamp': datetime.now().isoformat()
        }
    
    def get_product_recommendations(self, user_message):
        """Get product recommendations based on user query"""
        try:
            conn = sqlite3.connect('artisan_marketplace.db')
            cursor = conn.cursor()
            
            # Extract keywords from user message
            keywords = user_message.lower().split()
            
            # Search for products matching keywords
            query = '''
                SELECT p.id, p.name, p.description, p.category, p.price, p.image_path, a.name as artisan_name
                FROM products p
                JOIN artisans a ON p.artisan_id = a.id
                WHERE 1=1
            '''
            params = []
            
            for keyword in keywords:
                if len(keyword) > 2:  # Only search meaningful words
                    query += ' AND (p.name LIKE ? OR p.description LIKE ? OR p.category LIKE ?)'
                    params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
            
            query += ' LIMIT 5'
            cursor.execute(query, params)
            products = cursor.fetchall()
            
            conn.close()
            
            if products:
                response = "Here are some products that might interest you:\n\n"
                for product in products:
                    response += f"• {product[1]} ({product[3]}) by {product[6]} - ₹{product[4]}\n"
                    response += f"  {product[2][:100]}...\n\n"
                response += "Visit our Browse page to see all products and add items to your cart!"
            else:
                response = "I couldn't find specific products matching your query, but you can browse all our artisan products on the Browse page. We have a wide variety of handcrafted items!"
            
            return {
                'success': True,
                'message': response,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting product recommendations: {e}")
            return {
                'success': True,
                'message': "You can browse all our artisan products on the Browse page. We have various categories like pottery, jewelry, textiles, and more!",
                'timestamp': datetime.now().isoformat()
            }

# Global chatbot service instance
chatbot_service = ChatbotService()
