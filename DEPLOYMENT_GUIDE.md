# AI Artisan Marketplace - Deployment Guide

## 🚀 Quick Deployment to Render.com

### Step 1: Prepare Your Repository
1. Make sure all files are committed to your Git repository
2. Push your code to GitHub, GitLab, or Bitbucket

### Step 2: Deploy to Render.com
1. Go to [Render.com](https://render.com) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your Git repository
4. Configure the service:
   - **Name**: `ai-artisan-marketplace`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python demo_data.py`
   - **Start Command**: `python app.py`
   - **Instance Type**: Free tier (or upgrade as needed)

### Step 3: Environment Variables
The following environment variables are already configured in `render.yml`:
- `FLASK_ENV=production`
- `SECRET_KEY` (auto-generated)
- `GCP_PROJECT_ID=virtual-firefly-472606`
- `GEMINI_API_KEY` (configured)

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for the build to complete (5-10 minutes)
3. Your app will be available at: `https://ai-artisan-marketplace.onrender.com`

## 🔧 Alternative Deployment Options

### Heroku
1. Install Heroku CLI
2. Create a Heroku app: `heroku create your-app-name`
3. Set environment variables:
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-secret-key
   ```
4. Deploy: `git push heroku main`

### Railway
1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will auto-detect Python and deploy

### Vercel (with modifications)
1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```
3. Deploy: `vercel --prod`

## 📱 Testing Your Deployment

### Demo Accounts Available:
**Artisans:**
- Username: `john_artisan`, Password: `password123`
- Username: `maria_craft`, Password: `password123`

**Buyers:**
- Username: `alice_buyer`, Password: `password123`
- Username: `bob_shopper`, Password: `password123`

### Features to Test:
1. ✅ User registration and login
2. ✅ Product upload with images
3. ✅ AI story generation
4. ✅ Product browsing and search
5. ✅ Shopping cart functionality
6. ✅ Multi-language support
7. ✅ Admin dashboard

## 🛠 Troubleshooting

### Common Issues:
1. **Build Fails**: Check `requirements.txt` for all dependencies
2. **App Crashes**: Check logs in Render dashboard
3. **Database Issues**: Ensure `demo_data.py` runs during build
4. **Static Files**: Verify file paths in templates

### Logs:
- Render: Check "Logs" tab in dashboard
- Heroku: `heroku logs --tail`
- Railway: Check "Deployments" tab

## 🔒 Security Notes

- The app uses mock AI services for demo purposes
- For production, configure real Google Cloud APIs
- Update `SECRET_KEY` to a secure random string
- Consider using a production database (PostgreSQL)

## 📞 Support

If you encounter issues:
1. Check the logs in your deployment platform
2. Verify all environment variables are set
3. Ensure all dependencies are in `requirements.txt`
4. Test locally first: `python app.py`
