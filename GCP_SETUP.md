# Google Cloud Platform Integration Setup

## Overview
This guide will help you set up Google Cloud Translation API and Vertex AI for the AI Artisan Marketplace application.

## Prerequisites
- Google Cloud Platform account
- Billing enabled on your GCP project
- Python 3.7+ installed

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: `ai-artisan-marketplace`
4. Select your organization (if applicable)
5. Click "Create"

## Step 2: Enable Required APIs

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for and enable the following APIs:
   - **Cloud Translation API**
   - **Vertex AI API**

## Step 3: Create Service Account

1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Enter details:
   - Name: `ai-artisan-service-account`
   - Description: `Service account for AI Artisan Marketplace`
4. Click "Create and Continue"
5. Assign roles:
   - `Cloud Translation API User`
   - `Vertex AI User`
   - `Storage Object Viewer` (if using Cloud Storage)
6. Click "Continue" → "Done"

## Step 4: Generate Service Account Key

1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON" format
5. Click "Create"
6. Download the JSON file and save it securely

## Step 5: Configure Environment Variables

1. Copy the downloaded JSON file to your project directory
2. Rename it to `service-account-key.json`
3. Create a `.env` file in your project root:

```env
# Google Cloud Configuration
GCP_PROJECT_ID=your-project-id-here
GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json

# Flask Configuration
SECRET_KEY=your-secret-key-here

# Optional: Override default region
GCP_DEFAULT_REGION=asia-south1
```

## Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 7: Test the Integration

1. Run the application:
```bash
python app.py
```

2. Test translation:
   - Go to artisan dashboard
   - Add a product in a different language
   - Check if translation works

3. Test AI story generation:
   - Add a product
   - Click "Generate AI Story"
   - Verify the story is generated

## Regional Configuration

### Mumbai (asia-south1)
- Default region for the application
- Lower latency for Indian users
- Data residency compliance

### Delhi (asia-south2)
- Alternative region
- Can be used for load balancing
- Change in `config.py` if needed

## API Usage and Costs

### Translation API
- **Free tier**: 500,000 characters per month
- **Paid tier**: $20 per 1M characters
- **Supported languages**: 100+ languages

### Vertex AI
- **Text generation**: $0.0005 per 1K characters
- **Model training**: Variable pricing
- **Prediction requests**: $0.0001 per 1K characters

## Troubleshooting

### Common Issues

1. **Authentication Error**
   - Check if `GOOGLE_APPLICATION_CREDENTIALS` is set correctly
   - Verify the service account key file exists
   - Ensure the service account has proper permissions

2. **API Not Enabled**
   - Go to "APIs & Services" → "Library"
   - Search for the required APIs
   - Click "Enable" if not already enabled

3. **Billing Issues**
   - Ensure billing is enabled on your project
   - Check if you have sufficient credits
   - Monitor usage in the GCP Console

4. **Region Errors**
   - Verify the region is correct in `config.py`
   - Check if the API is available in your selected region

### Testing Without GCP

The application includes mock services that work without GCP:
- Translation shows `[Translated to Language]` prefix
- AI stories use template-based generation
- Recommendations use basic algorithms

## Security Best Practices

1. **Never commit service account keys to version control**
2. **Use environment variables for sensitive data**
3. **Rotate service account keys regularly**
4. **Monitor API usage and costs**
5. **Use least privilege principle for service accounts**

## Monitoring and Logging

1. **Enable Cloud Logging** for debugging
2. **Set up billing alerts** to monitor costs
3. **Use Cloud Monitoring** for API performance
4. **Check Cloud Console** for usage statistics

## Next Steps

1. **Deploy to production** using Google Cloud Run
2. **Set up CI/CD** with Cloud Build
3. **Implement caching** for better performance
4. **Add more AI features** using other Vertex AI models
5. **Scale horizontally** as your user base grows

## Support

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Translation API Guide](https://cloud.google.com/translate/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [GCP Support](https://cloud.google.com/support)
