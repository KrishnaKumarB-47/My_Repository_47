# Chatbot Integration Guide - Gemini AI Assistant

This guide explains how to set up and use the Gemini AI chatbot integration in the Artisan Marketplace.

## 🚀 Features

- **AI-Powered Responses**: Uses Google Gemini AI for intelligent conversations
- **Fallback System**: Works without API key using smart fallback responses
- **Product Recommendations**: Can recommend products based on user queries
- **Modern UI**: Beautiful, responsive chat interface
- **Real-time Chat**: Instant messaging with typing indicators
- **Quick Actions**: Pre-built buttons for common queries
- **Context Awareness**: Understands user type and marketplace context

## 📋 Prerequisites

1. Python 3.7+
2. Flask application running
3. (Optional) Google Gemini API key

## 🔧 Installation & Setup

### 1. Install Dependencies

The chatbot integration adds the following dependency:

```bash
pip install google-generativeai==0.3.2
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Add the following to your `.env` file:

```env
# Gemini AI Configuration (for chatbot)
GEMINI_API_KEY=your-gemini-api-key-here
```

### 3. Get Gemini API Key (Optional)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

**Note**: The chatbot works without an API key using intelligent fallback responses.

## 🏗️ Architecture

### Backend Components

1. **`chatbot_service.py`**: Core chatbot logic and Gemini integration
2. **`app.py`**: Flask routes for chat API endpoints
3. **`config.py`**: Configuration for Gemini API

### Frontend Components

1. **`templates/chatbot.html`**: Main chat interface
2. **`static/css/chatbot.css`**: Chat styling
3. **`static/js/chatbot.js`**: Chat interactions and API calls

## 🎯 Usage

### Accessing the Chatbot

1. **Direct URL**: Visit `/chatbot`
2. **Navigation**: Click "AI Assistant" in the main navigation
3. **Available to all users**: Both logged-in and guest users

### Chat Features

#### Quick Actions
- **Pottery**: Find pottery products
- **Jewelry**: Browse jewelry items
- **Register**: Get registration help
- **Browse**: General product browsing

#### Chat Capabilities
- Product recommendations
- Registration guidance
- General marketplace help
- Artisan and buyer support

### API Endpoints

#### POST `/api/chat`
Send a message to the chatbot.

**Request:**
```json
{
    "message": "Show me pottery products"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Here are some pottery products...",
    "timestamp": "2024-01-20T10:30:00"
}
```

## 🧪 Testing

### Run the Test Script

```bash
python test_chatbot.py
```

This will test:
- Basic chatbot responses
- Product recommendations
- Registration help
- Fallback responses
- API endpoint connectivity

### Manual Testing

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Visit `http://localhost:5000/chatbot`

3. Try these sample queries:
   - "Hello, what can you help me with?"
   - "Show me pottery products"
   - "How do I register as an artisan?"
   - "What products do you have?"

## 🔧 Configuration Options

### Chatbot Service Configuration

In `chatbot_service.py`, you can customize:

```python
class ChatbotService:
    def __init__(self):
        # Change model if needed
        self.model = genai.GenerativeModel('gemini-pro')
```

### UI Customization

In `static/css/chatbot.css`, customize:
- Colors and gradients
- Font sizes
- Animation speeds
- Layout dimensions

## 🚨 Error Handling

### API Key Issues
- **Missing API Key**: Automatically uses fallback responses
- **Invalid API Key**: Falls back to intelligent responses
- **API Quota Exceeded**: Graceful degradation to fallback

### Network Issues
- **Connection Errors**: Shows user-friendly error messages
- **Timeout**: Handles long response times gracefully
- **Offline Mode**: Maintains basic functionality

### Frontend Errors
- **JavaScript Errors**: Console logging with user notifications
- **API Failures**: Retry mechanisms and error states
- **Browser Compatibility**: Progressive enhancement

## 📱 Mobile Support

The chatbot interface is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Touch devices

## 🔒 Security Considerations

1. **API Key Security**: Never expose API keys in client-side code
2. **Input Validation**: All user inputs are sanitized
3. **Rate Limiting**: Consider implementing rate limiting for production
4. **Content Filtering**: Gemini API includes built-in safety filters

## 🚀 Deployment

### Production Checklist

1. **Environment Variables**: Set `GEMINI_API_KEY` in production
2. **Error Logging**: Configure proper logging
3. **Rate Limiting**: Implement API rate limiting
4. **Monitoring**: Set up monitoring for API usage
5. **Backup Responses**: Ensure fallback system works

### Environment Variables

```env
# Production environment
GEMINI_API_KEY=your-production-api-key
SECRET_KEY=your-secure-secret-key
```

## 🔄 Updates & Maintenance

### Updating Dependencies

```bash
pip install --upgrade google-generativeai
```

### Monitoring Usage

- Check Gemini API usage in Google AI Studio
- Monitor chat logs for common queries
- Update fallback responses based on user needs

## 🤝 Contributing

To improve the chatbot:

1. **Add New Fallback Responses**: Update `_get_fallback_response()` method
2. **Enhance Product Recommendations**: Improve `get_product_recommendations()`
3. **UI Improvements**: Modify CSS and JavaScript files
4. **New Features**: Add to the chatbot service class

## 📞 Support

For issues with the chatbot integration:

1. Check the test script output
2. Verify environment variables
3. Check browser console for errors
4. Review Flask application logs

## 🎉 Success!

Your Artisan Marketplace now has a powerful AI assistant that can:
- Help users navigate the platform
- Recommend products
- Provide registration guidance
- Answer general questions
- Work with or without Gemini API

The chatbot enhances user experience and provides 24/7 support for your marketplace!
