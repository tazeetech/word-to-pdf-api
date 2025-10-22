# Render.com Deployment Guide

## Overview
This Word to PDF converter is now configured to work on Render.com with LibreOffice automatically installed.

## Files Modified for Render.com Compatibility

### 1. `install_libreoffice.sh`
- **Purpose**: Installs LibreOffice and dependencies on Render.com
- **Features**:
  - Installs LibreOffice suite
  - Installs necessary fonts
  - Sets up environment variables
  - Verifies installation

### 2. `Procfile`
- **Before**: `web: bash install_libreoffice.sh && gunicorn app_working:app`
- **After**: `web: chmod +x install_libreoffice.sh && bash install_libreoffice.sh && gunicorn app_working:app --bind 0.0.0.0:$PORT`
- **Changes**:
  - Added executable permissions for install script
  - Added proper port binding for Render.com

### 3. `requirements.txt`
- **Added**: `docx2pdf==0.1.8` for additional conversion support
- **Note**: LibreOffice is installed via shell script, not pip

### 4. `app_working.py`
- **Enhanced LibreOffice detection**: Now supports both Windows and Linux paths
- **Improved LibreOffice conversion**: Added Linux-specific command arguments
- **Better environment handling**: Sets HOME and USER variables for LibreOffice
- **Dynamic port configuration**: Uses PORT environment variable from Render.com

## Deployment Steps

1. **Push your code to GitHub** (if not already done)
2. **Connect your repository to Render.com**
3. **Create a new Web Service** on Render.com
4. **Configure the service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app_working:app --bind 0.0.0.0:$PORT`
   - **Python Version**: 3.9 or higher
5. **Deploy**

## What Happens During Deployment

1. **Build Phase**: 
   - Installs Python dependencies from `requirements.txt`
2. **Start Phase**:
   - Makes install script executable
   - Runs `install_libreoffice.sh` to install LibreOffice
   - Starts the Flask app with Gunicorn

## Expected Behavior

- ✅ LibreOffice will be automatically installed
- ✅ The app will detect LibreOffice on Linux paths
- ✅ Word documents will convert to PDF successfully
- ✅ The app will work on both local development and Render.com

## Troubleshooting

If deployment fails:

1. **Check Render.com logs** for LibreOffice installation errors
2. **Verify all files are committed** to your repository
3. **Ensure Procfile is in root directory**
4. **Check that install_libreoffice.sh has proper permissions**

## Health Check

Visit `/health` endpoint to verify:
- LibreOffice installation status
- Available conversion tools
- System health

## Local Testing

To test locally with the same setup:
```bash
# Make script executable
chmod +x install_libreoffice.sh

# Install LibreOffice (Linux/Mac)
bash install_libreoffice.sh

# Run the app
python app_working.py
```

## Notes

- The installation script installs LibreOffice system-wide
- Fonts are installed for better document compatibility
- Environment variables are set for LibreOffice to work properly
- The app gracefully falls back to docx2pdf if LibreOffice fails
