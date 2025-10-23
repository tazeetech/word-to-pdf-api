#!/bin/bash

# Build script for Render.com deployment
echo "🚀 Starting build process..."

# Make install script executable
echo "📝 Making install script executable..."
chmod +x install_libreoffice.sh

# Install LibreOffice
echo "📦 Installing LibreOffice..."
bash install_libreoffice.sh

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Build completed successfully!"

