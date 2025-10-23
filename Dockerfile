# Use a lightweight Python image
FROM python:3.11-slim

# Install system dependencies including LibreOffice in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libreoffice \
    libreoffice-writer \
    fonts-liberation \
    fonts-dejavu-core \
    fontconfig \
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
EXPOSE $PORT

# Run the app using Gunicorn with dynamic port
CMD gunicorn -w 2 -b 0.0.0.0:$PORT app:app
