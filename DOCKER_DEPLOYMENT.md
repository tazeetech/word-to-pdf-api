# Docker Deployment Guide for Render.com

## Files Created

### 1. Dockerfile
- Uses Python 3.11-slim base image
- Installs LibreOffice and all necessary dependencies
- Sets up the working directory and installs Python packages
- Configures Gunicorn to run the Flask app

### 2. render.yaml
- Configures Render.com to use Docker deployment
- Sets up environment variables
- Enables auto-deployment

## Deployment Steps

1. **Push your code to GitHub** (if not already done)
2. **Connect to Render.com**:
   - Go to Render.com dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select "Docker" as the environment
   - Render will automatically detect the Dockerfile

3. **Configuration**:
   - **Build Command**: (Leave empty - Docker handles this)
   - **Start Command**: (Leave empty - Docker handles this)
   - **Port**: 8000 (or leave empty for auto-detection)

4. **Deploy**: Click "Create Web Service"

## What This Solves

- ✅ LibreOffice is installed directly in the container
- ✅ All system dependencies are included
- ✅ Fonts are properly configured
- ✅ Multiple conversion methods available (docx2pdf, WeasyPrint, LibreOffice)
- ✅ Production-ready with Gunicorn

## Testing

After deployment, test these endpoints:
- `/` - Main upload page
- `/health` - Health check
- `/debug` - Debug information

## File Structure

Your project should now look like:
```
word-to-pdf/
├── app.py
├── requirements.txt
├── Dockerfile
├── render.yaml
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── uploads/
```

## Notes

- The Docker container includes LibreOffice, so your app will work reliably
- Render will automatically build and deploy when you push changes
- The app uses multiple conversion methods as fallbacks
- All conversion tools should be available in the container
