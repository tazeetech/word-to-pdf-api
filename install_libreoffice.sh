#!/bin/bash

# Install LibreOffice on Render.com
# This script installs LibreOffice and necessary dependencies

echo "🚀 Starting LibreOffice installation for Render.com..."

# Update package list
echo "📦 Updating package list..."
apt-get update -y

# Install LibreOffice and dependencies
echo "📥 Installing LibreOffice and dependencies..."
apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    libreoffice-draw \
    libreoffice-math \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-freefont-ttf \
    fontconfig

# Install additional fonts for better compatibility
echo "🔤 Installing additional fonts..."
apt-get install -y \
    fonts-noto \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-liberation2

# Update font cache
echo "🔄 Updating font cache..."
fc-cache -fv

# Verify LibreOffice installation
echo "✅ Verifying LibreOffice installation..."
if command -v libreoffice &> /dev/null; then
    echo "✅ LibreOffice installed successfully!"
    libreoffice --version
else
    echo "❌ LibreOffice installation failed!"
    exit 1
fi

# Check if soffice is available (alternative command)
if command -v soffice &> /dev/null; then
    echo "✅ LibreOffice soffice command available!"
    soffice --version
else
    echo "⚠️  soffice command not found, but libreoffice is available"
fi

echo "🎉 LibreOffice installation completed successfully!"
echo "📋 Available LibreOffice commands:"
echo "   - libreoffice"
echo "   - soffice (if available)"

# Set environment variables for better compatibility
export LIBREOFFICE_CMD=libreoffice
export SOFFICE_CMD=soffice

echo "🔧 Environment variables set:"
echo "   LIBREOFFICE_CMD=$LIBREOFFICE_CMD"
echo "   SOFFICE_CMD=$SOFFICE_CMD"

echo "✅ LibreOffice setup complete! Ready to convert documents."
