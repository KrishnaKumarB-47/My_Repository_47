# AI Artisan Marketplace

A comprehensive AI-powered marketplace for artisans and buyers, built with Flask, HTML/CSS/JS, and SQLite, featuring Google Cloud AI integration.

## 🚀 Features

### For Artisans:
- **Product Upload**: Upload product name, description, category, price, and images
- **AI Story Generation**: Generate unique AI stories using Google Cloud Vertex AI
- **Multi-language Support**: Upload products in local languages with Google Cloud Translation API
- **Image Management**: Upload and manage product images
- **Dashboard**: Comprehensive dashboard to manage all products
- **Currency Support**: Automatic USD to INR conversion

### For Buyers:
- **Smart Recommendations**: AI-powered personalized recommendations using Vertex AI
- **Product Discovery**: Advanced browse feature with filters and search
- **Shopping Cart**: Full cart functionality with quantity management
- **Product Details**: View detailed product information with AI stories
- **Image Gallery**: High-quality product images
- **Multi-currency**: All prices displayed in Indian Rupees (INR)

## 🛠 Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Flask (Python 3.7+)
- **Database**: SQLite with cart functionality
- **AI Services**: Google Cloud Translation API & Vertex AI
- **Image Processing**: Pillow (PIL)
- **Configuration**: Environment-based config with dotenv

## 🚀 Quick Start

### Option 1: Run with Mock Services (No GCP Setup Required)
```bash
# Install dependencies
pip install -r requirements.txt

# Add demo data
python demo_data.py

# Run the application
python app.py

# Open http://localhost:5000 in your browser
```

### Option 2: Run with Google Cloud APIs
1. **Set up Google Cloud Project** (see [GCP_SETUP.md](GCP_SETUP.md))
2. **Configure environment variables**:
   ```bash
   # Create .env file
   GCP_PROJECT_ID=your-project-id
   GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json
   SECRET_KEY=your-secret-key
   ```
3. **Install dependencies and run**:
   ```bash
   pip install -r requirements.txt
   python demo_data.py
   python app.py
   ```

## 🎯 Demo Accounts

### Artisans (Upload Products)
- **john_artisan** / password123
- **maria_craft** / password123  
- **akira_wood** / password123
- **sophie_pottery** / password123

### Buyers (Browse & Shop)
- **alice_buyer** / password123
- **bob_shopper** / password123
- **charlie_collector** / password123

## 📱 Usage Guide

### For Artisans

1. **Login** with any artisan account
2. **Add Products**:
   - Click "Add New Product" on dashboard
   - Upload product image (PNG, JPG, JPEG, GIF, WEBP)
   - Enter product details in USD (auto-converted to INR)
   - Select language for translation
   - Click "Generate AI Story" for unique stories
   - Save the product

3. **Manage Products**:
   - View all products with AI stories
   - Images displayed in product cards
   - Prices shown in Indian Rupees

### For Buyers

1. **Login** with any buyer account
2. **Browse Products**:
   - Use "Browse All Products" for advanced search
   - Filter by category, search by name/description
   - Sort by price, date, or name
   - View product images and AI stories

3. **Shopping Cart**:
   - Add products to cart from browse or product detail pages
   - Manage quantities in cart
   - Remove items as needed
   - View total with shipping

4. **Product Details**:
   - Click any product to view full details
   - See high-quality images
   - Read AI-generated stories
   - Add to cart directly

## API Integration Ready

The application is designed to easily integrate with Google Cloud APIs:

1. **Google Cloud Translation API**: Replace the `translate_text()` function
2. **Vertex AI**: Replace the `generate_ai_story()` function
3. **Additional AI Services**: Extend the recommendation engine

## Project Structure

```
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── register_artisan.html
│   ├── register_buyer.html
│   ├── login_artisan.html
│   ├── login_buyer.html
│   ├── artisan_dashboard.html
│   ├── buyer_dashboard.html
│   └── product_detail.html
├── static/               # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── README.md
```

## Database Schema

- **artisans**: Store artisan information
- **buyers**: Store buyer information
- **products**: Store product details and AI stories
- **buyer_interactions**: Track user behavior for recommendations

## Future Enhancements

- Real Google Cloud API integration
- Image upload functionality
- Payment processing
- Advanced recommendation algorithms
- Social features and reviews
- Mobile app development

## Hackathon Notes

This project demonstrates:
- Full-stack web development
- AI integration concepts
- User experience design
- Database design
- API architecture
- Modern web technologies

Built for hackathon competition with focus on AI-powered features and user experience.

