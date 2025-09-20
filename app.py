# Utility route to update product images based on product name
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
import sqlite3
import os
import json
from datetime import datetime
import hashlib
import random

# ...existing code...

# Place this route after app initialization
# ...existing code...
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
import sqlite3
import os
import json
from datetime import datetime
import hashlib
import random
from werkzeug.utils import secure_filename
from config import Config
from gcp_services import gcp_services
from chatbot_service import chatbot_service

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Database initialization
def init_db():
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    # Create artisans table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artisans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            location TEXT,
            language TEXT DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create buyers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buyers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            preferences TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artisan_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            image_path TEXT,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            ai_story TEXT,
            language TEXT DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (artisan_id) REFERENCES artisans (id)
        )
    ''')
    
    # Create cart table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            buyer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (buyer_id) REFERENCES buyers (id),
            FOREIGN KEY (product_id) REFERENCES products (id),
            UNIQUE(buyer_id, product_id)
        )
    ''')
    
    # Create buyer interactions table for recommendations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buyer_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            buyer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            interaction_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (buyer_id) REFERENCES buyers (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Create admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def format_currency(amount):
    """Format amount in Indian Rupees"""
    return f"{Config.CURRENCY_SYMBOL}{amount:,.2f}"

def convert_usd_to_inr(usd_amount):
    """Convert USD to INR (approximate rate)"""
    return usd_amount * 83.0  # Approximate conversion rate

def generate_ai_story(description, category, artisan_name=""):
    """Generate AI story using GCP Vertex AI or fallback to mock"""
    return gcp_services.generate_ai_story(description, category, artisan_name)

def translate_text(text, target_language, source_language='en'):
    """Translate text using Google Cloud Translation API or fallback to mock"""
    return gcp_services.translate_text(text, target_language, source_language)

def get_recommendations(buyer_id, limit=6):
    """Enhanced recommendation engine using GCP Vertex AI"""
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    # Get buyer's preferences and interaction history
    cursor.execute('SELECT preferences FROM buyers WHERE id = ?', (buyer_id,))
    buyer_data = cursor.fetchone()
    preferences = buyer_data[0] if buyer_data else ""
    
    cursor.execute('''
        SELECT p.category, p.id, p.name, p.description, p.price, p.image_path, p.ai_story, a.name as artisan_name
        FROM products p
        JOIN artisans a ON p.artisan_id = a.id
        JOIN buyer_interactions bi ON p.id = bi.product_id
        WHERE bi.buyer_id = ? AND bi.interaction_type = 'view'
        ORDER BY bi.created_at DESC
        LIMIT 10
    ''', (buyer_id,))
    
    viewed_products = cursor.fetchall()
    
    # Get interaction history for GCP
    interaction_history = []
    for product in viewed_products:
        interaction_history.append({
            "product_id": product[1],
            "category": product[0],
            "name": product[2]
        })
    
    # Use GCP enhanced recommendations
    enhanced_recs = gcp_services.get_enhanced_recommendations(
        buyer_id, preferences, interaction_history
    )
    
    if not viewed_products and not enhanced_recs:
        # If no history, return random products
        cursor.execute('''
            SELECT p.category, p.id, p.name, p.description, p.price, p.image_path, p.ai_story, a.name as artisan_name
            FROM products p
            JOIN artisans a ON p.artisan_id = a.id
            ORDER BY RANDOM()
            LIMIT ?
        ''', (limit,))
        recommendations = cursor.fetchall()
    else:
        # Get products based on enhanced recommendations or categories
        if enhanced_recs:
            product_ids = [rec['product_id'] for rec in enhanced_recs[:limit]]
            placeholders = ','.join(['?' for _ in product_ids])
            cursor.execute(f'''
                SELECT p.category, p.id, p.name, p.description, p.price, p.image_path, p.ai_story, a.name as artisan_name
                FROM products p
                JOIN artisans a ON p.artisan_id = a.id
                WHERE p.id IN ({placeholders})
                ORDER BY CASE p.id {' '.join([f'WHEN {pid} THEN {i}' for i, pid in enumerate(product_ids)])} END
            ''', product_ids)
        else:
            # Fallback to category-based recommendations
            categories = [product[0] for product in viewed_products]
            placeholders = ','.join(['?' for _ in categories])
            cursor.execute(f'''
                SELECT p.category, p.id, p.name, p.description, p.price, p.image_path, p.ai_story, a.name as artisan_name
                FROM products p
                JOIN artisans a ON p.artisan_id = a.id
                WHERE p.category IN ({placeholders})
                ORDER BY RANDOM()
                LIMIT ?
            ''', categories + [limit])
        
        recommendations = cursor.fetchall()
    
    conn.close()
    return recommendations

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_artisan', methods=['GET', 'POST'])
def register_artisan():
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect('artisan_marketplace.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO artisans (username, email, password, name, location, language)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (data['username'], data['email'], hash_password(data['password']), 
                  data['name'], data['location'], data.get('language', 'en')))
            
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Artisan registered successfully'})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'success': False, 'message': 'Username or email already exists'})
    
    return render_template('register_artisan.html')

@app.route('/register_buyer', methods=['GET', 'POST'])
def register_buyer():
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect('artisan_marketplace.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO buyers (username, email, password, name, preferences)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['username'], data['email'], hash_password(data['password']), 
                  data['name'], data.get('preferences', '')))
            
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Buyer registered successfully'})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'success': False, 'message': 'Username or email already exists'})
    
    return render_template('register_buyer.html')

@app.route('/login_artisan', methods=['GET', 'POST'])
def login_artisan():
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect('artisan_marketplace.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, name FROM artisans 
            WHERE username = ? AND password = ?
        ''', (data['username'], hash_password(data['password'])))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['user_type'] = 'artisan'
            session['username'] = user[1]
            session['name'] = user[2]
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login_artisan.html')

@app.route('/login_buyer', methods=['GET', 'POST'])
def login_buyer():
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect('artisan_marketplace.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, name FROM buyers 
            WHERE username = ? AND password = ?
        ''', (data['username'], hash_password(data['password'])))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['user_type'] = 'buyer'
            session['username'] = user[1]
            session['name'] = user[2]
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login_buyer.html')

@app.route('/artisan_dashboard')
def artisan_dashboard():
    if 'user_id' not in session or session['user_type'] != 'artisan':
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, description, category, price, image_path, ai_story, created_at
        FROM products WHERE artisan_id = ?
        ORDER BY created_at DESC
    ''', (session['user_id'],))
    
    products = cursor.fetchall()
    conn.close()
    
    return render_template('artisan_dashboard.html', products=products)

@app.route('/buyer_dashboard')
def buyer_dashboard():
    if 'user_id' not in session or session['user_type'] != 'buyer':
        return redirect(url_for('index'))
    
    recommendations = get_recommendations(session['user_id'])
    return render_template('buyer_dashboard.html', recommendations=recommendations)

@app.route('/add_product', methods=['POST'])
def add_product():
    if 'user_id' not in session or session['user_type'] != 'artisan':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Handle form data (including file upload)
    if 'image' in request.files:
        # Handle file upload
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to make filename unique
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_path = filename
        else:
            image_path = None
    else:
        # Handle JSON data (from AJAX)
        data = request.get_json()
        image_path = None
    
    # Get form data
    if 'image' in request.files:
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        price = float(request.form.get('price'))
        language = request.form.get('language', 'en')
    else:
        name = data['name']
        description = data['description']
        category = data['category']
        price = float(data['price'])
        language = data.get('language', 'en')
    
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    # Get artisan name for AI story
    cursor.execute('SELECT name FROM artisans WHERE id = ?', (session['user_id'],))
    artisan_data = cursor.fetchone()
    artisan_name = artisan_data[0] if artisan_data else ""
    
    # Generate AI story using GCP services
    ai_story = generate_ai_story(description, category, artisan_name)
    
    # Translate if needed
    if language != 'en':
        translated_description = translate_text(description, language)
        translated_name = translate_text(name, language)
    else:
        translated_description = description
        translated_name = name
    
    # Price is already in INR (no conversion needed)
    cursor.execute('''
        INSERT INTO products (artisan_id, name, description, category, price, ai_story, language, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (session['user_id'], translated_name, translated_description, 
          category, price, ai_story, language, image_path))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Product added successfully'})

@app.route('/generate_story', methods=['POST'])
def generate_story():
    if 'user_id' not in session or session['user_type'] != 'artisan':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    
    # Get artisan name for better story generation
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM artisans WHERE id = ?', (session['user_id'],))
    artisan_data = cursor.fetchone()
    artisan_name = artisan_data[0] if artisan_data else ""
    conn.close()
    
    story = generate_ai_story(data['description'], data['category'], artisan_name)
    
    return jsonify({'success': True, 'story': story})

@app.route('/view_product/<int:product_id>')
def view_product(product_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.id, p.name, p.description, p.category, p.price, p.image_path, p.ai_story, a.name as artisan_name
        FROM products p
        JOIN artisans a ON p.artisan_id = a.id
        WHERE p.id = ?
    ''', (product_id,))
    
    product = cursor.fetchone()
    
    if product:
        # Record view interaction for recommendations
        if session['user_type'] == 'buyer':
            cursor.execute('''
                INSERT INTO buyer_interactions (buyer_id, product_id, interaction_type)
                VALUES (?, ?, ?)
            ''', (session['user_id'], product_id, 'view'))
            conn.commit()
    
    conn.close()
    
    if not product:
        return redirect(url_for('index'))
    
    return render_template('product_detail.html', product=product)

@app.route('/browse')
def browse():
    """Browse all products with filters"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Get filter parameters
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'newest')
    
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    # Build query based on filters
    query = '''
        SELECT p.category, p.id, p.name, p.description, p.price, p.image_path, p.ai_story, a.name as artisan_name
        FROM products p
        JOIN artisans a ON p.artisan_id = a.id
        WHERE 1=1
    '''
    params = []
    
    if category != 'all':
        query += ' AND p.category = ?'
        params.append(category)
    
    if search:
        query += ' AND (p.name LIKE ? OR p.description LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    # Add sorting
    if sort_by == 'newest':
        query += ' ORDER BY p.created_at DESC'
    elif sort_by == 'oldest':
        query += ' ORDER BY p.created_at ASC'
    elif sort_by == 'price_low':
        query += ' ORDER BY p.price ASC'
    elif sort_by == 'price_high':
        query += ' ORDER BY p.price DESC'
    elif sort_by == 'name':
        query += ' ORDER BY p.name ASC'
    
    cursor.execute(query, params)
    products = cursor.fetchall()
    
    # Get categories for filter dropdown
    cursor.execute('SELECT DISTINCT category FROM products')
    categories = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return render_template('browse.html', products=products, categories=categories, 
                         current_category=category, current_search=search, current_sort=sort_by)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Add product to cart"""
    if 'user_id' not in session or session['user_type'] != 'buyer':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    try:
        # Check if item already in cart
        cursor.execute('SELECT id, quantity FROM cart WHERE buyer_id = ? AND product_id = ?', 
                      (session['user_id'], product_id))
        existing = cursor.fetchone()
        
        if existing:
            # Update quantity
            new_quantity = existing[1] + quantity
            cursor.execute('UPDATE cart SET quantity = ? WHERE id = ?', 
                          (new_quantity, existing[0]))
        else:
            # Add new item
            cursor.execute('''
                INSERT INTO cart (buyer_id, product_id, quantity)
                VALUES (?, ?, ?)
            ''', (session['user_id'], product_id, quantity))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Product added to cart'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': 'Error adding to cart'})

@app.route('/cart')
def cart():
    """View shopping cart"""
    if 'user_id' not in session or session['user_type'] != 'buyer':
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.id, c.quantity, p.id, p.name, p.description, p.price, p.image_path, a.name as artisan_name
        FROM cart c
        JOIN products p ON c.product_id = p.id
        JOIN artisans a ON p.artisan_id = a.id
        WHERE c.buyer_id = ?
        ORDER BY c.added_at DESC
    ''', (session['user_id'],))
    
    cart_items = cursor.fetchall()
    
    # Calculate total
    total = sum(item[5] * item[1] for item in cart_items)  # price * quantity
    
    conn.close()
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    """Remove item from cart"""
    if 'user_id' not in session or session['user_type'] != 'buyer':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    cart_item_id = data.get('cart_item_id')
    
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM cart WHERE id = ? AND buyer_id = ?', 
                  (cart_item_id, session['user_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Item removed from cart'})

@app.route('/update_cart_quantity', methods=['POST'])
def update_cart_quantity():
    """Update quantity of item in cart"""
    if 'user_id' not in session or session['user_type'] != 'buyer':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    cart_item_id = data.get('cart_item_id')
    quantity = data.get('quantity', 1)
    
    if quantity <= 0:
        return jsonify({'success': False, 'message': 'Quantity must be positive'})
    
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    cursor.execute('UPDATE cart SET quantity = ? WHERE id = ? AND buyer_id = ?', 
                  (quantity, cart_item_id, session['user_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Quantity updated'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.get_json()
        conn = sqlite3.connect('artisan_marketplace.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, name FROM admins 
            WHERE username = ? AND password = ?
        ''', (data['username'], hash_password(data['password'])))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['user_type'] = 'admin'
            session['username'] = user[1]
            session['name'] = user[2]
            return jsonify({'success': True, 'message': 'Admin login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid admin credentials'})
    
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) FROM artisans')
    artisan_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM buyers')
    buyer_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM products')
    product_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM cart')
    cart_count = cursor.fetchone()[0]
    
    # Get recent products
    cursor.execute('''
        SELECT p.id, p.name, p.price, p.created_at, a.name as artisan_name
        FROM products p
        JOIN artisans a ON p.artisan_id = a.id
        ORDER BY p.created_at DESC
        LIMIT 10
    ''')
    recent_products = cursor.fetchall()
    
    # Get all users
    cursor.execute('SELECT id, name, email, created_at FROM artisans ORDER BY created_at DESC')
    artisans = cursor.fetchall()
    
    cursor.execute('SELECT id, name, email, created_at FROM buyers ORDER BY created_at DESC')
    buyers = cursor.fetchall()
    
    conn.close()
    
    stats = {
        'artisan_count': artisan_count,
        'buyer_count': buyer_count,
        'product_count': product_count,
        'cart_count': cart_count
    }
    
    return render_template('admin_dashboard.html', stats=stats, recent_products=recent_products, 
                         artisans=artisans, buyers=buyers)

@app.route('/admin_delete_product/<int:product_id>')
def admin_delete_product(product_id):
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('artisan_marketplace.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_dashboard'))

# Chatbot routes
@app.route('/chatbot')
def chatbot_page():
    """Chatbot page"""
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """API endpoint for chatbot interactions"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False, 
                'message': 'Please enter a message'
            })
        
        # Get user context if available
        user_context = None
        if 'user_id' in session:
            user_type = session.get('user_type', 'guest')
            user_name = session.get('name', 'User')
            user_context = f"User type: {user_type}, Name: {user_name}"
        
        # Check if user is asking about products
        product_keywords = ['product', 'item', 'buy', 'purchase', 'show me', 'find', 'search', 'recommend']
        if any(keyword in user_message.lower() for keyword in product_keywords):
            response = chatbot_service.get_product_recommendations(user_message)
        else:
            response = chatbot_service.get_chat_response(user_message, user_context)
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in chat API: {e}")
        return jsonify({
            'success': False,
            'message': 'Sorry, I encountered an error. Please try again.'
        })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

