# 🔧 Setup Instructions for GenAI Hackathon

## ⚠️ Required: Google API Key Setup

The application requires a Google API key to use the Gemini AI model.

### Step 1: Get your Google API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Create the .env file
The application looks for the API key in `/agents/.env`

Run these commands in your terminal:

```bash
# Navigate to the project directory
cd /home/test/GenAI_Hackathon

# Create the .env file in the agents directory
echo "GOOGLE_API_KEY=your-actual-api-key-here" > agents/.env

# Or use a text editor
nano agents/.env
```

### Step 3: Add your API key
Replace `your-actual-api-key-here` with your actual Google API key.

Example `.env` file content:
```
GOOGLE_API_KEY=AIzaSyD-xxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 4: Run the application
```bash
streamlit run app.py
```

## 📝 Environment Variables Template

Create a file named `.env` in the `agents/` directory with the following content:

```env
# Required: Google API Key for Gemini AI
GOOGLE_API_KEY=your-google-api-key-here

# Optional: Firebase configuration (if needed)
# FIREBASE_API_KEY=your-firebase-api-key
# FIREBASE_AUTH_DOMAIN=your-auth-domain
# FIREBASE_PROJECT_ID=your-project-id

# Optional: BigQuery configuration (if needed)
# GCP_PROJECT_ID=your-gcp-project-id
# GCP_DATASET_ID=your-dataset-id
```

## 🚨 Troubleshooting

If you see the error: `RuntimeError: Missing GOOGLE_API_KEY in .env`

1. Make sure the `.env` file exists in the `agents/` directory (not the root directory)
2. Verify the API key is correctly set in the file
3. Check that the file has the correct permissions
4. Ensure there are no extra spaces or quotes around the API key

## 🔒 Security Note
- Never commit your `.env` file to version control
- Keep your API keys secret and secure
- The `.gitignore` file should already exclude `.env` files
