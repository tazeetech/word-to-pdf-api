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

# Check libreoffice command
if command -v libreoffice &> /dev/null; then
    echo "✅ LibreOffice installed successfully!"
    libreoffice --version
    LIBREOFFICE_CMD="libreoffice"
else
    echo "❌ libreoffice command not found!"
    LIBREOFFICE_CMD=""
fi

# Check if soffice is available (alternative command)
if command -v soffice &> /dev/null; then
    echo "✅ LibreOffice soffice command available!"
    soffice --version
    SOFFICE_CMD="soffice"
else
    echo "⚠️  soffice command not found"
    SOFFICE_CMD=""
fi

# If neither command is found, try to find the executable
if [ -z "$LIBREOFFICE_CMD" ] && [ -z "$SOFFICE_CMD" ]; then
    echo "🔍 Searching for LibreOffice executables..."
    
    # Look for soffice in common locations
    for path in /usr/bin/soffice /usr/local/bin/soffice /opt/libreoffice/program/soffice; do
        if [ -f "$path" ]; then
            echo "✅ Found soffice at: $path"
            SOFFICE_CMD="$path"
            break
        fi
    done
    
    # Look for libreoffice in common locations
    for path in /usr/bin/libreoffice /usr/local/bin/libreoffice /opt/libreoffice/program/libreoffice; do
        if [ -f "$path" ]; then
            echo "✅ Found libreoffice at: $path"
            LIBREOFFICE_CMD="$path"
            break
        fi
    done
fi

# Final check
if [ -n "$LIBREOFFICE_CMD" ] || [ -n "$SOFFICE_CMD" ]; then
    echo "✅ LibreOffice installation verified!"
else
    echo "❌ LibreOffice installation failed - no executables found!"
    echo "🔍 Checking installed packages..."
    dpkg -l | grep -i libreoffice || echo "No LibreOffice packages found"
    exit 1
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
