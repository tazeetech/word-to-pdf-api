# Use a lightweight Python image
FROM python:3.11-slim

# Install system dependencies including LibreOffice and WeasyPrint dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libreoffice \
    libreoffice-writer \
    fonts-liberation \
    fonts-dejavu-core \
    fontconfig \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libcairo2 \
    libpango1.0-dev \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && fc-cache -fv

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Set environment variables
ENV FLASK_ENV=production

# Expose port (Render will set PORT dynamically)
EXPOSE 8000

# Run the app using Gunicorn with dynamic port
CMD gunicorn -w 2 -b 0.0.0.0:$PORT app:app
