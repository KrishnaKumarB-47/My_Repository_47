# 🗄️ User Management & Database Guide

## 📊 Current Database Status

### **Users in Database:**
- **Artisans**: 7 users
- **Buyers**: 4 users  
- **Admins**: 1 user
- **Total**: 12 users

### **Sample Users:**
- **Artisans**: john_artisan, maria_craft, akira_wood, sophie_pottery, pree_123
- **Buyers**: alice_buyer, bob_shopper, charlie_collector, pree_123
- **Admin**: admin (admin@artisanmarketplace.com)

## 🔧 How to Manage Users

### **1. View All Users**
```bash
python database_viewer.py
```
Then select option 1 to view all users with their details.

### **2. Modify User Information**
```bash
python database_viewer.py
```
Then select option 4 to modify user details:
- Change name, email, location, language
- Delete users
- Update preferences

### **3. Reset User Passwords**
```bash
python database_viewer.py
```
Then select option 5 to reset passwords for any user.

### **4. Quick Database Check**
```bash
python quick_db_check.py
```
Shows summary of all users and products.

## 🔑 Login Credentials

### **Admin Access:**
- **Username**: `admin`
- **Password**: `admin123`
- **Features**: Full admin dashboard, user management, product management

### **Artisan Accounts:**
- **john_artisan** / `password123`
- **maria_craft** / `password123`
- **akira_wood** / `password123`
- **sophie_pottery** / `password123`
- **pree_123** / `password123`

### **Buyer Accounts:**
- **alice_buyer** / `password123`
- **bob_shopper** / `password123`
- **charlie_collector** / `password123`
- **pree_123** / `password123`

## 🌐 Environment File Setup

### **1. Create .env File**
Create a file named `.env` in your project root with:

```env
# Google Cloud Configuration
GCP_PROJECT_ID=your-project-id-here
GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json

# Flask Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production

# Optional: Override default region
# GCP_DEFAULT_REGION=asia-south1
```

### **2. For Real API Integration:**
- **YES, specify API path in .env file**
- Set `GOOGLE_APPLICATION_CREDENTIALS=./path/to/your/service-account-key.json`
- Set `GCP_PROJECT_ID=your-actual-project-id`
- Download service account JSON key from Google Cloud Console

## 📸 Image Display Fix

### **Issue**: Product images not showing
### **Solution**: 
1. ✅ Uploads directory created
2. ✅ Test product with image added
3. ✅ Image display code fixed

### **To Test Image Display:**
1. Start the application: `python app.py`
2. Login as artisan: `john_artisan` / `password123`
3. Go to dashboard - you should see the test product with image
4. Add new products with images to test upload functionality

## 🎯 User Activity Monitoring

### **View User Login Activity:**
The database stores `created_at` timestamps for all users, but doesn't track login sessions. To add login tracking:

1. **Add login tracking table** (optional):
```sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    user_type TEXT NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

2. **Track logins in app.py** (optional):
```python
# Add to login routes
cursor.execute('''
    INSERT INTO user_sessions (user_id, user_type, ip_address)
    VALUES (?, ?, ?)
''', (user_id, user_type, request.remote_addr))
```

## 🚀 Quick Commands

### **Start Application:**
```bash
python app.py
```

### **View Database:**
```bash
python database_viewer.py
```

### **Quick Check:**
```bash
python quick_db_check.py
```

### **Add Test Data:**
```bash
python demo_data.py
```

### **Create Admin:**
```bash
python create_admin.py
```

## 🔍 Troubleshooting

### **Images Not Showing:**
1. Check if `static/uploads/` directory exists
2. Verify image files are uploaded
3. Check browser console for 404 errors
4. Ensure Flask is serving static files correctly

### **Users Not Found:**
1. Run `python quick_db_check.py` to see all users
2. Check if user exists in correct table (artisans/buyers/admins)
3. Verify username spelling

### **Login Issues:**
1. Check password hashing
2. Verify user exists in database
3. Check session management

## 📱 Admin Dashboard Features

### **Access**: Login as `admin` / `admin123`

### **Features:**
- **Statistics**: View user counts, product counts, cart items
- **Product Management**: View, delete products
- **User Management**: View artisans and buyers
- **Real-time Updates**: Live statistics

### **URL**: `http://localhost:5000/admin_dashboard`

---

**All user management tools are ready! Use `python database_viewer.py` to manage users and their login activity.** 🎉
